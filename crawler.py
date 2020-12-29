### crawler.py 
### Driver script.
### Iterates over Leagues, Squads and Players and stores their information into a database.


from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import database as db
import playerInfo as pi
import playerStats as ps
import time
import re

leagues = ['https://fbref.com/en/comps/12/La-Liga-Stats',
		   'https://fbref.com/en/comps/13/Ligue-1-Stats',
		   'https://fbref.com/en/comps/9/Premier-League-Stats',
		   'https://fbref.com/en/comps/20/Bundesliga-Stats',
		   'https://fbref.com/en/comps/11/Serie-A-Stats']


def crawl(leagues):
    header = ['name', 'position', 'foot', 'height', 'weight', 'dob', 'cityob', 'countryob', 'nt', 'club', 'age']
    outfield_tables = ps.getStatsHeader(getPlayers(getSquads(leagues[0])[0])[0], ps.tables)
    keeper_tables = ps.getStatsHeader(getPlayers(getSquads(leagues[0])[0])[1], ps.tables)
    db.createInfoTable(header)
    db.createStatsTables(outfield_tables)
    db.createStatsTables(keeper_tables)

    for league in leagues:
        for squad in getSquads(league):
            for player in getPlayers(squad):
                print(pi.scrapeInfo(player))
                db.addInfo(pi.scrapeInfo(player))
                print("Sleep for 2 seconds.\n")
                time.sleep(2.0)


def getSquads(league):
	request = Request(league, headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
	 'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
	 'Accept':'text/html,application/xhtml+xml,application/xml;'
	 'q=0.9,image/webp,*/*;q=0.8'})
	html = urlopen(request)
	soup = BeautifulSoup(html, 'html.parser')
	links = []
	for link in soup.find("table").find_all('a', href=re.compile('(\/squads\/)')):
		links.append(link.attrs['href'])
	return links
	

def getPlayers(squad):
	request = Request('https://fbref.com{}'.format(squad), headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
	 'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
	 'Accept':'text/html,application/xhtml+xml,application/xml;'
	 'q=0.9,image/webp,*/*;q=0.8'})
	html = urlopen(request)
	soup = BeautifulSoup(html, 'html.parser')
	links = []
	for link in soup.find("table").find_all('a', href = re.compile('(\/players\/)(.){9}(?!(matchlogs))')):
		links.append(link.attrs['href'])	
	return links

crawl(leagues)