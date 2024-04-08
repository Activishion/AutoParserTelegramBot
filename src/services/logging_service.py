import logging

from logging.handlers import RotatingFileHandler

from settings.config import settings


class AplicationLogging:
    """
    The class is responsible for collecting and processing logs of 
    the entire application in the required time.
    """

    @staticmethod
    def init_error_logger() -> logging.Logger:
        error_log = logging.getLogger('error_logger')
        error_log.setLevel(logging.ERROR)
        error_log_handler = RotatingFileHandler(
            settings.DIRECTORY_ERROR_LOG,
            maxBytes=1000000,
            backupCount=100
        )
        error_log_formatter = logging.Formatter(
            settings.LOG_FORMAT,
            datefmt=settings.LOG_DATE_FORMAT
        )
        error_log_handler.setFormatter(error_log_formatter)
        error_log.addHandler(error_log_handler)
        return error_log

    @staticmethod
    def init_static_logger() -> logging.Logger:
        static_log = logging.getLogger('static_logger')
        static_log.setLevel(logging.INFO)
        static_log_handler = RotatingFileHandler(
            settings.DIRECTORY_STATIC_LOG,
            maxBytes=1000000,
            backupCount=100
        )
        static_log_formatter = logging.Formatter(
            settings.LOG_FORMAT,
            datefmt=settings.LOG_DATE_FORMAT
        )
        static_log_handler.setFormatter(static_log_formatter)
        static_log.addHandler(static_log_handler)
        return static_log
    

error_log = AplicationLogging.init_error_logger()
static_log = AplicationLogging.init_static_logger()
