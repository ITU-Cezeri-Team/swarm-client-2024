from pymavlink import mavutil
import time


def try_recv_match(vehicle, message_name, retries=10, timeout=1, blocking=False):
    """
    Tries to receive a MAVLink message by matching the message name.

    Parameters:
        vehicle: The vehicle object.
        message_name: The name of the MAVLink message to match.
        retries: Number of times to retry if no message is received.
        timeout: Timeout for each recv_match attempt in seconds.

    Returns:
        The matched MAVLink message if successful, None otherwise.
    """
    # print(f"Attempt to receive {message_name} message...")
    for attempt in range(1, retries + 1):
        # print(f"Attempt {attempt} to receive {message_name} message...")
        try:
            # Try to receive the matched message
            msg = vehicle.recv_match(
                type='GLOBAL_POSITION_INT', blocking=blocking, timeout=timeout
            )
            if msg != None:
                print(f"Received {message_name} message.")
                return msg  # Return the received message if successful
        except Exception as e:
            print(f"Error receiving {message_name}: {str(e)}")

        # If the message was not received, wait a bit before retrying
        print(
            f"{message_name} message not received. Retrying after {timeout} seconds..."
        )
        time.sleep(timeout)

    print(f"Failed to receive {message_name} message after {retries} attempts.")
    return None  # Return None if all attempts fail


def request_global_position(drone, rate=2):
    """
    Requests the GLOBAL_POSITION_INT data stream at a specified rate.

    Args:
        drone (mavutil.mavlink_connection): The drone connection.
        rate (int): The rate at which to request the data stream (Hz). Default is 1 Hz.
    """
    drone.mav.request_data_stream_send(
        drone.target_system,
        drone.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_POSITION,
        rate,
        1,  # Enable the stream
    )
    print(f"Requested GLOBAL_POSITION_INT data stream at {rate} Hz")


def set_drone_mode(drone: mavutil.mavlink_connection, mode: str) -> None:
    """
    Sets the flight mode of the drone.

    This function attempts to change the flight mode of a drone by sending the appropriate
    MAVLink command. It waits for an acknowledgment from the drone to confirm the mode change.

    Parameters
    ----------
    drone : mavutil.mavlink_connection
        The MAVLink connection object representing the drone.
    mode : str
        The desired flight mode (e.g., "GUIDED", "LOITER", "RTL").

    Raises
    ------
    ValueError
        If the specified mode is unknown or the mode change is not accepted by the drone.
    RuntimeError
        If no acknowledgment is received or an error occurs during the mode change process.
    """

    # Get the mode ID
    if mode not in drone.mode_mapping():
        print(f"Unknown mode: {mode}")
        print(f"Available modes: {list(drone.mode_mapping().keys())}")
        return  # TODO assert exception here

    mode_id = drone.mode_mapping()[mode]

    # Set the mode
    drone.mav.set_mode_send(
        drone.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id,
    )

    # Wait for ACK command
    # MAVLink requires an ACK from the drone to confirm the mode change
    ack = None
    while not ack:
        ack = try_recv_match(drone, message_name="COMMAND_ACK", blocking=True)
        if ack:
            try:
                ack_result = ack.result
                if ack.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
                    if ack_result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                        print(f"Mode change to {mode} accepted")
                    else:
                        print(
                            mavutil.mavlink.enums["MAV_RESULT"][
                                ack_result["result"]
                            ].description
                        )
                    break
            except AttributeError as e:
                print(
                    f"Error processing ACK message: {e}"
                )  # TODO assert exception here
        else:
            print("No ACK received, retrying...")

    # Wait for ACK command
    # MAVLink requires an ACK from the drone to confirm the mode change
    # ack = None
    # while not ack:
    #     ack = try_recv_match(drone, message_name="COMMAND_ACK")
    #     if ack:
    #         try:
    #             ack_result = ack.result
    #             if ack.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
    #                 if ack_result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
    #                     print(f"Mode change to {mode} accepted")
    #                 else:
    #                     print(
    #                         f"Mode change to {mode} failed with result {ack_result}"  # TODO assert exception here
    #                     )
    #                 break
    #         except AttributeError as e:
    #             print(
    #                 f"Error processing ACK message: {e}"
    #             )  # TODO assert exception here
    #     else:
    #         print("No ACK received, retrying...")


def send_position_target_global_int(
    drone: mavutil.mavlink_connection,
    lat: float,
    lon: float,
    alt: float,
    vx: float = 0,
    vy: float = 0,
    vz: float = 0,
    yaw: float = 0,
    yaw_rate: float = 0,
) -> None:
    """
    Send a position target message to the drone using global coordinates.

    Args:
        drone (mavutil.mavlink_connection): The drone connection.
        lat (float): Latitude in degrees.
        lon (float): Longitude in degrees.
        alt (float): Altitude in meters.
        vx (float): X velocity in m/s.
        vy (float): Y velocity in m/s.
        vz (float): Z velocity in m/s.
        yaw (float): Yaw angle in radians.
        yaw_rate (float): Yaw rate in radians/second.
    """
    drone.mav.send(
        drone.mav.set_position_target_global_int_encode(
            0,  # time_boot_ms (not used)
            0,
            0,  # target system, target component
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,  # frame
            0b0000111111111000,  # type_mask (only positions enabled)
            int(lat * 1e7),
            int(lon * 1e7),
            alt,  # lat, lon, alt
            vx,
            vy,
            vz,  # x, y, z velocity in m/s (not used)
            0,
            0,
            0,  # afx, afy, afz acceleration (not used)
            yaw,
            yaw_rate,  # yaw, yaw_rate (not used)
        )
    )
