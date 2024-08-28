from pymavlink import mavutil
import time
from pymavlink_utils import (
    request_global_position,
    set_drone_mode,
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
        self.is_initialized = False
        pass

    def initialize(self) -> None:
        """
        Initialize the environment.
        """
        if self.is_initialized:
            return
        vehicle = mavutil.mavlink_connection(self.connection_string, baud=57600)
        vehicle.wait_heartbeat()
        request_global_position(vehicle, rate=10)
        self.vehicle = vehicle
        self.is_initialized = True
        print("Connected to Pixhawk")
        time.sleep(0.5)
        set_drone_mode(vehicle, "GUIDED")
        time.sleep(0.5)
        print("Environment initialized")

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
            if (
                ack_msg != None
                and ack_msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED
            ):
                # time.sleep(2)
                # set_drone_mode(self.vehicle, "GUIDED")
                self.is_armed = True
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
            if (
                ack_msg != None
                and ack_msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED
            ):
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
                if msg == None:
                    continue
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
                if msg == None:
                    continue
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
            send_position_target_global_int(self.vehicle, lat, lon, alt, 0, 0, 0)

            print(f"Drone moving to {lat, lon, alt} with velocity 0, 0, 0")

        except Exception as e:
            print(f"Error moving drone: {str(e)}")

    def set_mode(self, mode: str) -> None:
        set_drone_mode(self.vehicle, mode)

    def get_current_state(self) -> Tuple[float, float, float]:
        msg = try_recv_match(self.vehicle, message_name="GLOBAL_POSITION_INT")
        if msg == None:
            return None
        latitude = msg.lat / 1e7
        longtitude = msg.lon / 1e7
        altitude = msg.relative_alt / 1000.0

        return latitude, longtitude, altitude

    def start_compass_calibration(self) -> None:
        """
        Start compass calibration for the drone.
        """
        print("Starting compass calibration...")

        try:
            # Send MAV_CMD_DO_START_MAG_CAL command
            self.vehicle.mav.command_long_send(
                self.vehicle.target_system,
                self.vehicle.target_component,
                mavutil.mavlink.MAV_CMD_DO_START_MAG_CAL,
                0,  # confirmation
                0,  # autopilot mag device ID (0 for all)
                1,  # autopilot mag orientation
                1,  # internal mag orientation
                0,  # external mag 1 orientation (0 for default)
                0,  # external mag 2 orientation (0 for default)
                0,  # external mag 3 orientation (0 for default)
                0,  # reserved, set to 0
            )

            # Monitor the calibration process
            while True:
                msg = self.vehicle.recv_match(
                    type=["MAG_CAL_PROGRESS", "MAG_CAL_REPORT"], blocking=True
                )
                if msg:
                    print(msg)
                    if (
                        msg.get_type() == "MAG_CAL_REPORT" and msg.cal_status == 5
                    ):  # 5 indicates calibration completed
                        print("Compass calibration completed successfully!")
                        break
                time.sleep(0.5)

        except Exception as e:
            print(f"Compass calibration failed: {str(e)}")

    def cancel_compass_calibration(self) -> None:
        """
        Cancel ongoing compass calibration.
        """
        print("Cancelling compass calibration...")

        try:
            # Send MAV_CMD_DO_CANCEL_MAG_CAL command
            self.vehicle.mav.command_long_send(
                self.vehicle.target_system,
                self.vehicle.target_component,
                mavutil.mavlink.MAV_CMD_DO_CANCEL_MAG_CAL,
                0,  # confirmation
                0,  # Reserved, set to 0
                0,  # Reserved, set to 0
                0,  # Reserved, set to 0
                0,  # Reserved, set to 0
                0,  # Reserved, set to 0
                0,  # Reserved, set to 0
            )

            print("Compass calibration canceled.")
        except Exception as e:
            print(f"Failed to cancel compass calibration: {str(e)}")

    def reboot(self) -> None:
        """
        Reboot the drone by sending a reboot command.
        """
        print("Rebooting the drone...")
        try:
            # Send MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN command to reboot
            self.vehicle.mav.command_long_send(
                self.vehicle.target_system,
                self.vehicle.target_component,
                mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN,
                0,
                1,  # 1 for reboot
                0,  # reserved, set to 0
                0,  # reserved, set to 0
                0,  # reserved, set to 0
                0,  # reserved, set to 0
                0,  # reserved, set to 0
                0,  # reserved, set to 0
            )

            # Optionally, you might need to close the connection and reopen it after reboot
            self.vehicle.close()
            print("Drone rebooted. Reconnecting...")
            time.sleep(10)  # Wait for the drone to reboot and reconnect
            self.initialize()  # Reinitialize connection

        except Exception as e:
            print(f"Failed to reboot drone: {str(e)}")
