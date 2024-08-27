import paho.mqtt.client as mqtt
from heartbeat import start_heartbeat
from pymavlink_helper import PyMavlinkHelper
from heartbeat_processor import HeartbeatProcessor
from get_current_state import start_publishing_state
import time

MESSAGE_TYPES = {
    "init_connection": "init_connection",
    "arm": "arm",
    "disarm": "disarm",
    "takeoff": "takeoff",
    "land": "land",
    "move": "move",
    "set_mode": "set_mode",
    "heartbeat": "heartbeat",
    "end_connection": "end_connection",
    "compass_calibration": "compass_calibration",
    "accel_compass": "accel_compass",
}


def process_message(
    message: dict,
    client: mqtt.Client,
    helper: PyMavlinkHelper,
    heartbeat_processor: HeartbeatProcessor,
    client_id: int,
) -> None:
    topic = "server/" + str(client_id)
    message_type = message["msg_type"]
    if message_type == MESSAGE_TYPES["init_connection"]:
        helper.initialize()

        heartbeat_interval = message["args"]["heartbeat_interval"] / 1000
        state_interval = message["args"]["state_interval"] / 1000
        start_heartbeat(client, heartbeat_interval, topic)
        start_publishing_state(client, helper, topic, state_interval)

    elif message_type == MESSAGE_TYPES["arm"]:
        helper.arm(message["args"]["force"])

    elif message_type == MESSAGE_TYPES["disarm"]:
        helper.disarm(message["args"]["force"])

    elif message_type == MESSAGE_TYPES["takeoff"]:
        helper.takeoff(message["args"]["altitude"])

    elif message_type == MESSAGE_TYPES["land"]:
        helper.land()

    elif message_type == MESSAGE_TYPES["move"]:
        print('Move received')
        helper.move(
            message["args"]["lat"],
            message["args"]["lon"],
            message["args"]["alt"],
            message["args"]["vx"],
            message["args"]["vy"],
            message["args"]["vz"],
        )

    elif message_type == MESSAGE_TYPES["set_mode"]:
        helper.set_mode(message["args"]["mode"])

    elif message_type == MESSAGE_TYPES["heartbeat"]:
        heartbeat_processor.recieve_heartbeat()

    elif message_type == MESSAGE_TYPES["end_connection"]:
        client.disconnect()
        time.sleep(2)
        exit()

    else:
        raise ValueError("Invalid message type")
