# PyWebScraper

A simple web scraper that uses the BeautifulSoup library to scrape the web. This project is still early in development and initially for personal use.

## Features

- Scrape a website content
- Save to a file in Markdown or HTML format
- Image download support

## Dependencies

All dependencies are listed in the requirements.txt file. To install them, run the following command:

```bash
pip install -r requirements.txt
```

List of dependencies:

- beautifulsoup4
- requests
- markdownify

## Installation

To install the package, run the following command:

```bash
pip install .
```

## Usage

### Initialize the PyWebScraper class

```python
from pywebscraper import PyWebScraper

url = 'https://www.example.com'

scraper = PyWebScraper(url)
```

> **Note:**  
> The default output directory is in the output directory.

### Scrape a website content and save to a file in Markdown format

```python
output_file = 'output.md'
scraper.save_markdown(filename=output_file)
```

### Scrape a website content and save to a file in HTML format

```python
output_file = 'output.html'
scraper.save_content_html(filename='content.html')
```

### Scrape a website content and download images

```python
output_file = 'output.md'
scraper.save_markdown(filename=output_file, download_images=True)
```
