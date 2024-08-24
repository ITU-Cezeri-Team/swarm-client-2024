import paho.mqtt.client as mqtt
import json
from process_message import process_message


TOPIC_LIST = ["drone/1", "drone/2", "drone/3"]


def start_client():
    # MQTT Configuration
    BROKER = "192.168.1.127"
    PORT = 1883
    CLIENT_ID = "CLIENT1"

    def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage) -> None:
        message.payload.decode()
        json_data = json.loads(message.payload.decode())
        process_message(json_data, client)

    def on_connect(client: mqtt.Client, userdata, flags, rc) -> None:
        if rc == 0:
            print(f"Connected to MQTT Broker as {CLIENT_ID}")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    keep_alive = 60
    client.connect(BROKER, PORT, keep_alive)

    # Blocking loop to process network traffic, dispatches callbacks
    client.loop_forever()


if __name__ == "_main_":
    start_client()
