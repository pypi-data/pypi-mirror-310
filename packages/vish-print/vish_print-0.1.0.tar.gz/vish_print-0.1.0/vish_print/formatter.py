# vish_print/formatter.py
import json

def format_output(*args, format_type=None):
    """
    Format the output based on the format_type.

    Args:
        *args: Objects to format.
        format_type: The type of format (e.g., 'json', 'plain').

    Returns:
        The formatted output as a string.
    """
    # Join the arguments into a single string
    output = " ".join(str(arg) for arg in args)

    if format_type == "json":
        # Convert the output to JSON format
        return json.dumps({"message": output})
    else:
        # Default to plain text
        return output
