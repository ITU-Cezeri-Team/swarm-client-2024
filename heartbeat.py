import paho.mqtt.client as mqtt
import time
import threading
import json


def send_heartbeat(
    heartbeat_interval: int,
    client: mqtt.Client,
    topic: str,
):
    msg = {
        "msg_type": "heartbeat",
        "args": {},
    }
    # send a heartbeat every heartbeat_interval seconds in an infinite loop
    while True:
        client.publish(topic, json.dumps(msg))

        time.sleep(heartbeat_interval)


def start_heartbeat(client: mqtt.Client, heartbeat_interval: int, topic: str):
    threading.Thread(
        target=send_heartbeat, args=(heartbeat_interval, client, topic)
    ).start()
