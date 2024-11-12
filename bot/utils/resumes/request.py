import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


class SiteServerError(Exception):
    """Exception for server error from the site."""


class InvalidResponse(Exception):
    """Exception for invalid response from GET request to the site."""


def get_soup_by_(url: str) -> BeautifulSoup:
    """Returns BeautifulSoup object from the given url."""
    response = _get_response_from_(url)
    return BeautifulSoup(response.text, "lxml")


def _get_response_from_(url: str) -> requests.Response:
    """Returns response or raises an exception for the given url."""
    response = requests.get(
        url.strip(), headers={"user-agent": generate_user_agent().strip()}
    )
    if response.status_code >= 500:
        raise SiteServerError(
            f"Server error from the site ({response.status_code}):\n{url=}"
        )
    elif not response.ok:
        raise InvalidResponse(
            f"Not OK server response from the site ({response.status_code}):"
            f"\n{url=}"
        )
    return response
