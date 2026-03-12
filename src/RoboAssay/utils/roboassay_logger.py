try:
    from robot.api import logger as rf_logger

    class _RFLogger:
        def __init__(self, name):
            self._name = name

        def info(self, msg):
            rf_logger.info(f"[{self._name}] {msg}")

        def warn(self, msg):
            rf_logger.warn(f"[{self._name}] {msg}")

        def warning(self, msg):
            rf_logger.warn(f"[{self._name}] {msg}")

        def debug(self, msg):
            rf_logger.debug(f"[{self._name}] {msg}")

        def error(self, msg):
            rf_logger.error(f"[{self._name}] {msg}")

    def get_logger(name):
        return _RFLogger(name)

except ImportError:
    import logging

    def get_logger(name):
        logger = logging.getLogger(f"RoboAssay.{name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        return logger
