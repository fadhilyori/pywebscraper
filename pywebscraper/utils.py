import os
import shutil

import requests


def validate_url(url: str):
    """
    Validates the URL.

    Args:
        url (str): The URL to validate.

    Raises:
        ValueError: If the URL is empty, invalid, or unreachable
    """
    # Check if the URL is empty
    if not url:
        raise ValueError("URL cannot be empty.")

    # Check if the URL is valid
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("Invalid URL. It must start with 'http://' or 'https://'.")

    # Check if the URL is reachable
    try:
        response = requests.head(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"The URL is unreachable {url}: {e}")


def write_to_file(content: str, path: str, filename: str) -> str:
    """
    Writes the content to a file.

    Args:
        content (str): The content to write to the file.
        path (str): The path to save the file.
        filename (str): The name of the file.

    Returns:
        str: The full path to the saved file.
    """
    filepath = os.path.join(path, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath

def clear_directory_content(path: str):
    """
    Clears the content of a directory.

    Args:
        path (str): The path to the directory.
    """
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
