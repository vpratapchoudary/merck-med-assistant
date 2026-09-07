import logging

def log_config(name: str = __name__) -> logging.Logger:
    """
    Configures the logging settings for the application.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(name)