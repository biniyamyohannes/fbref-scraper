import re
from typing import List
from crawler import get_soup

season = '2020-2021'


# Scrape player performance statistics from a single page
def scrape_stats(player, tables):
    """

    :param player:
    :param tables:
    :return:
    """
    url = 'https://fbref.com{}'.format(player)
    soup = get_soup(url)

    tables[0], tables[1], tables[2] = tables[1], tables[2], tables[0]  # FIX/GET RID OF THIS
    all_dicts = []

    for i in range(0, len(tables)):

        table = soup.find('table', {'id': tables[i]})
        all_dicts.append(dict())
        stat_dict = all_dicts[i]
        stat_dict['table'] = tables[i][6:-7]  # stats_keeper_dom_lg

        if table != None:
            stat_dict['id'] = re.search('(/......../)', url).group(1).strip('/')
            cell = table.find('th', text=season)
            if cell != None:  # if the table exists
                attr_name = cell.attrs['data-stat']
                if any(attr_name in dictionary for dictionary in all_dicts) or (
                        attr_name in ['age', 'squad', 'country', 'comp_level', 'lg_finish']):  # first cell
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
                    if any(attr_name in dictionary for dictionary in all_dicts) or (
                            attr_name in ['age', 'squad', 'country', 'comp_level', 'lg_finish']):
                        continue
                    else:
                        stat = cell.get_text()
                        if (',' in stat):
                            stat = stat.replace(',', '')
                        try:
                            stat_dict[attr_name] = float(stat)
                        except ValueError:
                            stat_dict[attr_name] = stat

    all_dicts = [all_dicts[i] for i in range(len(all_dicts)) if len(all_dicts[i]) != 1]

    for dictionary in all_dicts:
        print(dictionary)

    return all_dicts


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
            # Create a column list, append table name and season columns
            columns.append([])
            columns[-1].append(table[6:-7])
            header = soup.find('table', {'id': table}).find('th', text="Season")
            columns[-1].append(header.attrs['data-stat'])

            # Iterate through the rest of the table header
            while (header := header.find_next_sibling('th')).get_text() != "Matches":
                column = header.attrs['data-stat']

                # Check for duplicates and columns that belong in the info table
                if any(column in x for x in columns) or \
                        column in ['age', 'squad', 'country', 'comp_level', 'lg_finish']:
                    continue

                # Append all the other columns
                columns[-1].append(column)

        except:
            print('get_stats_headers: Something went wrong trying to scrape columns.')

    columns = [header for header in columns if header != []]

    return columns
