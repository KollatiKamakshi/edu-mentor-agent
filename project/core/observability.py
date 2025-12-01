import logging
import sys

def setup_logging(level=logging.INFO):
    """Sets up a centralized, structured logging system."""

    # Check if handler already exists to prevent duplicate output in notebooks
    if logging.getLogger().hasHandlers():
        return

    logger = logging.getLogger()
    logger.setLevel(level)

    # Console Handler
    c_handler = logging.StreamHandler(sys.stdout)
    c_handler.setLevel(level)

    # Formatter for structured logs
    formatter = logging.Formatter(
        '[%(levelname)s] [%(name)s] (%(asctime)s) - %(message)s',
        datefmt='%H:%M:%S'
    )
    c_handler.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(c_handler)
    logger.info("Observability system initialized.")

# Initialize logging immediately upon import
setup_logging()
