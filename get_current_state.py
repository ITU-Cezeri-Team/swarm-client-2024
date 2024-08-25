import time
import threading


def start_publishing_state(client, helper, topic, state_interval):
    def publish_loop():
        while True:
            publish_state(client, helper, topic)
            time.sleep(state_interval)

    thread = threading.Thread(target=publish_loop)
    thread.daemon = True
    thread.start()


def publish_state(client, helper, topic):
    latitude, longitude, altitude = helper.get_current_state()
    if latitude is not None and longitude is not None and altitude is not None:
        state_msg = {
            "lat": latitude,
            "lon": longitude,
            "alt": altitude,
        }
        client.publish(topic, str(state_msg))
        # print(f"Published state to topic {topic}: {state_msg}")
    else:
        print("Failed to retrieve GPS coordinates, not publishing.")
