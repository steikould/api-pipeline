import logging
import json
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Sets up the logger for the pipeline."""
    logger = logging.getLogger("api_pipeline")
    logger.setLevel(logging.INFO)

    # Create a file handler that logs to a file
    handler = RotatingFileHandler("api_pipeline.log", maxBytes=1024 * 1024, backupCount=3)

    # Create a JSON formatter
    formatter = logging.Formatter(
        json.dumps(
            {
                "timestamp": "%(asctime)s",
                "level": "%(levelname)s",
                "message": "%(message)s",
            }
        )
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
