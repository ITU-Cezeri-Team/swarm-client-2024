import os
import datetime


def log_incoming_message(message: dict, folder_path: str) -> None:
    """
    Logs an incoming message to a file.

    Parameters
    ----------
        message (dict):
            The message as dictionary.
        filepath (str):
            The path to the log file.
    """
    file_path = os.path.join(
        folder_path, "INCOMING", datetime.date.today().strftime("%Y-%m-%d") + ".txt"
    )

    folder = os.path.dirname(file_path)
    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(file_path):
        open(file_path, "w").close()

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    with open(file_path, "a") as file:
        file.write(f"Time: {time} | Message: {message}\n")


def log_outgoing_message(message: dict, folder_path: str) -> None:
    """
    Logs an outgoing message to a file.

    Parameters
    ----------
        message (dict):
            The message as dictionary.
        filepath (str):
            The path to the log file.
    """
    file_path = os.path.join(
        folder_path, "OUTGOING", datetime.date.today().strftime("%Y-%m-%d") + ".txt"
    )

    folder = os.path.dirname(file_path)
    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(file_path):
        open(file_path, "w").close()

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    with open(file_path, "a") as file:
        file.write(f"Time: {time} | Message: {message}\n")
