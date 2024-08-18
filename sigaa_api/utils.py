"""This module contains utilities functions."""

import re
from datetime import datetime, date


def remove_newlines_and_tabs(input_string: str) -> str:
    """
    Removes newlines and tabs from the input string.

    Args:
        input_string (str): The string to be cleaned.

    Returns:
        str: The cleaned string with no newlines or tabs.
    """
    return re.sub(r"[\n\t]", "", input_string)


def clean_paid_workload_string(input_string: str) -> str:
    """
    Cleans the paid workload string.

    Args:
        input_string (str): The string to be cleaned.

    Returns:
        str: The cleaned string with no newlines, tabs,
        leading or trailing spaces and any character that is not a digit.
    """
    # Clean str
    cleaned_str = re.sub(r"[^\d]", "", remove_newlines_and_tabs(input_string)).strip()
    # Number is an integer, but if it's 28, for example, we need to convert it to 0.28
    # If number is 100, we need to convert it to 1.00
    if len(cleaned_str) == 1:
        cleaned_str = f"0.0{cleaned_str}"
    elif len(cleaned_str) == 2:
        cleaned_str = f"0.{cleaned_str}"
    elif len(cleaned_str) == 3:
        cleaned_str = f"{cleaned_str[0]}.{cleaned_str[1:]}"
    return cleaned_str


def convert_semester_to_date(semester_str: str) -> date:
    """
    Converts a semester string in the format 'year.semester' to a date object representing the start date of the semester.

    Args:
        semester_str (str): The semester string in the format 'year.semester'.

    Returns:
        _Date: The start date of the semester as a date object.

    Raises:
        ValueError: If the semester value is invalid. Should be 1 or 2.
    """
    year, semester = map(int, semester_str.split("."))

    if semester == 1:
        start_date = datetime(year, 1, 1).date()
    elif semester == 2:
        start_date = datetime(year, 7, 1).date()
    else:
        raise ValueError("Invalid semester value. Should be 1 or 2.")

    return start_date
