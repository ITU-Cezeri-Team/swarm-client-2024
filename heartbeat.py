import paho.mqtt.client as mqtt
import time
import threading
import json


def send_heartbeat(
    heartbeat_interval,
    topic,
):
    msg = {
        "msg_type": "heartbeat",
        "args": {},
    }
    # send a heartbeat every heartbeat_interval seconds in an infinite loop
    while True:
        mqtt.Client.publish(topic, json.dumps(msg))

        time.sleep(heartbeat_interval)


def start_heartbeat(client: mqtt.Client, heartbeat_interval: int):
    threading.Thread(target=send_heartbeat, args=(heartbeat_interval,)).start()
