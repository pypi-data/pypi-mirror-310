import logging
import sys
from pathlib import Path

def setup_logging(level=logging.INFO, log_file=None):
    # Create your application's logger
    logger = logging.getLogger('openapi_agent')  # Use your app's namespace
    logger.setLevel(level)
    
    # Remove any existing handlers
    logger.handlers = []
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if log_file specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

def get_logger(name):
    # Always return a child of your app's logger
    return logging.getLogger(f'openapi_agent.{name}')