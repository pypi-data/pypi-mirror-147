"""MQTT client for local broker inter-service communications.

This MQTT client sets up automatic connection and reconnection intended mainly
for use with a local broker on an edge device e.g. Raspberry Pi.

Reads broker configuration from a local `.env` file or environment variables:

* `MQTT_HOST` the IP address or hostname or container of the broker
* `MQTT_USER` the authentication username for the broker
* `MQTT_PASS` the authentication password for the broker

Typically the `fieldedge-broker` will be a **Mosquitto** service running locally
in a **Docker** container listening on port 1883 for authenticated connections.

"""
import json
import logging
import os
from atexit import register as on_exit
from socket import timeout   #: for Python < 3.10 compatibility vs TimeoutError
from threading import enumerate as enumerate_threads
from time import sleep, time
from typing import Callable, Union

from dotenv import load_dotenv
from paho.mqtt.client import MQTT_ERR_SUCCESS, Client

_log = logging.getLogger(__name__)

load_dotenv()

CONNECTION_RESULT_CODES = {
    0: 'MQTT_ERR_SUCCESS',
    1: 'MQTT_ERR_INCORRECT_PROTOCOL',
    2: 'MQTT_ERR_INVALID_CLIENT_ID',
    3: 'MQTT_ERR_SERVER_UNAVAILABLE',
    4: 'MQTT_ERR_BAD_USERNAME_PASSWORD',
    5: 'MQTT_ERR_UNAUTHORIZED',
    6: 'MQTT_ERR_CONNECTION_LOST',
    7: 'MQTT_ERR_TIMEOUT_WAITING_FOR_LENGTH',
    8: 'MQTT_ERR_TIMEOUT_WAITING_FOR_PAYLOAD',
    9: 'MQTT_ERR_TIMEOUT_WAITING_FOR_CONNACK',
    10: 'MQTT_ERR_TIMEOUT_WAITING_FOR_SUBACK',
    11: 'MQTT_ERR_TIMEOUT_WAITING_FOR_UNSUBACK',
    12: 'MQTT_ERR_TIMEOUT_WAITING_FOR_PINGRESP',
}


def _get_mqtt_result(rc: int) -> str:
    if rc in CONNECTION_RESULT_CODES:
        return CONNECTION_RESULT_CODES[rc]
    return 'UNKNOWN'


class MqttError(Exception):
    """A MQTT-specific error."""
    pass


class MqttClient:
    """A customized MQTT client.

    Attributes:
        client_id (str): A unique client_id.
        on_message (Callable): A function called when a subscribed message
            is received from the broker.
        on_connect (Callable): A function called when the client connects
            to the broker.
        on_disconnect (Callable): A function called when the client disconnects.
        is_connected (bool): Status of the connection to the broker.
        connect_retry_interval (int): Seconds between broker reconnect attempts.

    """
    def __init__(self,
                 client_id: str,
                 on_message: Callable[..., "tuple[str, object]"] = None,
                 subscribe_default: Union[str, "list[str]"] = None,
                 on_connect: Callable = None,
                 on_disconnect: Callable = None,
                 connect_retry_interval: int = 5,
                 auto_connect: bool = True,
                 port: int = 1883,
                 keepalive: int = 60,
                 bind_address: str = '',
                 certfile: str = None,
                 ):
        """Initializes a managed MQTT client.
        
        Args:
            client_id (str): The unique client ID
            on_message (Callable): The callback when subscribed messages are
                received as `topic, message`.
            subscribe_default (Union[str, list[str]]): The default
                subscription(s) established on re/connection.
            on_connect (Callable): (optional) callback when connection to the
                broker is established.
            on_disconnect (Callable): (optional) callback when disconnecting
                from the broker.
            logger (Logger): (optional) Logger
            connect_retry_interval (int): Seconds between broker reconnect
                attempts.
            auto_connect (bool): Automatically attempts to connect when created.
            port (int): The MQTT port the broker is listening on.
            keepalive (int): The socket timeout and/or keepalive ping interval
                in seconds.
            bind_address (str): (optional) A local bind address
            certfile (str): If using TLS, the path of the certificate

        Raises:
            `MqttError` if the client_id is not valid.

        """
        self._host = os.getenv('MQTT_HOST') or 'fieldedge-broker'
        self._user = os.getenv('MQTT_USER') or None
        self._pass = os.getenv('MQTT_PASS') or None
        self._port = port
        self._keepalive = keepalive
        self._bind_address = bind_address
        self._certfile = certfile
        if not isinstance(client_id, str) or client_id == '':
            _log.error('Invalid client_id')
            raise MqttError('Invalid client_id')
        if not callable(on_message):
            _log.warning('No on_message specified')
        on_exit(self._cleanup)
        self.on_message = on_message
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.client_id = client_id
        self._mqtt = Client()
        self.is_connected = False
        self._subscriptions = {}
        self.connect_retry_interval = connect_retry_interval
        self.auto_connect = auto_connect
        self._failed_connect_attempts = 0
        if subscribe_default:
            if not isinstance(subscribe_default, list):
                subscribe_default = [subscribe_default]
            for sub in subscribe_default:
                self.subscribe(sub)
        if self.auto_connect:
            self.connect()
    
    @property
    def client_id(self):
        return self._client_id
    
    @client_id.setter
    def client_id(self, id: str):
        try:
            if isinstance(int(id.split('_')[1]), int):
                # previously made unique, could be a bouncing MQTT connection
                id = id.split('_')[0]
        except (ValueError, IndexError):
            pass   #: new id will be made unique
        self._client_id = f'{id}_{int(time())}'

    @property
    def subscriptions(self) -> dict:
        """The dictionary of subscriptions.
        
        Use subscribe or unsubscribe to change the dict.

        'topic' : { 'qos': (int), 'mid': (int) }

        """
        return self._subscriptions

    @property
    def failed_connection_attempts(self) -> int:
        return self._failed_connect_attempts

    def _cleanup(self, *args):
        # TODO: logging raises an error since the log file was closed
        # for arg in args:
        #     _log.debug(f'mqtt cleanup called with arg = {arg}')
        # _log.debug('Terminating MQTT connection')
        self._mqtt.user_data_set('terminate')
        self._mqtt.loop_stop()
        self._mqtt.disconnect()
    
    def connect(self):
        """Attempts to establish a connection to the broker and re-subscribe."""
        try:
            _log.debug(f'Attempting MQTT broker connection to {self._host}'
                       f' as {self._client_id}')
            self._mqtt.reinitialise(client_id=self.client_id)
            self._mqtt.user_data_set(None)
            self._mqtt.on_connect = self._mqtt_on_connect
            self._mqtt.on_disconnect = self._mqtt_on_disconnect
            self._mqtt.on_subscribe = self._mqtt_on_subscribe
            self._mqtt.on_message = self._mqtt_on_message
            if self._user and self._pass:
                self._mqtt.username_pw_set(username=self._user,
                                           password=self._pass)
            if self._port == 8883:
                self._mqtt.tls_set(self._certfile)
                self._mqtt.tls_insecure_set(True)
            self._mqtt.connect(self._host,
                               port=self._port,
                               keepalive=self._keepalive,
                               bind_address=self._bind_address)
            threads_before = enumerate_threads()
            self._mqtt.loop_start()
            threads_after = enumerate_threads()
            for thread in threads_after:
                if thread in threads_before:
                    continue
                thread.name = 'MqttThread'
                break
        except (ConnectionError, timeout, TimeoutError) as err:
            self._failed_connect_attempts += 1
            if self.connect_retry_interval > 0:
                _log.warning(f'Unable to connect to {self._host} ({err})'
                             f' - retrying in {self.connect_retry_interval} s')
                sleep(self.connect_retry_interval)
                self.connect()
            else:
                _log.warning(f'Failed to connect to {self._host}'
                             ' but retry disabled - call connect() to retry')

    def disconnect(self):
        """Attempts to disconnect from the broker."""
        self._mqtt.user_data_set('terminate')
        self._mqtt.loop_stop()
        self._mqtt.disconnect()

    def _mqtt_on_connect(self, client, userdata, flags, rc):
        self._failed_connect_attempts = 0
        if rc == 0:
            _log.debug(f'Established MQTT connection to {self._host}')
            if not self.is_connected:
                for sub in self.subscriptions:
                    self._mqtt_subscribe(sub, self.subscriptions[sub]['qos'])
                self.is_connected = True
            if self.on_connect:
                self.on_connect(client, userdata, flags, rc)
        else:
            _log.error(f'MQTT broker connection result code: {rc}'
                       f' ({_get_mqtt_result(rc)})')
    
    def _mqtt_subscribe(self, topic: str, qos: int = 0):
        _log.debug(f'{self._client_id} subscribing to {topic} (qos={qos})')
        (result, mid) = self._mqtt.subscribe(topic=topic, qos=2)
        if result == MQTT_ERR_SUCCESS:
            self._subscriptions[topic]['mid'] = mid
        else:
            _log.error(f'MQTT Error {result} subscribing to {topic}')

    def _mqtt_unsubscribe(self, topic: str):
        _log.debug(f'{self._client_id} unsubscribing to {topic}')
        (result, mid) = self._mqtt.unsubscribe(topic)
        if result != MQTT_ERR_SUCCESS:
            _log.error(f'MQTT Error {result} unsubscribing to {topic}')

    def subscribe(self, topic: str, qos: int = 0) -> None:
        """Adds a subscription.
        
        Subscriptions property is updated with qos and message id.

        Args:
            topic (str): The MQTT topic to subscribe to
            qos (int): The MQTT qos 0..2

        """
        _log.debug(f'Adding subscription {topic} (qos={qos})')
        self._subscriptions[topic] = {'qos': qos, 'mid': 0}
        if self.is_connected:
            self._mqtt_subscribe(topic, qos)
        else:
            _log.warning('MQTT not connected will subscribe later')

    def unsubscribe(self, topic: str) -> None:
        """Removes a subscription.
        
        Args:
            topic (str): The MQTT topic to unsubscribe

        """
        _log.debug(f'Removing subscription {topic}')
        if topic in self._subscriptions:
            del self._subscriptions[topic]
        if self.is_connected:
            self._mqtt_unsubscribe(topic)

    def _mqtt_on_disconnect(self, client, userdata, rc):
        if self.on_disconnect:
            self.on_disconnect(client, userdata, rc)
        if userdata != 'terminate':
            _log.warning('MQTT broker disconnected'
                              f' - result code {rc} ({_get_mqtt_result(rc)})')
            self._mqtt.loop_stop()
            # get new unique ID to avoid bouncing connection
            self.client_id = self.client_id
            self.is_connected = False
            if self.auto_connect:
                self.connect()

    def _mqtt_on_subscribe(self, client, userdata, mid, granted_qos):
        _log.debug(f'MQTT subscription message id: {mid}')
        for sub in self.subscriptions:
            if mid != self.subscriptions[sub]['mid']:
                _log.error('Subscription failed'
                                f' message id={mid}'
                                f' expected {self.subscriptions[sub]["mid"]}')
            else:
                _log.info(f'Subscription to {sub} successful')

    def _mqtt_on_message(self, client, userdata, message):
        payload = message.payload.decode()
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError as e:
            _log.debug(f'MQTT message payload non-JSON ({e})')
        _log.debug(f'MQTT received message "{payload}"'
            f'on topic "{message.topic}" with QoS {message.qos}')
        if userdata:
            _log.debug(f'MQTT client userdata: {userdata}')
        self.on_message(message.topic, payload)

    def publish(self, topic: str, message: 'str|dict', qos: int = 1):
        """Publishes a message to a MQTT topic.

        If the message is a dictionary, 
        
        Args:
            topic (str): The MQTT topic
            message (str|dict): The message to publish
            qos (int): The MQTT Quality of Service (0, 1 or 2)

        """
        if not isinstance(message, str):
            message = json.dumps(message, skipkeys=True)
        if not isinstance(qos, int) or qos not in range(0, 3):
            _log.warning(f'Invalid MQTT QoS {qos} - using QoS 1')
            qos = 1
        _log.debug(f'MQTT publishing: {topic}: {message}')
        (rc, mid) = self._mqtt.publish(topic=topic, payload=message, qos=qos)
        del mid
        if rc != MQTT_ERR_SUCCESS:
            errmsg = f'Publishing error {rc} ({_get_mqtt_result(rc)})'
            _log.error(errmsg)
            # raise MqttError(errmsg)
