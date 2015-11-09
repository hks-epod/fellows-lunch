#!/usr/local/bin/python 

"""
PROGRAM: pperish-clean.py
PROGRAMMER: Angela Ambroz, Senior Research and Training Manager, EPoD
DATE: Nov 2015

PURPOSE: 
You might not always want to scrape data from an HTML <table>. Sometimes, you want
to pull all the links from a specific website, or all the articles from a series of
webpages. The principles of scraping remain the same:
1. Identify the top-level page you want to scrape.
2. Identify the HTML tags for the element(s) you want to scrape - and see whether
the tags follow any pattern or logic (e.g. all the same <class=""> or with an <id="">
that makes sense). 
3. Use BeautifulSoup (or another library) to hunt within a webpage for the tags you want.
4. Use csv (or another output library) to output your data into an external file. 

For more info on F(AF)L, see here: http://epod.hmdc.harvard.edu/fellows-lunch/

INPUTS: Rohini, Asim and Rema's websites
OUTPUTS: three giant .txt files of all the text in all their papers

"""

# As usual, import the libraries you need 
import urllib2  						# to open a website and get its HTML
import urllib 							# to save a website as a file
import os 								# to deal with files/folders on your OS
from bs4 import BeautifulSoup 			# to easily loop through HTML tags
from unidecode import unidecode 		# to deal with awful unicode errors


# Pulling the local directory
DIR = os.getcwd()


# This is a dictionary ("dict") of {key: value} pairs. 
# A tutorial on dicts: http://www.tutorialspoint.com/python/python_dictionary.htm
# Dicts are very helpful data storage types. 
# They resemble JSON files. 
# One of their big advantages is that you can nest info within info.
# Here, we've made a dict with three professor "objects": one for Rohini, one for Asim, one for Rema.
# Each professor object has a name, homepage, and 'top'. 
# 'Homepage' is where we find the list of publications.
# 'Top' is where the PDFs of those publications are housed. 
PROFS = [
{'name': 'Rohini', 'homepage': 'http://www.hks.harvard.edu/fs/rpande/research.html', 'top': 'http://www.hks.harvard.edu/fs/rpande/'}, 
{'name': 'Asim', 'homepage': 'http://www.hks.harvard.edu/fs/akhwaja/', 'top': 'http://www.hks.harvard.edu/fs/akhwaja/'},
{'name': 'Rema', 'homepage': 'http://scholar.harvard.edu/remahanna/published-and-forthcoming', 'top': ''}
]


# Get URLs for all papers
def getPapers(url):
	"""
	This multi-line comment is a 'docstring'. It shows up in some automated helpfiles and error messages 
	should this function return an error. 

	This function is called getPapers(), and it takes a URL as its input. It outputs an array of PDF links.

	If you want to see the output, just write "print papers" above the last line below ("return papers"). 
	"""
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	papers = []
	for link in soup.find_all('a'):
		if link.get("href") and "pdf" in link.get("href"):
			papers.append(link.get("href"))
		if link.get("href") and "files" in link.get("href"):
			papers.append(link.get("href"))	
	return papers


# Scrape text from all papers
def stripText(papers, top):
	"""
	This next function, stripText(), 
	"""
	text = []
	for url in papers:
		if url[0:4]!= "http":
			url = top + url

		print url
		
		try:
			urllib2.urlopen(url)
			urllib.urlretrieve(url, DIR + "/paper.pdf")
			
			os.system("pdf2txt.py -o paper.txt -t text paper.pdf")
			raw = open(DIR + "/paper.txt").read()
			text.append(unidecode(raw))

		except:
			print "Problem with opening the URL."

	if os.path.isfile(DIR + "/paper.pdf"):
		os.remove(DIR + "/paper.pdf") 
	if os.path.isfile(DIR + "/paper.txt"):
		os.remove(DIR + "/paper.txt")
	return text


# Create corpus

for pi in PROFS:
	if not os.path.isfile(DIR + "corpi/" + pi["name"] + ".txt"):
		print "Now doing: " + pi['name']
		print "Getting " + pi['name'] + "'s papers..."
		papers = getPapers(pi['homepage'])
		print "Scraping the text from " + pi['name'] + "'s papers..."
		name = pi['name']
		file = open(DIR + "/" + pi['name'] + ".txt", "w")
		strings = stripText(papers, pi['top'])
		print strings[0:5]

		if strings=="":
			file.close()
		else:
			file.write(str(strings))
			file.close()

