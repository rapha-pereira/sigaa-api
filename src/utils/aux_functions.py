"""This module contains string cleaning functions."""

import re


@staticmethod
def remove_newlines_and_tabs(input_string: str) -> str:
    """
    Removes newlines and tabs from the input string.

    Args:
        input_string (str): The string to be cleaned.

    Returns:
        str: The cleaned string with no newlines or tabs.
    """
    cleaned_string = re.sub(r"[\n\t]", "", input_string)
    return cleaned_string
