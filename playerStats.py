from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import re


#Create a BS object from a single webpage
url = 'https://fbref.com/en/players/b9fbae28/NGolo-Kante'
request = Request(url, headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
 'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
 'Accept':'text/html,application/xhtml+xml,application/xml;'
 'q=0.9,image/webp,*/*;q=0.8'})
html = urlopen(request)
soup = BeautifulSoup(html, 'html.parser')


#List of desired tables 
tables = [
	'stats_standard_dom_lg',
	'stats_keeper_dom_lg',
	'stats_keeper_adv_dom_lg',
	'stats_shooting_dom_lg',
	'stats_passing_dom_lg',
	'stats_passing_types_dom_lg',
	'stats_gca_dom_lg',
	'stats_defense_dom_lg',
	'stats_possession_dom_lg',
	'stats_playing_time_dom_lg',
	'stats_misc_dom_lg',
	]

season = '2019-2020'

#Scrape player performance statistics from a single page 
def scrapeStats(soup, tables):
	statDict = {}

#Standard stats table
	header = soup.find('table', {'id':tables[0]}).find('th', text="Season")
	cell = soup.find('table', {'id':tables[0]}).find('th', text=season)
	statDict[header.get_text()] = cell.get_text()
	while (header.find_next_sibling('th').get_text() != "Matches"):
			header = header.find_next_sibling('th')
			cell = cell.find_next_sibling('td')
			if header.get_text() in statDict:
				try:
					statDict[header.get_text() +  '/90']= cell.get_text()
				except KeyError:
					statDict[header.get_text()] = cell.get_text()
			else:
				statDict[header.get_text()] = cell.get_text()

#Rest of the tables
	for i in range(len(tables)-1):
		header = soup.find('table', {'id':tables[i+1]}).find('th', text="Season")
		cell = soup.find('table', {'id':tables[i+1]}).find('th', text=season)
		statDict[header.get_text()] = cell.get_text()
		while (header.find_next_sibling('th').get_text() != "Matches"):
			header = header.find_next_sibling('th')
			cell = cell.find_next_sibling('td')
			statDict[header.get_text()] = cell.get_text()
	return cleanStats(statDict)


#Format
def cleanStats(statDict):
	try:
		statDict['G+A/90'] = statDict.pop('G+A')
		statDict['G-PK/90'] = statDict.pop('G-PK')
		statDict['G+A-PK/90'] = statDict.pop('G+A-PK')
		statDict['xG+xA/90'] = statDict.pop('xG+xA')
		statDict['npxG+xA/90'] = statDict.pop('npxG+xA')
	except KeyError:
		print('playerStats: cleanStats: Key Error occured.')
	except:
		print('Something else went wrong.')
	return statDict

def getStatsHeader(url, tables):
	#Fetch the html
	url = 'https://fbref.com{}'.format(url)
	try:
		request = Request(url, headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
		'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
		'Accept':'text/html,application/xhtml+xml,application/xml;'
		'q=0.9,image/webp,*/*;q=0.8'})
	except: 
		print("playerInfo: scrapeInfo: Exception was raised when trying to create a Request object.")
	try:
		html = urlopen(request)
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to open the url request.")
		print("Exception was raised when trying to create a Request object.")
	try:
		html = urlopen(request)
	except:
		print("Exception was raised when trying to open the url request.")

	soup = BeautifulSoup(html, 'html.parser')

	#Columns of the first table (needs special loop because it has duplicate columns)
	columns = [[]]
	header = soup.find('table', {'id':tables[0]}).find('th', text="Season") #find the first column
	columns.append(header.get_text())
	while (header.find_next_sibling('th').get_text() != "Matches"):
		header = header.find_next_sibling('th')
		if header.get_text() in columns[0]:
			columns[0].append(header.get_text() +  '/90')
		else:
			columns[0].append(header.get_text())

	#Rest of the tables
	for i in range(1, len(tables)):
		try:
			header = soup.find('table', {'id':tables[i]}).find('th', text="Season")
			columns.append([])
			while (header.find_next_sibling('th').get_text() != "Matches"):
				header = header.find_next_sibling('th')
				columns[i].append(header.get_text())
		except:
			print("playeStats: getStatsHeader: Column not found.")
			print(tables[i])

	return columns


"""
stats = scrapeStats(soup, tables)
print(stats)
print('\n' + 'Number of keys: ' + str(len(stats)))
"""