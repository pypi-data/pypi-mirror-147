"""
Object value parsing and validation functions.
"""

import string

NAME_OKAY = string.ascii_letters + string.digits + "-_"


def body(text):
    """
    Return a text body with trimmed whitespace.
    """

    return text.strip() + "\n"


def name(text):
    """
    Return a lowercase name string without punctuation.
    """

    text = str(text).strip().lower()
    return "".join(char for char in text if char in NAME_OKAY)
