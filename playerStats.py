from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import re

season = '2020-2021'

# Scrape player performance statistics from a single page 
def scrapeStats(player, tables):
	#Fetch the html
	url = 'https://fbref.com{}'.format(player)
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

	tables[0], tables[2] = tables[2], tables[0] 							#FIX/GET RID OF THIS
	all_dicts = []

	for i in range(0, len(tables)):
		
		table = soup.find('table', {'id':tables[i]})
		all_dicts.append(dict())
		stat_dict = all_dicts[i]
		stat_dict['table'] = tables[i]
		
		if table != None:
			stat_dict['id'] = re.search('(/......../)', url).group(1).strip('/')
			cell = table.find('th', text=season)
			attr_name = cell.attrs['data-stat']
			if cell != None:
				while (cell.find_next_sibling('td').get_text() != "Matches"):
					cell = cell.find_next_sibling('td')
					attr_name = cell.attrs['data-stat']
					if any(attr_name in dictionary for dictionary in all_dicts):
						pass
					else:
						try:
							stat_dict[attr_name] = float(cell.get_text())
						except ValueError:
							#print("Not a number.")
							stat_dict[attr_name] = cell.get_text()
	
	all_dicts = [all_dicts[i] for i in range(len(all_dicts)) if len(all_dicts[i]) != 1]

	for dictionary in all_dicts:
		print(dictionary)

	return all_dicts

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
		print("getStatsHeader: scrapeInfo: Exception was raised when trying to open the url request.")
		print("Exception was raised when trying to create a Request object.")
	try:
		html = urlopen(request)
	except:
		print("Exception was raised when trying to open the url request.")

	soup = BeautifulSoup(html, 'html.parser')
	columns = [[]]

	# Columns of the general goalkeeping table have to be added manually because bf4 search didn't work
	if soup.find('table', {'id':tables[0]}) != None:
		columns[0].append(tables[0])
		gk_columns = ['season', 'age', 'squad', 'country', 'comp_level', 'lg_finish', 'games', 'games_starts', 'minutes', 'GA', 'GA90', 'SoTA', 'Saves', 'Save%', 'W', 'D', 'L', 'CS', 'CS%', 'PKatt', 'PKA', 'PKsv', 'PKm']
		for i in range(len(gk_columns)):
			columns[0].append(gk_columns[i])

	# Other tables
	for i in range(1, len(tables)):
		try:
			columns.append([])	
			header = soup.find('table', {'id':tables[i]}).find('th', text="Season") #find the first column			
			columns[i].append(tables[i])									
			while (header.find_next_sibling('th').get_text() != "Matches"):
				header = header.find_next_sibling('th')
				if any(header.attrs['data-stat'] in column for column in columns):
					pass
				else:
					columns[i].append(header.attrs['data-stat'])
		except:
			print('getStatsHeader: Something went wrong trying to scrape columns.')

	columns = [columns[i] for i in range(len(columns)) if columns[i] != []]

	return columns