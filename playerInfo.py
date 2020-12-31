### playerInfo.py
### Scrapes general player information such as age, height, weight, etc.

from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
from datetime import date
from time import strptime
import re

#Scrape general information about a player
#Postcondition: Returns a dictionary of player information
def scrapeInfo(player):

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
	header = soup.find('div',{'itemtype':'https://schema.org/Person'})

	#Store general info in a dictionary
	info = {}
	try:
		info['id'] = re.search('(/......../)', url).group(1).strip('/')
	except: 
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['name'] = header.h1.span.get_text()		
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['position'] = (header.find(text="Position:").parent.next_sibling.split('\n', 1)[0]).strip(" ()',").replace("(", "")	
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['foot'] = (header.find(text="Footed:").parent.next_sibling).lstrip()
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['height'] = int(header.find('span', {'itemprop':'height'}).get_text().split('c')[0])
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['weight'] = int(header.find('span', {'itemprop': 'weight'}).get_text().split('k')[0])
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['dob'] = re.sub(re.compile('(\\n)+( )*'),'',header.find('span',{'itemprop': 'birthDate'}).get_text())
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['cityob'] = header.find('span', {'itemprop':'birthPlace'}).get_text().split(',')[0].split('in ')[1]
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['countryob'] = header.find('span', {'itemprop':'birthPlace'}).get_text().split(',')[1].strip()
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['nt'] = header.find(text = 'National Team:').parent.next_sibling.replace('\xa0','').strip()
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['club'] = header.find('a', {'href':re.compile('(\/squads\/)')}).get_text()
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['age'] = getAge(info['dob'])	#age uses the obsolete <nobr> tag, which it seems BF4 is not recognizing
	except:
		print("playerInfo: scrapeInfo: Exception was raised when trying to scrape player info.")
	try:
		info['name'] = header.h1.span.get_text()		
	except:
		print("Exception was raised when trying to scrape player info.")
	try:
		info['position'] = (header.find(text="Position:").parent.next_sibling.split('\n', 1)[0]).strip(" ()',").replace("(", "")	
	except:
		print("Exception was raised when trying to scrape player info.")
	try:
		info['foot'] = (header.find(text="Footed:").parent.next_sibling).lstrip()
	except:
		print("Exception was raised when trying to scrape player info.")
	try:
		info['height'] = int(header.find('span', {'itemprop':'height'}).get_text().split('c')[0])
	except:
		print("Exception was raised when trying to scrape player info.")
	try:
		info['weight'] = int(header.find('span', {'itemprop': 'weight'}).get_text().split('k')[0])
	except:
		print("Exception was raised when trying to scrape player info.")
	try:
		info['dob'] = re.sub(re.compile('(\\n)+( )*'),'',header.find('span',{'itemprop': 'birthDate'}).get_text())
	except:
		print("Exception was raised when trying to scrape player info.")
	try:
		info['cityob'] = header.find('span', {'itemprop':'birthPlace'}).get_text().split(',')[0].split('in ')[1]
	except:
		print("Exception was raised when trying to scrape player info.")
	try:
		info['countryob'] = header.find('span', {'itemprop':'birthPlace'}).get_text().split(',')[1].strip()
	except:
		print("Exception was raised when trying to scrape player info.")
	try:
		info['nt'] = header.find(text = 'National Team:').parent.next_sibling.replace('\xa0','').strip()
	except:
		print("Exception was raised when trying to scrape player info.")
	try:
		info['club'] = header.find('a', {'href':re.compile('(\/squads\/)')}).get_text()
	except:
		print("Exception was raised when trying to scrape player info.")
	try:
		info['age'] = getAge(info['dob'])	#age uses the obsolete <nobr> tag, which it seems BF4 is not recognizing
	except:
		print("Exception was raised when trying to scrape player info.")

	return info

#Calculate age from DOB
#Postcondition: Returns a value for the age of a player
def getAge(birthdate):

	dobList = birthdate.split() 		#split DOB into [m, d, y]
	birthdateYear = int(dobList[2],10)
	birthdateDay = int(dobList[1].rstrip(','),10)		 #get rid of comma after day, convert to int
	birthdateMonth = strptime(dobList[0][0:3], '%b').tm_mon
	today = date.today()
	age = today.year - birthdateYear - ((today.month, today.day) < (birthdateMonth, birthdateDay))
	
	return age