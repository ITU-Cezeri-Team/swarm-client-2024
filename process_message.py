import paho.mqtt.client as mqtt
from heartbeat import start_heartbeat

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


def process_message(message: dict, client: mqtt.Client) -> None:
    message_type = message["msg_type"]
    if message_type == MESSAGE_TYPES["init_connection"]:
        heartbeat_interval = message["args"]["heartbeat_interval"]
        start_heartbeat(client, heartbeat_interval)
        # TODO: Implement send_current_state
        pass
    elif message_type == MESSAGE_TYPES["arm"]:
        pass
    elif message_type == MESSAGE_TYPES["disarm"]:
        pass
    elif message_type == MESSAGE_TYPES["takeoff"]:
        pass
    elif message_type == MESSAGE_TYPES["land"]:
        pass
    elif message_type == MESSAGE_TYPES["move"]:
        pass
    elif message_type == MESSAGE_TYPES["set_mode"]:
        pass
    elif message_type == MESSAGE_TYPES["heartbeat"]:
        pass
    else:
        raise ValueError("Invalid message type")
