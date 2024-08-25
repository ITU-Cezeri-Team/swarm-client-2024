import paho.mqtt.client as mqtt
import json
from process_message import process_message
from logger import log_incoming_message
from pymavlink_helper import PyMavlinkHelper
from heartbeat_processor import HeartbeatProcessor
import argparse


LOG_PATH = "logs/"
PIXHAWK_CONNECTION_STRING = "serial:/dev/serial0:57600"


def start_client(client_id):
    helper = PyMavlinkHelper(PIXHAWK_CONNECTION_STRING)
    heartbeat_processor = HeartbeatProcessor(die_time=10)
    # MQTT Configuration
    BROKER = "192.168.1.127"
    PORT = 1883
    CLIENT_ID = "CLIENT_" + str(client_id)
    topic = "drone/" + str(client_id)

    def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage) -> None:
        json_data = json.loads(message.payload.decode())
        log_incoming_message(json_data, LOG_PATH)
        process_message(json_data, client, helper, heartbeat_processor, client_id)

    def on_connect(client: mqtt.Client, userdata, flags, rc) -> None:
        if rc == 0:
            print(f"Connected to MQTT Broker as {CLIENT_ID}")
            client.subscribe(topic)
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    keep_alive = 60
    client.connect(BROKER, PORT, keep_alive)

    # Blocking loop to process network traffic, dispatches callbacks
    client.loop_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "client_id", type=int, help="The unique client ID for the MQTT client (0, 1, 2)"
    )
    args = parser.parse_args()

    start_client(args.client_id)
