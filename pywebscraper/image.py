import os
from dataclasses import dataclass
from typing import Any

import requests

from pywebscraper.utils import validate_url


@dataclass
class ImageContent:
    """
    A simple class to store image content and its metadata.

    Attributes:
        url (str): The URL of the image.
        alt_text (str): The alt text of the image.
        local_path (str): The local path of the saved image if it's already saved. Default is None.
    """

    url: str
    alt_text: str
    local_path: str | None = None

    def __post_init__(self):
        # Validate the URL
        validate_url(self.url)

    def get_filename(self) -> str:
        """
        Get the image file name based on the URL.

        Example:
            - https://example.com/image.jpg -> image.jpg
            - https://example.com/path/to/image.jpg -> image.jpg
            - https://example.com/many/dir/path/to/image.jpg?size=large -> image.jpg

        Returns:
            str: The image file name.
        """
        return self.url.split("/")[-1].split("?")[0]

    def get_filepath(self) -> str:
        """
        Get the full image file path based on the URL except the domain name. without query parameters.

        Example:
            - https://example.com/image.jpg -> image.jpg
            - https://example.com/path/to/image.jpg -> path/to/image.jpg
            - https://example.com/many/dir/path/to/image.jpg?size=large -> many/dir/path/to/image.jpg

        Returns:
            str: The image file path.
        """
        return "/".join(self.url.split("/")[3:]).split("?")[0]

    def _download(self) -> bytes | None | Any:
        """Downloads the image content from the URL."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image {self.url}: {e}")

    def save(self, path: str = "output/images/", use_subdirectories: bool = True) -> str:
        """
        Saves the image content to a file.

        Args:
            path (str): The directory path to save the image. Default is "output/images/".
            use_subdirectories (bool): If True, the image will be saved in subdirectories based on the URL path. Default is True.

        Returns:
            str: The path to the saved image.
        """
        if use_subdirectories:
            filename = self.get_filepath()
        else:
            filename = self.get_filename()

        full_path = os.path.join(path, filename)
        base_path = os.path.dirname(full_path)

        # Create the directory if it doesn't exist
        if not os.path.exists(base_path):
            os.makedirs(base_path, exist_ok=True)

        image_content = self._download()

        with open(full_path, "wb") as f:
            f.write(image_content)
        print(f"Image saved to {full_path}")

        self.local_path = full_path

        # Return the path to the saved image
        return full_path
