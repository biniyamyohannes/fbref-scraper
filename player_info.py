# player_info.py
"""Function to scrape the general player information."""

from datetime import date
from time import strptime
import re
from typing import Dict
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup


def get_soup(url: str) -> Dict:
    """
    Fetch the html for the given player URL and return a BeautifulSoup object.

    Arguments:
        url -- player's URL as a string
    """
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                                                      'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
                                        'Accept': 'text/html,application/xhtml+xml,application/xml;'
                                                  'q=0.9,image/webp,*/*;q=0.8'})
    except:
        print("Exception was raised when trying to create a Request object.")
    try:
        html = urlopen(request)
    except:
        print("Exception was raised when trying to open the url request.")
    try:
        return BeautifulSoup(html, 'html.parser')
    except:
        print("Exception was raised when trying to create a soup object from the given html.")
        return None


def scrape_info(player):
    """
    Scrape general information about a player

    Arguments:
        player  -- string part of the URL that identifies a player
    Returns:
        info    -- a dictionary of player information
                -- each key is a column (name, position, etc.)
                -- each value is a data point
    """
    url = f'https://fbref.com{player}'
    soup = get_soup(url)
    header = soup.find('div', {'itemtype': 'https://schema.org/Person'})

    # Store general player info in a dictionary
    info = {}

    # Find the unique player ID
    try:
        info['id'] = re.search('(/......../)', url).group(1).strip('/')
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    # Find the player name
    try:
        info['name'] = header.h1.span.get_text()
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    # Find the player's preferred position(s)
    try:
        info['position'] = (header.find(text="Position:").parent.next_sibling.split('\n', 1)[0])\
            .strip(" ()',").replace("(", "")
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    # Find the player's preferred foot
    try:
        info['foot'] = header.find(text="Footed:").parent.next_sibling.lstrip()
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    # Find player's height
    try:
        info['height'] = int(header.find('span', {'itemprop': 'height'}).get_text().split('c')[0])
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    # Find player's weight
    try:
        info['weight'] = int(header.find('span', {'itemprop': 'weight'}).get_text().split('k')[0])
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    # Find player's date of birth
    try:
        info['dob'] = re.sub(re.compile('(\\n)+( )*'), '', header
                             .find('span', {'itemprop': 'birthDate'}).get_text())
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    # Find player's city of birth
    try:
        info['cityob'] = header.find('span', {'itemprop': 'birthPlace'}) \
        .get_text().split(',')[0].split('in ')[1]
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    # Find player;s country of birth
    try:
        info['countryob'] = header.find('span', {'itemprop': 'birthPlace'}) \
        .get_text().split(',')[1].strip()
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    # Find the national team the player plays for
    try:
        print(header.find(text='National Team:').parent.parent.a.get_text(strip=True))
        info['nt'] = header.find(text='National Team:').parent.parent.a.get_text(strip=True)
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    # Find the club the player currently plays for
    try:
        info['club'] = header.find('a', {'href': re.compile('(\/squads\/)')}).get_text()
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    # Calculate the player's age from his date of birth
    try:
        info['age'] = get_age(info['dob'])
    except:
        print("playerInfo: scrape_info: Exception was raised when trying to scrape player info.")

    return info


def get_age(birthdate: str) -> int:
    """
    # Calculate age from palyer's DOB.

    Arguments:
        birthdate   -- string representing the player's date of birth (m, d, y)
    Returns:
        age         -- player's age in years
    """
    dob_list = birthdate.split()
    birthdate_year = int(dob_list[2], 10)
    birthdate_day = int(dob_list[1].rstrip(','), 10)  # get rid of comma after day, convert to int
    birthdate_month = strptime(dob_list[0][0:3], '%b').tm_mon
    today = date.today()
    age = today.year - birthdate_year - ((today.month, today.day)
                                         < (birthdate_month, birthdate_day))

    return age
