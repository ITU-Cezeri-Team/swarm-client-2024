import paho.mqtt.client as mqtt
import time
import threading


def send_heartbeat(
    heartbeat_interval,
    topic,
):
    # send a heartbeat every heartbeat_interval seconds in an infinite loop
    while True:
        mqtt.Client.publish(topic)
        time.sleep(heartbeat_interval)


def start_heartbeat(client: mqtt.Client, heartbeat_interval: int):
    threading.Thread(target=send_heartbeat, args=(heartbeat_interval,)).start()
