import re
from typing import List, Dict
from requests import get_soup

SEASON = '2020-2021'


# Scrape player performance statistics from a single page
def scrape_stats(player: str, tables: List[str]) -> List[Dict]:
    """
    Scrapes stats tables for a single player.

    Arguments:
        player    -- A unique player URL path.
        tables    -- List of strings each of which is the name of a table to scrape.
    Returns:
        all_dicts -- A list of dictionaries.
                  -- Each dictionary represents a stats table.
                  -- Every key is a column and every value is a data point for that column.
    """
    url = 'https://fbref.com{}'.format(player)
    soup = get_soup(url)

    all_tables = []

    for table in tables:

        stats = soup.find('table', {'id': table})

        if stats != None:
            all_tables.append(dict())
            stat_dict = dict()
            stat_dict['table'] = table[6:-7]
            stat_dict['id'] = re.search('(/......../)', url).group(1).strip('/')
            cell = stats.find('tr', {'id': 'stats'})

            if cell != None:  # if the table exists
                attr_name = cell.attrs['data-stat']
                if any(attr_name in dictionary for dictionary in all_tables) or (
                        attr_name in ['age', 'country', 'comp_level', 'lg_finish']):  # first cell
                    pass
                else:
                    stat = cell.get_text()
                    if (',' in stat):
                        stat = stat.replace(',', '')
                    try:
                        stat_dict[attr_name] = float(stat)
                    except ValueError:
                        stat_dict[attr_name] = stat
                while (cell.find_next_sibling('td').get_text() != "Matches"):  # rest of the cells
                    cell = cell.find_next_sibling('td')
                    attr_name = cell.attrs['data-stat']
                    if any(attr_name in dictionary for dictionary in all_tables) or (
                            attr_name in ['age', 'country', 'comp_level', 'lg_finish']):
                        continue
                    else:
                        stat = cell.get_text()
                        if (',' in stat):
                            stat = stat.replace(',', '')
                        try:
                            stat_dict[attr_name] = float(stat)
                        except ValueError:
                            stat_dict[attr_name] = stat

    all_tables = [all_tables[i] for i in range(len(all_tables)) if len(all_tables[i]) != 1]

    for dictionary in all_tables:
        print(dictionary)

    return all_tables


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

    columns = []

    for table in tables:

        try:
            # Create a column list, append table name to it
            columns.append([])
            columns[-1].append(table[6:-7])
            header = soup.find('table', {'id': table}).find('th', text="Season")

            # Iterate through the rest of the table header
            while (header := header.find_next_sibling('th')).get_text() != "Matches":
                column = header.attrs['data-stat']

                # Check for duplicates and columns that belong in the info table
                if any(column in x for x in columns) or \
                        column in ['age', 'season', 'squad', 'country', 'comp_level', 'lg_finish']:
                    continue

                # Append all the other columns
                columns[-1].append(column)

        except:
            print('get_stats_headers: Something went wrong trying to scrape columns.')

    columns = [header for header in columns if header != []]

    return columns
