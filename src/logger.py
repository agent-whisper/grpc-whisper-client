import sys
from loguru import logger


logger.remove(0)
_logger_id = logger.add(sys.stderr, level="DEBUG")


# Configure logger sinks here
def set_logger_level(level):
    global _logger_id
    logger.remove(_logger_id)
    _logger_id = logger.add(sys.stderr, level=level)
