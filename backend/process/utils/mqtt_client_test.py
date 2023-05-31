'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2023-05-26 22:38:06
LastEditors: zhai
LastEditTime: 2023-05-26 23:49:03
'''

import time
from mqtt_client import MqttClient


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")
    client.subscribe("topic1/#")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))



broker_address = "127.0.0.1"    # broker address
port = 1883                         # broker port
# user = "abc"                        # connection username
# password = "123456"                 # connection password


client = MqttClient(broker_address, port)

# client.username_pw_set(user, password=password) 
client.on_connect_cb = on_connect
client.on_message_cb = on_message
# client.reconnect_delay_set(min_delay=3, max_delay=60)

while True:
    client.check_connection()
    client.publish("topic1", 'alive')
    # client.loop()
    time.sleep(2)