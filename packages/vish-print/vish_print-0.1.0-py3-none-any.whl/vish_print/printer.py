# vish_print/printer.py
import sys
import logging
from .formatter import format_output

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

def print_output(*args, file=None, log=False, format_type=None):
    """
    A more advanced print function with support for logging and formatting.

    Args:
        *args: Objects to print.
        file: Optional file-like object to print to. Default is sys.stdout.
        log: If True, logs the output using logging.
        format_type: Optional format type ("json", "plain", etc.).
    """
    # Convert objects to a formatted string
    output = format_output(*args, format_type=format_type)

    # Print the output to the console or file
    if file:
        print(output, file=file)
    else:
        print(output)

    # Optionally log the output
    if log:
        logger.info(output)
