import logging
import os


class Logger:
    def __init__(self, name, level=logging.INFO, log_file=None):
        if not log_file:
            log_file = os.path.join(os.getcwd(), "coauthor.log")
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        self.log_file = log_file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def clean_log_file(self):
        if self.log_file and os.path.exists(self.log_file):
            os.remove(self.log_file)
            print(f"Log file '{self.log_file}' has been removed.")

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    # def exception(self, msg):
    #     self.logger.exception(msg)
