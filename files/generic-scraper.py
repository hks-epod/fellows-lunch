#!/usr/local/bin/python 

"""
PROGRAM: generic-scraper.py
PROGRAMMER: Angela Ambroz, Senior Research and Training Manager, EPoD
DATE: Nov 2015

PURPOSE: 
This is an example web scraper for the F(AF)L workshop on Python web scraping. 
I'm going to pull the table of episodes of Mr. Robot (a TV show everyone says
I should watch) from its Wiki page, and output a simple csv. 

For more info on F(AF)L, see here: http://epod.hmdc.harvard.edu/fellows-lunch/

INPUTS: This table: https://en.wikipedia.org/wiki/Mr._Robot_%28TV_series%29#Episodes
OUTPUTS: the same table, as "Mr Robot - Spoilers.csv"

"""

# We start by importing the modules we'll need
import csv 										# for reading/writing CSV files
import os 										# for reading/making folder ts 
import urllib2 									# for opening webpages
from bs4 import BeautifulSoup 					# BeautifulSoup! For easy parsing of websites
 

# Setting some globals
URL = "https://en.wikipedia.org/wiki/Mr._Robot_%28TV_series%29"
DIR = os.getcwd()								# a relative reference to the directory we're in


# Defining a function to parse a website
# into a bunch of objects
def Souping(url):
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	return soup

# We use that function to parse the Mr. Robot wiki
topPage = Souping(URL)

# We use BeautifulSoup's method, .find(), to find 
# all HTML elements with the class "wikitable"
table = topPage.find(class_="wikitable")

# We can now use BeautifulSoup's method, .find_all(), 
# to find all <tr> elements in the "wikitable" table
rows = table.find_all("tr")

# Let's pull the header out (these are <th> elements)
# Note: We're using Pythons' lovely LIST COMPREHENSION
# functionality. More here: http://blog.teamtreehouse.com/python-single-line-loops
header = [row.find_all("th") for row in rows]

# The WikiTable has two <th> rows; we only want the first one
header = header[0]

# And we DON'T want the first element ("No.")
header.pop(0)

# Another list comprehension, now grabbing all <td> elements 
# in each <tr>.
datarows = [row.find_all("td") for row in rows]


# We're ready to export to CSV! Let's start a WITH statement.
# This opens a file, does stuff to it, and closes it at the end
# of the with statement. 

# Here, we create a .csv called "Mr Robot - spoilers" and put it in
# our current directory.
with open(DIR + "/Mr Robot - spoilers.csv", "w") as f:
	
	# We're using the csv module's method, .writer() to write to a CSV file
	csvwriter = csv.writer(f)

	# If you look at the wiki table (https://en.wikipedia.org/wiki/Mr._Robot_%28TV_series%29#Episodes),
	# you'll see that the summary text comes in the row BELOW the other info. Here, we're moving
	# it up. So, anytime we see a row with only one element (if len(row) == 1), then we'll add that 
	# element to the previous row (datarows[index - 1].extend(row)). Then we delete it (datarows.pop(index)).
	for index, row in enumerate(datarows):
		if len(row) == 1:
			datarows[index - 1].extend(row)
		datarows.pop(index)

	# Let's add in the header row, at the top.
	datarows.insert(0, header)

	# If you look at each row (print datarows), you'll see we've got a bunch of HTML code. 
	# BeautifulSoup offers an easy way to strip all that down to just the text.
	# Here, we loop through each cell of each row, strip out just the text (point.getText().encode("utf-8"))
	# and then create a new row (newrow) we'll then write to the CSV. 
	for i, row in enumerate(datarows):

		newrow = []

		for point in row:
			text = point.getText().encode("utf-8")
			newrow.append(text)	

		# Writing each new row to a row in the new csv
		csvwriter.writerow(newrow)


# And we're done!

