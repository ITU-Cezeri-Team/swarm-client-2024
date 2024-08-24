import paho.mqtt.client as mqtt
from heartbeat import start_heartbeat
from pymavlink_helper import PyMavlinkHelper
from get_current_state import start_publishing_state


topic = "server"

MESSAGE_TYPES = {
    "init_connection": "init_connection",
    "arm": "arm",
    "disarm": "disarm",
    "takeoff": "takeoff",
    "land": "land",
    "move": "move",
    "set_mode": "set_mode",
    "heartbeat": "heartbeat",
}


def process_message(
    message: dict, client: mqtt.Client, helper: PyMavlinkHelper
) -> None:
    message_type = message["msg_type"]
    if message_type == MESSAGE_TYPES["init_connection"]:
        helper.initialize()

        heartbeat_interval = message["args"]["heartbeat_interval"] / 1000
        state_interval = message["args"]["state_interval"] / 1000
        start_heartbeat(client, heartbeat_interval)
        start_publishing_state(client, helper, topic, state_interval)

        pass
    elif message_type == MESSAGE_TYPES["arm"]:
        helper.arm(message["args"]["force"])
    elif message_type == MESSAGE_TYPES["disarm"]:
        helper.disarm(message["args"]["force"])
    elif message_type == MESSAGE_TYPES["takeoff"]:
        helper.takeoff(message["args"]["altitude"])
    elif message_type == MESSAGE_TYPES["land"]:
        helper.land()
    elif message_type == MESSAGE_TYPES["move"]:
        helper.move(
            message["args"]["lat"],
            message["args"]["lon"],
            message["args"]["alt"],
            message["args"]["vx"],
            message["args"]["vy"],
            message["args"]["vz"],
        )
    elif message_type == MESSAGE_TYPES["set_mode"]:
        pass
    elif message_type == MESSAGE_TYPES["heartbeat"]:
        pass
    else:
        raise ValueError("Invalid message type")
