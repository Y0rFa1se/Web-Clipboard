import logging

class Logger:

    @classmethod
    def configure(cls, SETTINGS):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        file_handler = logging.FileHandler(SETTINGS["LOG_FILE"])
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        cls.logger = logging.getLogger()
        cls.logger.setLevel(logging.DEBUG)

        cls.logger.addHandler(console_handler)
        cls.logger.addHandler(file_handler)

    @staticmethod
    def debug(message):
        Logger.logger.debug(message)

    @staticmethod
    def info(message):
        Logger.logger.info(message)

    @staticmethod
    def warning(message):
        Logger.logger.warning(message)

    @staticmethod
    def error(message):
        Logger.logger.error(message)

    @staticmethod
    def critical(message):
        Logger.logger.critical(message)