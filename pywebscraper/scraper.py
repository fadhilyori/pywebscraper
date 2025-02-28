import os
from typing import Sequence

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from pywebscraper.image import ImageContent
from pywebscraper.utils import write_to_file, validate_url, clear_directory_content


class PyWebScraper:
    """
    A simple web scrapper for extracting content and images from a webpage.

    Attributes:
        url (str): The URL of the webpage.

    Methods:
        extract_content: Extracts the main content from the webpage.
        extract_images: Extracts image URLs from the webpage.
        get_images: Downloads and returns image content.
        get_content_html: Extracts the main content and returns it as HTML.
    """

    url: str
    _soup: BeautifulSoup
    _content: BeautifulSoup = None
    _images: Sequence[ImageContent] = None

    def __init__(self, url: str):
        """
        Initializes the WebScraper object with a URL.

        Args:
            url (str): The URL of the webpage.

        Raises:
            ValueError: If the URL is invalid or empty.
        """

        # Validate the URL
        validate_url(url)

        self.url = url
        html = self._fetch_html()
        self._soup = BeautifulSoup(html, "html.parser")

    def _fetch_html(self) -> str | None:
        """
        Fetches HTML content from the URL.

        Returns:
            str | None: The HTML content of the webpage. None if an error occurs.
        """
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the webpage: {e}")
            return None

    def extract_content(self) -> BeautifulSoup:
        """
        Extracts main content from HTML.

        Returns:
            BeautifulSoup: The main content of the webpage.
        """
        content = self._soup.find("article") or self._soup.find("div", {"class": "content"}) or self._soup.body

        self._content = content if content else self._soup.body

        return self._content

    def extract_images(self) -> list:
        """
        Extracts image URLs from the HTML content.

        Returns:
            list: A list of image URLs
        """
        images = []
        for img in self._soup.find_all("img"):
            img_url = img.get("src")
            alt_text = img.get("alt", "Image")
            if img_url:
                images.append((alt_text, img_url))
        return images

    def get_images(self) -> Sequence[ImageContent]:
        """
        Extracts image content from the HTML content.

        Returns:
            Sequence[ImageContent]: A sequence of ImageContent objects.
        """

        if self._images is not None:
            return self._images

        self._images = [ImageContent(url, alt_text) for alt_text, url in self.extract_images()]

        return self._images

    def get_content_html(self) -> str:
        """
        Extracts the main content from the HTML and returns it as a string in HTML format.

        Returns:
            str: The main content of the webpage in HTML format.
        """
        content = self.extract_content()
        return str(content)

    def get_full_html(self) -> str:
        """
        Returns the full HTML content of the webpage.

        Returns:
            str: The full HTML content of the webpage.
        """
        return str(self._soup)

    def get_content_markdown(self, heading_style: str = "ATX") -> str:
        """
        Extracts the main content from the HTML and returns it as a string in Markdown format.

        Args:
            heading_style (str): The style for rendering headings in Markdown.
                Possible values: ATX (default), ATX_CLOSED, SETEXT, and UNDERLINED

        Returns:
            str: The main content of the webpage in Markdown format.
        """
        content = self.extract_content()
        return md(str(content), heading_style=heading_style)

    def save_images(self, path: str = "output/images"):
        """
        Downloads and saves all images from the webpage.

        Args:
            path (str): The directory path to save the images. Default is "output/images".
        """
        images = self.get_images()

        for image in images:
            image.save(path=path)

    def _process_images(
            self,
            content: str,
            path: str = "output",
            images_dir_name: str = "images",
            flatten_images: bool = False
    ) -> str:
        """
        Downloads and saves images from the webpage and updates the content with local image paths.

        Args:
            content (str): The content of the webpage.
            path (str): The directory path for base output. Default is "output".
            images_dir_name (str): The name of the directory to save images. Default is "images".
            flatten_images (bool): Whether to save all images in single directory instead of subdirectories. Default is False.

        Returns:
            str: The updated content with local image paths.
        """

        save_path = os.path.join(path, images_dir_name)
        images = self.get_images()

        # Check if images have already saved locally
        for image in images:
            if not image.local_path:
                image.save(path=save_path, use_subdirectories=not flatten_images)

            content = content.replace(image.url, image.local_path.replace(path, ""))

        return content

    def save_markdown(
            self,
            path: str = "output",
            filename: str = "index.md",
            download_images: bool = False,
            images_dir_name: str = "images",
            clear_output_dir: bool = False,
            flatten_images: bool = False
    ):
        """
        Saves the main content of the webpage as a Markdown file. Optionally downloads images.

        Args:
            path (str): The path to save the Markdown file. Default is "output".
            filename (str): The name of the Markdown file. Default is "index.md".
            download_images (bool): Whether to download images from the webpage. Default is False.
            images_dir_name (str): The name of the directory to save images. Default is "images".
            clear_output_dir (bool): Whether to clear the output directory before saving. Default is False.
            flatten_images (bool): Whether to save all images in single directory instead of subdirectories. Default is False.
        """

        if clear_output_dir:
            clear_directory_content(path)
            print("Output directory cleared.")

        content: str = self.get_content_markdown()

        if download_images:
            content = self._process_images(
                content,
                path=path,
                images_dir_name=images_dir_name,
                flatten_images=flatten_images
            )

        file_path = write_to_file(content, path=path, filename=filename)
        print(f"Markdown content saved to {file_path}")

    def save_content_html(
            self,
            path: str = "output",
            filename: str = "index.html",
            download_images: bool = False,
            images_dir_name: str = "images",
            clear_output_dir: bool = False,
            flatten_images: bool = False
    ):
        """
        Saves the main content of the webpage as an HTML file. Optionally downloads images.

        Args:
            path (str): The path to save the HTML file. Default is "output".
            filename (str): The name of the HTML file. Default is "index.html".
            download_images (bool): Whether to download images from the webpage. Default is False.
            images_dir_name (str): The name of the directory to save images. Default is "images".
            clear_output_dir (bool): Whether to clear the output directory before saving. Default is False.
            flatten_images (bool): Whether to save all images in single directory instead of subdirectories. Default is False.
        """

        if clear_output_dir:
            clear_directory_content(path)
            print("Output directory cleared.")

        content: str = self.get_content_html()

        if download_images:
            content = self._process_images(
                content,
                path=path,
                images_dir_name=images_dir_name,
                flatten_images=flatten_images
            )

        file_path = write_to_file(content, path=path, filename=filename)
        print(f"HTML content saved to {file_path}")
