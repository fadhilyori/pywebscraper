import pytest
from pywebscraper.utils import validate_url, is_relative_url


@pytest.mark.parametrize('url', [
    "https://www.google.com",
    "https://www.google.com/search?q=python",
    "https://example.com",
])
def test_validate_url_with_valid_url(url):
    try:
        validate_url(url)
    except ValueError:
        pytest.fail("validate_url() raised ValueError unexpectedly!")

@pytest.mark.parametrize('url', [
    # Invalid URL
    "http:google.com",
    "example",
    "ftp://example.com",

    # Unreachable URL
    "https://www.example.com/invalid_url",

    # Empty URL
    "",
])
def test_validate_url_with_invalid_url(url):
    with pytest.raises(ValueError):
        validate_url("invalid_url")


@pytest.mark.parametrize('url', [
    "/search",
    "#section",
    "?q=python",
    "/search?q=python",
])
def test_is_relative_url_with_relative_url(url):
    assert is_relative_url(url) == True

@pytest.mark.parametrize('url', [
    "https://example.com/search",
    "http://example.com/#section",
    "http://example.com/?q=python",
    "http://example.com/search?q=python",
])
def test_is_relative_url_with_absolute_url(url):
    assert is_relative_url(url) == False
