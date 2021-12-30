# requests.py
"""Contains the functions for making HTML requests and creating BeautifulSoup objects."""

import re
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from typing import List
from bs4 import BeautifulSoup

def get_soup(url: str) -> BeautifulSoup:
    """
    Fetch the html for the given player URL and return a BeautifulSoup object.

    Arguments:
        url -- player's URL path as a string
    """
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                                                          'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
                                            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                                                      'q=0.9,image/webp,*/*;q=0.8'})
    except ValueError as e:
        print("requests: get_soup: ", e)
        return None

    try:
        html = urlopen(request)
    except (ValueError, URLError) as e:
        print("requests: get_soup: ", e)
        return None
    
    try:
        return BeautifulSoup(html, 'html.parser')
    except Exception as e:
        print("requests: get_soup: ", e)
        return None


def get_squads(league: str) -> List[str]:
    """
    Crawl a league page and collect all team URLs.

    Arguments:
         league -- single URL of a league

    Returns:
        List of strings. Each string is a unique team URL.
    """
    url = f'https://fbref.com{league}'
    soup = get_soup(url)

    links = []

    for link in soup.find("table").find_all('a', href=re.compile('(\/squads\/)')):
        links.append(link.attrs['href'])

    return links


def get_players(squad: str) -> List[str]:
    """
    Crawl a team page and collect all player URLs.

    Arguments:
         squad -- single URL of a league

    Returns:
        List of strings. Each string is a unique player URL.
    """
    url = f'https://fbref.com{squad}'
    soup = get_soup(url)

    links = []

    for link in soup.find("table").find_all('a', href=re.compile('(\/players\/)(.){9}(?!(matchlogs))')):
        links.append(link.attrs['href'])

    return links
