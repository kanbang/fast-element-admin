'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2023-05-31 10:28:12
LastEditors: zhai
LastEditTime: 2023-05-31 17:59:30
'''
import time
import logging
import redis
from utils.mqtt_client import MqttClient

# log
logger = logging.getLogger()
handler = logging.FileHandler('./save2redis.log')
logger.addHandler(handler)

# logger.error('haha')

# Redis数据库相关配置
redis_host = "localhost"
redis_port = 6379

redis_db =redis.Redis(host=redis_host,port=redis_port) # password="66666666666"


def on_connect(client, userdata, flags, rc):
    client.subscribe("$SYS/#")
    client.subscribe("topic1/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))



broker_address = "127.0.0.1"    # broker address
port = 1883                         # broker port
# user = "abc"                        # connection username
# password = "123456"                 # connection password

client = MqttClient(broker_address, port)

client.on_connect_cb = on_connect
client.on_message_cb = on_message

while True:
    client.check_connection()
    client.publish("topic1", 'alive')
    # client.loop()
    time.sleep(2)


redis_db.rpush("18",1)      
redis_db.rpush("18",2)      
redis_db.rpush("18",3)      
redis_db.lrange("18",0,-1)  
redis_db.llen("8")       
