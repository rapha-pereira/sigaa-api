"""This module contains string cleaning functions."""

import re


@staticmethod
def remove_newlines_and_tabs(input_string: str) -> str:
    cleaned_string = re.sub(r"[\n\t]", "", input_string)
    return cleaned_string
