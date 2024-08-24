from pymavlink import mavutil
import time
from pymavlink_utils import (
    request_global_position,
    set_mode,
    try_recv_match,
    send_position_target_global_int,
)
from typing import List, Tuple
import threading


class PyMavlinkHelper:
    """
    PyMavlink environment helper class that provides a high-level interface to interact with the environment.
    """

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
        pass

    def initialize(self) -> None:
        """
        Initialize the environment.
        """
        vehicle = mavutil.mavlink_connection(self.connection_string, timeout=30)
        vehicle.wait_heartbeat()
        self.vehicle = vehicle
        print("Connected to Pixhawk")

        request_global_position(vehicle, rate=10)
        time.sleep(0.5)
        set_mode(vehicle, "LOITER")

    def arm(self, force) -> None:
        """
        Arm the vehicle.
        """

        try:
            self.vehicle.mav.command_long_send(
                self.vehicle.target_system,
                self.vehicle.target_component,
                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                0,
                1,
                2989 if force else 0,
                0,
                0,
                0,
                0,
                0,
            )
            ack_msg = try_recv_match(self.vehicle, message_name="COMMAND_ACK")
            if ack_msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                set_mode(self.vehicle, "GUIDED")
                print(f"Drone armed")
            else:
                print(f"Failed to arm drone")
        except Exception as e:
            raise ValueError(f"Failed to arm drone: {e}")

    def disarm(self, force: bool) -> None:
        """
        Disarm the vehicle.
        """
        try:
            self.vehicle.mav.command_long_send(
                self.vehicle.target_system,
                self.vehicle.target_component,
                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                0,
                0,
                21196 if force else 0,
                0,
                0,
                0,
                0,
                0,
            )
            ack_msg = try_recv_match(self.vehicle, message_name="COMMAND_ACK")
            if ack_msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                print(f"Drone disarmed")
            else:
                print(f"Failed to disarm drone")
        except Exception as e:
            raise ValueError(f"Failed to disarm drone: {e}")

    def takeoff(self, target_altitude: float) -> None:
        """
        Takeoff the vehicle to the specified altitude.

        Args:
            target_altitude (float): The altitude to reach in meters. Must be greater than 0.
        """

        def monitor_altitude():
            while True:
                msg = try_recv_match(self.vehicle, message_name="GLOBAL_POSITION_INT")
                altitude = msg.relative_alt / 1000.0  # altitude in meters
                print(f"Altitude: {altitude}")
                if altitude >= target_altitude * 0.85:  # 85% of target altitude
                    print("Reached target altitude")
                    break
                time.sleep(1)  # Wait before checking altitude again

        try:
            if target_altitude <= 0:
                return  # Do not proceed with takeoff if altitude is 0 or less
            print("Taking off...")

            self.vehicle.mav.command_long_send(
                self.vehicle.target_system,
                self.vehicle.target_component,
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                target_altitude,
            )

            # Start the altitude monitoring in a separate thread
            altitude_thread = threading.Thread(target=monitor_altitude)
            altitude_thread.start()

        except Exception as e:
            print(f"Error during takeoff: {e}")

    def land(self) -> None:
        """
        Initiate the landing process of the drone.
        """

        def monitor_landing():
            while True:
                msg = try_recv_match(self.vehicle, message_name="GLOBAL_POSITION_INT")
                altitude = msg.relative_alt / 1000.0  # altitude in meters
                print(f"Drone Altitude: {altitude}")
                if (
                    altitude <= 0.3
                ):  # Assume landed if altitude is less than or equal to 0.3 meters
                    print("Drone Landed")
                    break
                time.sleep(1)

        try:
            print("Landing drone...")
            self.vehicle.mav.command_long_send(
                self.vehicle.target_system,
                self.vehicle.target_component,
                mavutil.mavlink.MAV_CMD_NAV_LAND,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            )
            time.sleep(0.3)

            # Start the landing monitoring in a separate thread
            landing_thread = threading.Thread(target=monitor_landing)
            landing_thread.start()

        except Exception as e:
            print(f"Error during landing: {e}")

    def move(
        self,
        lat: float,
        lon: float,
        alt: float,
        vx: float,
        vy: float,
        vz: float,
    ) -> None:
        """
        Move a drone to the target coordinates.

        Args:
            drone_index (int): Index of the drone to move.
            target_coordinates (Tuple[float, float, float]): Target coordinates (x, y, z).
        """
        try:
            # Send position target
            send_position_target_global_int(self.vehicle, lat, lon, alt, vx, vy, vz)

            # Log the movement
            self._log_message(
                f"Drone moving to {lat, lon, alt} with velocity {vx, vy, vz}"
            )

        except Exception as e:
            self._log_message(f"Error moving drone: {str(e)}")

    def set_mode(self, mode: str) -> None:
        pass

    def get_current_state(self) -> Tuple[float, float, float]:
        msg = try_recv_match(self.vehicle, message_name="GLOBAL_POSITION_INT")
        latitude = msg.lat / 1e7
        longtitude = msg.lon / 1e7
        altitude = msg.relative_alt / 1000.0

        return latitude, longtitude, altitude