import re
from typing import List
from urllib.parse import urlparse

import pyperclip
from prompt_toolkit.validation import ValidationError


def parse_clipboard() -> List[str]:
    """
    Parse the clipboard contents to extract list of items.

    Returns:
    List[str]: A list of cleaned and normalized strings.
    """
    contents = pyperclip.paste()
    return parse_string(contents)


def parse_user_input(contents: str) -> List[str]:
    """
    Parse the input string to extract list of items.

    Args:
    content (str): The string containing items separated by commas.

    Returns:
    List[str]: A list of cleaned and normalized strings.
    """
    return parse_string(contents)


def parse_file(file_path: str) -> List[str]:
    """
    Parse the input string to extract list of items, handling alphanumerics,
    commas, spaces, newlines, hyphens, ampersands, parentheses, and periods.

    Args:
    content (str): The string containing items separated by commas.

    Returns:
    List[str]: A list of cleaned and normalized strings.
    """
    # Make the assumption that the file exists and the path is valid
    with open(file_path, "r") as file:
        contents = file.read()
    return parse_string(contents)


def parse_string(contents: str) -> List[str]:
    """
    Parse the input string to extract list of items.

    Args:
    content (str): The string containing items separated by commas.

    Returns:
    List[str]: A list of cleaned and normalized strings.
    """
    # Normalize: remove newlines and extra spaces, lowercase the string
    normalized_content = re.sub(r"\s+", " ", contents.replace("\n", " ")).lower()

    # Split by commas
    items = normalized_content.split(",")

    # Trim spaces from each item
    items = [item.strip() for item in items if item.strip()]

    return items


def is_valid_url(input_url: str) -> bool:
    """
    Validate the input string to check if it's a well-formed URL.

    Args:
    input_url (str): URL entered by the user.

    Returns:
    bool: True if the URL is valid, otherwise False.
    """
    parsed_url = urlparse(input_url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)


def validate_url(input_url: str):
    """
    Validator function for InquirerPy that raises a ValidationError
    if the URL is not valid.

    Args:
    input_url (str): URL entered by the user.

    Raises:
    ValidationError: If the URL is invalid.
    """
    if not is_valid_url(input_url):
        raise ValidationError(
            message="Please enter a valid URL. Example: http://www.example.com"
        )
