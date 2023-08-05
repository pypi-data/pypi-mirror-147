import time
from robertcommonio.system.io.mqtt import MQTTConfig, MQTTAccessor
from datetime import datetime

HOST = 'mqtt.smartbeop.com'
PORT = 8883
client_id = 'aiot_webapi_hqyc_client'
TOPIC = 'clp/project/data/ahu' #'SUBSTATION/MASTER/200120-1/S_SNT_DA' #'SUBSTATION/MASTER/200120-1/S_SNT_DAT'
USER = 'clp'
PSW = '9T3QV7hdjcHNIHpt'

def call_back(data):
    print(data)

def test_pub():
    accessor = MQTTAccessor(MQTTConfig(HOST=HOST, PORT=PORT, USER=USER, PSW=PSW, TOPIC=TOPIC, CLIENT_ID=client_id, KEEP_ALIVE=60))
    while True:
        accessor.publish_topic(TOPIC, datetime.now().strftime('%H:%M:%S'), 0)
        time.sleep(2)

def test_sub():
    accessor = MQTTAccessor(MQTTConfig(HOST=HOST, PORT=PORT, USER=USER, PSW=PSW, TOPIC=TOPIC, CLIENT_ID=client_id, KEEP_ALIVE=60, ENABLE_LOG=True))
    accessor.subscribe_topics(TOPIC, 0, 10, call_back)

test_pub()
