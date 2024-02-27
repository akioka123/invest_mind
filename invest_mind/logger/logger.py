import logging
import logging.handlers


class AppLogger:
    def __init__(self, method_name):
        """Initializes the logger object with the method name.

        Args:
            method_name (str): 呼び出したメソッド名
        """

        self.logger = logging.getLogger(method_name)
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        self.file_handler = logging.handlers.RotatingFileHandler(
            "./logs/invest_mind.log", maxBytes=1048576, backupCount=5
        )
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def debug(self, message: str):
        """Logs the debug message.

        Args:
            message (str): デバッグメッセージ
        """
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug(message)

    def info(self, message: str):
        """Logs the info message.

        Args:
            message (str): 情報メッセージ
        """
        self.logger.setLevel(logging.INFO)
        self.logger.info(message)

    def warning(self, message: str):
        """Logs the warning message.

        Args:
            message (str): 警告メッセージ
        """
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(message)

    def error(self, message: str):
        """Logs the error message.

        Args:
            message (str): エラーメッセージ
        """
        self.logger.setLevel(logging.ERROR)
        self.logger.error(message)
