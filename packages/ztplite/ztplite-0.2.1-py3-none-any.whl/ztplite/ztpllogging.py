import logging
import sys
from logging import handlers

_script_logger = None


def set_loggers(*args):
    """
    Set loggers for entire module

    :param args: List of logging.Filterers to be logged to. By default this will be FileHandlers and SysLogHandlers
    """
    global _script_logger

    if _script_logger is None:
        _script_logger = logging.getLogger("ztp.logger")
    if args:
        for log_obj in args:
            if log_obj is not None:
                if isinstance(log_obj, logging.handlers.SysLogHandler):
                    log_obj.setLevel(logging.INFO)
                    log_obj.setFormatter(
                        logging.Formatter("%(name)s - %(levelname)s: %(message)s ", "%m/%d/%Y %I:%M:%S %p"))
                    _script_logger.addHandler(log_obj)
                    _script_logger.setLevel(logging.INFO)
                elif isinstance(log_obj, logging.FileHandler):
                    log_obj.setLevel(logging.INFO)
                    log_obj.setFormatter(
                        logging.Formatter("%(levelname)s | %(asctime)s | %(message)s", "%m/%d/%Y %I:%M:%S %p"))
                    _script_logger.addHandler(log_obj)
                    _script_logger.setLevel(logging.INFO)
    else:
        std_out_handler = logging.StreamHandler(sys.stdout)
        std_out_handler.setLevel(logging.INFO)
        std_out_handler.setFormatter(
            logging.Formatter("%(name)s - %(levelname)s: %(message)s ", "%m/%d/%Y %I:%M:%S %p"))
        _script_logger.addHandler(std_out_handler)
        _script_logger.setLevel(logging.INFO)


def get_logger():
    """
    Gets an application logger. Sets a default one if one has not been set yet when this call is made

    :return: A logging object with handlers
    :rtype: logging
    """
    if _script_logger is None:
        set_loggers()
    return _script_logger
