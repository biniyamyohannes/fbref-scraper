# player_stats.py
"""Functions that scrape player stats."""

from typing import List, Dict
from src.scraper.requests import get_soup


# Scrape player performance statistics from a single page
def scrape_stats(player: str, tables: List[str]) -> List[Dict]:
    """
    Scrapes stats tables for a single player.

    Arguments:
        player       -- A unique player URL path.
        tables       -- List of strings each of which is the name of a table to scrape.
    Returns:
        stats_tables -- A list of dictionaries.
                     -- Each dictionary represents a row of a stats table.
                     -- Every key is a column name and every value is a data point for that column.
    """
    url = f'https://fbref.com{player}'
    soup = get_soup(url)

    stats_tables = []

    # Iterate over the table names that should be scraped
    for table in tables:

        # Find the table tag with the given table name
        stats = soup.find('table', id=table)

        # If the table doesn't exist, move on to the next table
        if stats is None:
            continue

        # Rows is a list of all the <tr> tags in the current table
        rows = stats.find_all(name='tr', id='stats')

        # Iterate over the <tr> tags and extract the data from them
        # Contains all the table cells for a single player/season/club
        for row in rows:

            # Add the table name and primary key attributes (id, season, squad) to the dictionary
            season = row.find(name='th').get_text()
            squad = row.find(name='td', attrs={"data-stat": "squad"}).get_text()
            stat_dict = {'table': table[6:-7], 'id': player[12:20], 'season': season, 'squad': squad}

            # All html table cells in a single table row
            cells = row.find_all(name='td')

            # cell is a single html table cell (a <td> tag)
            for cell in cells:

                # attr_name is the name of the attribute's cell (season, age, etc.)
                attr_name = cell.attrs['data-stat']

                # Skip if attribute is part of the primary key or belongs in the info table
                if attr_name in ['season', 'age', 'squad', 'country', 'comp_level', 'lg_finish', 'matches']:
                    continue

                # Otherwise, add the attribute and its value to the dictionary
                cell_value = cell.get_text()
                stat_dict[attr_name] = cell_value         # add the data point to the dictionary

            # Append the dictionary representing a single row to the list
            stats_tables.append(stat_dict)

    return stats_tables


def get_stats_headers(url: str, tables: List[str]) -> List[List[str]]:
    """
    Extract the column names from all the stats tables.

    Arguments:
        url     -- string containing the player's unique url
        tables  -- list of string, each of which is the name of a table
                -- the column names will be extracted from each table's header
    Returns:
        columns -- A list of string lists. Each list (column[i]) represents a table.
                -- First element of the list (column[i][0]) is the table name.
                -- Remaining elements of the list (column[i][1:]) are the column names.
    """
    url = f'https://fbref.com{url}'
    soup = get_soup(url)

    headers = []

    for table in tables:

        try:
            # Create a header list, append the table name to it
            headers.append([])
            headers[-1].append(table[6:-7])
            header = soup.find('table', {'id': table}).find('th', text="Season")

            # Iterate through the rest of the table header
            while (header := header.find_next_sibling('th')).get_text() != "Matches":
                column = header.attrs['data-stat']

                # Check for duplicates and columns that belong in the info table
                if column in ['age', 'season', 'squad', 'country', 'comp_level', 'lg_finish'] or\
                        any(column in x for x in headers):
                    continue

                # Append all the other columns
                headers[-1].append(column)

        except:
            print('get_stats_headers: Something went wrong trying to scrape columns.')

    headers = [header for header in headers if header != []]

    return headers
