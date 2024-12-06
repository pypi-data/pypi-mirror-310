import logging
from datetime import datetime

def setup_logger(log_file="machine_id.log"):
    """
    Set up a logger for the package.

    Args:
        log_file (str): The file where logs will be written.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("machine_id_logger")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def format_response(data, success=True):
    """
    Format a standardized API response.

    Args:
        data (dict): Data to include in the response.
        success (bool): Whether the response indicates success.

    Returns:
        dict: Formatted response.
    """
    return {
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
    }

def validate_command(command):
    """
    Validate the command list for job execution.

    Args:
        command (list): Command to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(command, list):
        raise ValueError("Command must be a list of strings.")
    if not command:
        raise ValueError("Command cannot be empty.")
    if not all(isinstance(c, str) for c in command):
        raise ValueError("All command elements must be strings.")
    return True
