'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2023-05-26 22:38:06
LastEditors: zhai
LastEditTime: 2023-05-27 00:16:20
'''

from time import sleep
from typing import Callable
import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

        self.on_connect_cb : Callable = None
        self.on_message_cb : Callable = None

        self.mqtt_client = None
        
        self.is_connected = False
        self.is_connecting = False

        self.reconnect_delay = 10
        self.client_keep_alive_time = 60
        self.polling_delay = 1

    def print(self, msg):
        print(f'[MqttClient]: {msg}')

    def check_connection(self) -> bool:
        if self.is_connected :
            return True
        
        return self._connect_once()
        
    def _connect_once(self) ->bool:
        if self.is_connecting:
            return True
        
        self.print(f'Connecting to MQTT broker (host: {self.host} | port: {self.port})')

        if self.mqtt_client is None:
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.on_connect = self.on_connect
            self.mqtt_client.on_disconnect = self.on_disconnect
            self.mqtt_client.on_message = self.on_message
            
            self.mqtt_client.reconnect_delay_set(min_delay=1, max_delay=self.reconnect_delay)
            
        try:
            # self.mqtt_client.reconnect()

            self.mqtt_client.connect(self.host, self.port, self.client_keep_alive_time)
            self.mqtt_client.loop_start()

            self.print("loop_start")
            self.is_connecting =True
            return True

        except Exception:
            return False

    def connect_loop(self):
        if self._connect_once():
            return 
        
        sleep(self.reconnect_delay)
        self.print(f'Retrying to connect with mqtt-broker')
        self.connect_loop()

    def on_connect(self, client, userdata, flags, rc):
        self.print(f'Received connect() status [{rc}]')
        self.is_connected = rc == mqtt.MQTT_ERR_SUCCESS
        if self.is_connected :
            self.print("Connected to mqtt-broker")
        
            if self.on_connect_cb:
                # Subscribing in on_connect() means that if we lose the connection and
                # reconnect then subscriptions will be renewed.
                self.on_connect_cb(client, userdata, flags, rc)
            

    def on_disconnect(self, client, userdata, rc):
        self.print("Client disconnected from mqtt-broker")
        self.is_connected = False

        # loop_stop() 不能写在on_disconnect 回调里, 否则 threading.current_thread() == client._thread，\
        # 客户端无法清除client._thread 子进程，以后再使用loop_start()就无效了
        # self.mqtt_client.loop_stop()
        # self.print("loop_stop")

    def on_message(self, client, userdata, msg):
        if self.on_message_cb:
            self.on_message_cb(client, userdata, msg)

    def publish(self, topic: str, data: str) -> None:
        if self.is_connected:
            message = self.mqtt_client.publish(topic, data, qos=2)
            message.wait_for_publish()

    # def subscribe(self, topic: str, handler: Callable) -> None:
    #     if self.mqtt_client.is_connected:
    #         self.mqtt_client.subscribe(topic)
    #         self.mqtt_client.message_callback_add(topic, handler)


