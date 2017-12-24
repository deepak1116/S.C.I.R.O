import os
import sqlite3
import operator
from collections import OrderedDict
import matplotlib.pyplot as plt

def parse(url):
	try:
		parsed_url_components = url.split('//')
		sublevel_split = parsed_url_components[1].split('/', 1)
		domain = sublevel_split[0].replace("www.", "")
		return domain
	except IndexError:
		print("URL format error! url = {}".format(url))

def analyze(results):

	prompt = input("[.] Type <c> to print or <p> to plot\n[>] ")

	if prompt.lower() == "c":
		for site, count in list(sites_count_sorted.items()):
			print(site, count)
	elif prompt.lower() == "p":
		plt.bar(list(range(len(results))), list(results.values()), align='edge')
		plt.xticks(rotation=45)
		plt.xticks(list(range(len(results))), list(results.keys()))
		plt.show()
	else:
		print("[.] Uh?")
		analyze (sites_count_sorted)

#path to user's history database (Chrome)
data_path = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\\User Data\Profile 1"
files = os.listdir(data_path)

history_db = os.path.join(data_path, 'history')

#connection
c = sqlite3.connect(history_db)
cursor = c.cursor()

#list all tables
#list_tables = "SELECT name FROM sqlite_master WHERE type='table';"
#cursor.execute(list_tables)
#print cursor.fetchall()

#url and visit counts
try:
	select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
	cursor.execute(select_statement)
except sqlite3.OperationalError:
	print("[!] The database is locked! Please exit Chrome and run the script again.")
	quit()

results = cursor.fetchall() #tuple

sites_count = {} #to iterate easier

for url, count in results:
	url = parse(url)
	if url in sites_count:
		sites_count[url] += 1
	else:
		sites_count[url] = 1

sites_count_sorted = OrderedDict(sorted(list(sites_count.items()), key=operator.itemgetter(1), reverse=True))

analyze (sites_count_sorted)