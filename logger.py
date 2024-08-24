# def log_message(message: str, folder_path: str) -> None:
#     """
#     Logs a message to a file.

#     Parameters
#     ----------
#         message (dict):
#             The type of the ROS message.
#         message (str):
#             The content of the ROS message.
#         time (str):
#             The timestamp of the ROS message.
#         filepath (str):
#             The path to the log file.
#     """
#     file_path = os.path.join(folder_path, datetime.date.today().strftime("%Y-%m-%d") + ".txt")

#     folder = os.path.dirname(file_path)
#     if not os.path.exists(folder):
#         os.makedirs(folder)

#     if not os.path.exists(file_path):
#         open(file_path, 'w').close()

#     time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
#     with open(file_path, 'a') as file:
#         file.write(f"Time: {time} | {message_type} | Channel: {channel} | Message: {message}\n")
