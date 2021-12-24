# crawler.py
"""Driver program. Iterates over Leagues, Squads, and Players
 and stores their information into a database."""

import time
from typing import List
import database as db
from requests import get_players, get_squads
from player_info import scrape_info
from player_stats import get_stats_headers, scrape_stats

# List of leagues to crawl
LEAGUES = [
    '/en/comps/12/La-Liga-Stats',
    '/en/comps/13/Ligue-1-Stats',
    '/en/comps/9/Premier-League-Stats',
    '/en/comps/20/Bundesliga-Stats',
    '/en/comps/11/Serie-A-Stats'
]

# List of tables to collect per player
TABLES = [
    'stats_keeper_dom_lg',
    'stats_keeper_adv_dom_lg',
    'stats_standard_dom_lg',
    'stats_shooting_dom_lg',
    'stats_passing_dom_lg',
    'stats_passing_types_dom_lg',
    'stats_gca_dom_lg',
    'stats_defense_dom_lg',
    'stats_possession_dom_lg',
    'stats_playing_time_dom_lg',
    'stats_misc_dom_lg',
]

def crawl(leagues: List[str]) -> None:
    """
    Iteratively crawl a list of soccer leagues and scrape player data.
    Scrapes all teams in a league and all players in a team.

    Arguments:
         leagues -- list of URLs of soccer leagues to scrape
    """
    # A player used to determine the format of the stats tables
    # (needs to be a goalkeeper since they have all the tables necessary)
    PLAYER = '/en/players/1840e36d/Thibaut-Courtois'

    player_tables = get_stats_headers(PLAYER, TABLES)

    db.create_info_table()
    db.create_stats_tables(player_tables)

    for league in leagues:
        for squad in get_squads(league):
            for player in get_players(squad):
                player_info = scrape_info(player)
                print(player_info)
                db.add_info(player_info)
                db.add_stats(scrape_stats(player, TABLES))
                print("Sleep for 2 seconds.\n")
                time.sleep(2.0)


if __name__ == "__main__":
    crawl(LEAGUES)
