from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import re

season = '2020-2021'

# Scrape player performance statistics from a single page 
def scrape_stats(player, tables):
	#Fetch the html
	url = 'https://fbref.com{}'.format(player)
	try:
		request = Request(url, headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
		'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
		'Accept':'text/html,application/xhtml+xml,application/xml;'
		'q=0.9,image/webp,*/*;q=0.8'})
	except: 
		print("playerInfo: scrape_info: Exception was raised when trying to create a Request object.")
	try:
		html = urlopen(request)
	except:
		print("playerInfo: scrape_info: Exception was raised when trying to open the url request.")

	soup = BeautifulSoup(html, 'html.parser')

	tables[0], tables[1], tables[2] = tables[1], tables[2], tables[0] 							#FIX/GET RID OF THIS
	all_dicts = []

	for i in range(0, len(tables)):
		
		table = soup.find('table', {'id':tables[i]})
		all_dicts.append(dict())
		stat_dict = all_dicts[i]
		stat_dict['table'] = tables[i][6:-7] # stats_keeper_dom_lg
		
		if table != None:
			stat_dict['id'] = re.search('(/......../)', url).group(1).strip('/')
			cell = table.find('th', text=season)
			if cell != None:			#if the table exists
				attr_name = cell.attrs['data-stat']
				if any(attr_name in dictionary for dictionary in all_dicts) or (attr_name in ['age','squad', 'country', 'comp_level', 'lg_finish']):			# first cell
					pass
				else:
					stat = cell.get_text()
					if (',' in stat):
						stat = stat.replace(',','')
					try:
						stat_dict[attr_name] = float(stat)
					except ValueError:
						stat_dict[attr_name] = stat
				while (cell.find_next_sibling('td').get_text() != "Matches"):			# rest of the cells
					cell = cell.find_next_sibling('td')
					attr_name = cell.attrs['data-stat']
					if any(attr_name in dictionary for dictionary in all_dicts) or (attr_name in ['age','squad', 'country', 'comp_level', 'lg_finish']):
						continue
					else:
						stat = cell.get_text()
						if (',' in stat):
							stat = stat.replace(',','')
						try:
							stat_dict[attr_name] = float(stat)
						except ValueError:
							stat_dict[attr_name] = stat
	
	all_dicts = [all_dicts[i] for i in range(len(all_dicts)) if len(all_dicts[i]) != 1]

	for dictionary in all_dicts:
		print(dictionary)

	return all_dicts

def get_stats_header(url, tables):

	#Fetch the html
	url = 'https://fbref.com{}'.format(url)
	try:
		request = Request(url, headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
		'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
		'Accept':'text/html,application/xhtml+xml,application/xml;'
		'q=0.9,image/webp,*/*;q=0.8'})
	except: 
		print("playerInfo: scrape_info: Exception was raised when trying to create a Request object.")
	try:
		html = urlopen(request)
	except:
		print("get_stats_header: scrape_info: Exception was raised when trying to open the url request.")
		print("Exception was raised when trying to create a Request object.")

	soup = BeautifulSoup(html, 'html.parser')
	columns = [[]]

	# Columns of the general goalkeeping table have to be added manually because bf4 search didn't work
	if soup.find('table', {'id':tables[0]}) != None:
		columns[0].append(tables[0][6:-7])
		gk_columns = ['goals_against_gk',
					  'goals_against_per90_gk',
					  'shots_on_target-against',
					  'saves', 
					  'save_pct',
					  'wins_gk',
					  'draws_gk',
					  'losses_gk',
					  'clean_sheets',
					  'clean_sheets_pct',
					  'pens_att_gk',
					  'pens_allowed',
					  'pens_saved',
					  'pens_missed_gk']
		for i in range(len(gk_columns)):
			columns[0].append(gk_columns[i])

	# Other tables
	for i in range(1, len(tables)):
		try:
			columns.append([])	
			header = soup.find('table', {'id':tables[i]}).find('th', text="Season") #find the first column			
			columns[i].append(tables[i][6:-7])									
			while (header.find_next_sibling('th').get_text() != "Matches"):
				header = header.find_next_sibling('th')
				if any(header.attrs['data-stat'] in column for column in columns) or (header.attrs['data-stat'] in ['age','squad', 'country', 'comp_level', 'lg_finish']):
					pass
				else:
					columns[i].append(header.attrs['data-stat'])
		except:
			print('get_stats_header: Something went wrong trying to scrape columns.')

	columns = [columns[i] for i in range(len(columns)) if columns[i] != []]

	return columns