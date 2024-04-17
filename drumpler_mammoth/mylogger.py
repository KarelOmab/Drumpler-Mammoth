import logging
from logging.handlers import RotatingFileHandler

class MyLogger:
    _logger = None

    @classmethod
    def get_logger(cls, name='MammothLogger', file_name='mammoth.log', level=logging.DEBUG):
        if cls._logger is None:
            # Create logger
            cls._logger = logging.getLogger(name)
            cls._logger.setLevel(level)

            # Create handlers
            c_handler = logging.StreamHandler()
            f_handler = RotatingFileHandler(file_name, maxBytes=1048576, backupCount=5)

            # Create formatters and add them to handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            c_handler.setFormatter(formatter)
            f_handler.setFormatter(formatter)

            # Add handlers to the logger
            cls._logger.addHandler(c_handler)
            cls._logger.addHandler(f_handler)

        return cls._logger
