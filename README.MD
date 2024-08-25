### Steps to Set Up Raspberry Pi for Running `main.py`

#### 1. Install the Raspberry Pi OS
   - Download the Raspberry Pi Imager from the [official website](https://www.raspberrypi.org/software/).
   - Use the Raspberry Pi Imager to flash the Raspberry Pi OS onto an SD card.
   - Insert the SD card into your Raspberry Pi and power it on.

#### 2. Enable SSH and Serial Port
   - Once the Raspberry Pi boots, log in with the default credentials (Username: `pi`, Password: `raspberry`).
   - Run the configuration tool:
     ```bash
     sudo raspi-config
     ```
   - **Enable SSH:**
     - Navigate to `Interface Options` > `SSH` and enable it.
   - **Enable Serial Port:**
     - Navigate to `Interface Options` > `Serial Port`.
     - Disable the login shell over serial and enable the serial port hardware.

   - Reboot the Raspberry Pi to apply the changes:
     ```bash
     sudo reboot
     ```

#### 3. Install Necessary Libraries
   - After rebooting, install the required libraries using `apt-get`:
     ```bash
     sudo apt-get update
     sudo apt-get install -y python3-pip python3-pymavlink python3-paho-mqtt
     ```
   - If you encounter issues with system packages, you can use the `--break-system-packages` option:
     ```bash
     sudo apt-get install --break-system-packages python3-xyz
     ```

#### 4. Clone the Repository
   - Navigate to the directory where you want to clone the repository:
     ```bash
     cd ~
     ```
   - Clone the repository from GitHub:
     ```bash
     git clone https://github.com/ITU-Cezeri-Team/swarm-client-2024.git
     ```

#### 5. Run the `main.py` Script
   - Change directory to the cloned repository:
     ```bash
     cd swarm-client-2024
     ```
   - Run the `main.py` script using Python:
     ```bash
     python3 main.py
     ```

This guide should help you set up your Raspberry Pi to run the `main.py` script from the specified repository, including enabling SSH and the serial port, installing necessary libraries, and executing the script.
