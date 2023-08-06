import os
from datetime import datetime


class Logger:
    def __init__(self, log_file_name):
        # »»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»
        # Declares the log folder path and creates the folder if it
        # doesn't exist
        # »»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»
        self.logs_folder_path = "logs"
        if not os.path.exists("logs"):
            os.makedirs("logs")

        # »»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»
        # Opens the correct logfile or creates one if it doesn't exist
        # »»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»
        self.log_file = open(f"logs/{log_file_name}.txt", "a")
        self.log_file.write(f"###############################################################\n")
        self.log_file.write(f"[{datetime.now().strftime('%d/%m/%Y at %H:%M:%S')}]\n[LOGGER INITIALIZED]\n")
        self.log_file.write(f"###############################################################\n")
        self.log_file.flush()

    def log_info(self, message):
        self.log_file.write(f"[{datetime.now().strftime('%d/%m/%Y at %H:%M:%S')} | INFO   ]: {message}\n")
        self.log_file.flush()

    def log_warning(self, message):
        self.log_file.write(f"[{datetime.now().strftime('%d/%m/%Y at %H:%M:%S')} | WARNING]: {message}\n")
        self.log_file.flush()

    def log_error(self, message):
        self.log_file.write(f"[{datetime.now().strftime('%d/%m/%Y at %H:%M:%S')} | ERROR  ]: {message}\n")
        self.log_file.flush()
