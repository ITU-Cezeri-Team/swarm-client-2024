import paho.mqtt.client as mqtt
from pymavlink import mavutil

client_id = "pi_zero_client_1"  # Pi Zero ID
MQTT_BROKER = "your_mqtt_broker_ip"
MQTT_PORT = 1883

PIXHAWK_CONNECTION_STRING = "serial:/dev/ttyAMA0:115200"


def on_message(client, userdata, message):
    if message.topic == f"drone/{client_id}/init":
        print("Received initialization request")
        try:
            # Pixhawk'a bağlan
            vehicle = mavutil.mavlink_connection(PIXHAWK_CONNECTION_STRING)
            vehicle.wait_heartbeat()
            print("Connected to Pixhawk")

            # Bağlantı bilgisini bilgisayara gönder
            client.publish(f"drone/{client_id}/status", "connected")
        except Exception as e:
            print(f"Failed to connect to Pixhawk: {e}")
            client.publish(f"drone/{client_id}/status", "failed")


mqtt_client = mqtt.Client(client_id=client_id)
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(f"drone/{client_id}/init")  # Initialize mesajlarını dinle
mqtt_client.loop_forever()
