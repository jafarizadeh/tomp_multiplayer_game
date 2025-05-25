from utils.logger import Logger

logger = Logger(name="TEST", log_level="DEBUG", to_file=True, file_path="test.log")

logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warn("This is a warning.")
logger.error("This is an error.")
logger.set_level("WARN")
logger.debug("This debug message should not appear.")
