
     #########  ##############  #######
    ##     ##  ##    ##    ##  ##
   ##     ##  ##    ##    ##  #######
  ##     ##  ##    ##    ##       ##
 ##     ##  ##    ##    ##  #######
 
# NOS to Teletext converter
# Demo by Nathan Dane for Max de Vos, 2025
# Copyright free, do what you like & have fun with it :)

# Start by importing all the libraries we need
import newsreel_werkend
import Eredivisie_uitslagen
import Eerste_divisie
import feedparser
from bs4 import BeautifulSoup
import lxml
import cchardet
import copy

from textBlock import toTeletextBlock
from page import exportTTI, loadTTI
from legaliser import pageLegaliser

# Load the template page for the header & footer
newsPageTemplate = loadTTI("news_page.tti")

# How many news pages do we want to create?
maxPages = 10
startPage = 102

# Download and parse an RSS Feed of news from NOS
newsData = feedparser.parse("https://feeds.nos.nl/nosnieuwsalgemeen")

# Initialise a Page Counter
pageNum = 0

# Create a headlines list for P101
headlines = []

# Loop through each news story to produce pages
for newsArticle in newsData['entries']:
	# Set the first line we write on
	line = 5
	
	# Create a new teletext page
	teletextPage = {"number":(pageNum + startPage),"subpages":[{"packets":copy.deepcopy(newsPageTemplate["subpages"][0]["packets"])}]}
	
	# Create the title
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"yellow","text":newsArticle["title"]}]}]},
		line = line
	)
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add the title to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	# NOS provides news within the RSS feed, encoded as HTML
	# So we use BeautifulSoup to extract the HTML
	NOSSoup = BeautifulSoup(newsArticle['summary'], "lxml")
	NOSResults = NOSSoup.find_all('p')
	
	for paragraph in NOSResults:
		# Create a teletext paragraph
		paraBlock = toTeletextBlock(
			input = {"content":[{"align":"left","content":[{"colour":"white","text":paragraph.text}]}]},
			line = line
		)
		
		# Is this going to make the page too long?
		if (len(paraBlock) + line) > 22:
			break
		
		# Move on the line pointer
		line += (len(paraBlock) + 1)
		
		# Add this paragraph to the teletext page
		teletextPage["subpages"][0]["packets"] += paraBlock
	
	# Export the final page
	# We run it through "legaliser", this fixes the accented characters, but may be wrong for your country!
	exportTTI(pageLegaliser(teletextPage))
	
	headlines.append({"title":newsArticle["title"],"number":str(pageNum + startPage)})
	
	# Iterate the page counter
	pageNum += 1
	
	# Stop when we have enough pages
	if pageNum > maxPages:
		break

# Next we create P101, the headlines
# Start by loading the template
newsIndexTemplate = loadTTI("news_index.tti")

# Create a page
teletextPage = {"number":101,"subpages":[{"packets":copy.deepcopy(newsIndexTemplate["subpages"][0]["packets"])}]}

line = 5

for headline in headlines:
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"white","text":headline["title"]}]},{"align":"right","content":[{"colour":"yellow","text":headline["number"]}]}]},
		line = line
	)
	
	# Is this going to make the page too long?
	if (len(paraBlock) + line) > 22:
		break
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add this paragraph to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	exportTTI(pageLegaliser(teletextPage))
# Load the template page for the header & footer
newsPageTemplate = loadTTI("news_page.tti")

# How many news pages do we want to create?
maxPages = 10
startPage = 201

# Download and parse an RSS Feed of news from NOS
newsData = feedparser.parse("https://feeds.nos.nl/nossportalgemeen")

# Initialise a Page Counter
pageNum = 0

# Create a headlines list for P101
headlines = []

# Loop through each news story to produce pages
for newsArticle in newsData['entries']:
	# Set the first line we write on
	line = 5
	
	# Create a new teletext page
	teletextPage = {"number":(pageNum + startPage),"subpages":[{"packets":copy.deepcopy(newsPageTemplate["subpages"][0]["packets"])}]}
	
	# Create the title
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"yellow","text":newsArticle["title"]}]}]},
		line = line
	)
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add the title to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	# NOS provides news within the RSS feed, encoded as HTML
	# So we use BeautifulSoup to extract the HTML
	NOSSoup = BeautifulSoup(newsArticle['summary'], "lxml")
	NOSResults = NOSSoup.find_all('p')
	
	for paragraph in NOSResults:
		# Create a teletext paragraph
		paraBlock = toTeletextBlock(
			input = {"content":[{"align":"left","content":[{"colour":"white","text":paragraph.text}]}]},
			line = line
		)
		
		# Is this going to make the page too long?
		if (len(paraBlock) + line) > 22:
			break
		
		# Move on the line pointer
		line += (len(paraBlock) + 1)
		
		# Add this paragraph to the teletext page
		teletextPage["subpages"][0]["packets"] += paraBlock
	
	# Export the final page
	# We run it through "legaliser", this fixes the accented characters, but may be wrong for your country!
	exportTTI(pageLegaliser(teletextPage))
	
	headlines.append({"title":newsArticle["title"],"number":str(pageNum + startPage)})
	
	# Iterate the page counter
	pageNum += 1
	
	# Stop when we have enough pages
	if pageNum > maxPages:
		break

# Next we create P101, the headlines
# Start by loading the template
newsIndexTemplate = loadTTI("news_index.tti")

# Create a page
teletextPage = {"number":200,"subpages":[{"packets":copy.deepcopy(newsIndexTemplate["subpages"][0]["packets"])}]}

line = 5

for headline in headlines:
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"white","text":headline["title"]}]},{"align":"right","content":[{"colour":"yellow","text":headline["number"]}]}]},
		line = line
	)
	
	# Is this going to make the page too long?
	if (len(paraBlock) + line) > 22:
		break
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add this paragraph to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	exportTTI(pageLegaliser(teletextPage))
# Load the template page for the header & footer
newsPageTemplate = loadTTI("news_page.tti")

# How many news pages do we want to create?
maxPages = 10
startPage = 181

# Download and parse an RSS Feed of news from NOS
newsData = feedparser.parse("https://feeds.nos.nl/jeugdjournaal")

# Initialise a Page Counter
pageNum = 0

# Create a headlines list for P101
headlines = []

# Loop through each news story to produce pages
for newsArticle in newsData['entries']:
	# Set the first line we write on
	line = 5
	
	# Create a new teletext page
	teletextPage = {"number":(pageNum + startPage),"subpages":[{"packets":copy.deepcopy(newsPageTemplate["subpages"][0]["packets"])}]}
	
	# Create the title
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"yellow","text":newsArticle["title"]}]}]},
		line = line
	)
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add the title to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	# NOS provides news within the RSS feed, encoded as HTML
	# So we use BeautifulSoup to extract the HTML
	NOSSoup = BeautifulSoup(newsArticle['summary'], "lxml")
	NOSResults = NOSSoup.find_all('p')
	
	for paragraph in NOSResults:
		# Create a teletext paragraph
		paraBlock = toTeletextBlock(
			input = {"content":[{"align":"left","content":[{"colour":"white","text":paragraph.text}]}]},
			line = line
		)
		
		# Is this going to make the page too long?
		if (len(paraBlock) + line) > 22:
			break
		
		# Move on the line pointer
		line += (len(paraBlock) + 1)
		
		# Add this paragraph to the teletext page
		teletextPage["subpages"][0]["packets"] += paraBlock
	
	# Export the final page
	# We run it through "legaliser", this fixes the accented characters, but may be wrong for your country!
	exportTTI(pageLegaliser(teletextPage))
	
	headlines.append({"title":newsArticle["title"],"number":str(pageNum + startPage)})
	
	# Iterate the page counter
	pageNum += 1
	
	# Stop when we have enough pages
	if pageNum > maxPages:
		break


# Next we create P101, the headlines
# Start by loading the template
newsIndexTemplate = loadTTI("news_index.tti")

# Create a page
teletextPage = {"number":180,"subpages":[{"packets":copy.deepcopy(newsIndexTemplate["subpages"][0]["packets"])}]}

line = 5

for headline in headlines:
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"white","text":headline["title"]}]},{"align":"right","content":[{"colour":"yellow","text":headline["number"]}]}]},
		line = line
	)
	
	# Is this going to make the page too long?
	if (len(paraBlock) + line) > 22:
		break
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add this paragraph to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	exportTTI(pageLegaliser(teletextPage))

# Next we create P101, the headlines
# Start by loading the template
newsIndexTemplate = loadTTI("news_index.tti")

# Create a page
teletextPage = {"number":600,"subpages":[{"packets":copy.deepcopy(newsIndexTemplate["subpages"][0]["packets"])}]}

line = 5

for headline in headlines:
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"white","text":headline["title"]}]},{"align":"right","content":[{"colour":"yellow","text":headline["number"]}]}]},
		line = line
	)
	
	# Is this going to make the page too long?
	if (len(paraBlock) + line) > 22:
		break
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add this paragraph to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	exportTTI(pageLegaliser(teletextPage))
# Load the template page for the header & footer
newsPageTemplate = loadTTI("news_page.tti")

# How many news pages do we want to create?
maxPages = 10
startPage = 221

# Download and parse an RSS Feed of news from NOS
newsData = feedparser.parse("https://feeds.nos.nl/nosvoetbal")

# Initialise a Page Counter
pageNum = 0

# Create a headlines list for P101
headlines = []

# Loop through each news story to produce pages
for newsArticle in newsData['entries']:
	# Set the first line we write on
	line = 5
	
	# Create a new teletext page
	teletextPage = {"number":(pageNum + startPage),"subpages":[{"packets":copy.deepcopy(newsPageTemplate["subpages"][0]["packets"])}]}
	
	# Create the title
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"yellow","text":newsArticle["title"]}]}]},
		line = line
	)
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add the title to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	# NOS provides news within the RSS feed, encoded as HTML
	# So we use BeautifulSoup to extract the HTML
	NOSSoup = BeautifulSoup(newsArticle['summary'], "lxml")
	NOSResults = NOSSoup.find_all('p')
	
	for paragraph in NOSResults:
		# Create a teletext paragraph
		paraBlock = toTeletextBlock(
			input = {"content":[{"align":"left","content":[{"colour":"white","text":paragraph.text}]}]},
			line = line
		)
		
		# Is this going to make the page too long?
		if (len(paraBlock) + line) > 22:
			break
		
		# Move on the line pointer
		line += (len(paraBlock) + 1)
		
		# Add this paragraph to the teletext page
		teletextPage["subpages"][0]["packets"] += paraBlock
	
	# Export the final page
	# We run it through "legaliser", this fixes the accented characters, but may be wrong for your country!
	exportTTI(pageLegaliser(teletextPage))
	
	headlines.append({"title":newsArticle["title"],"number":str(pageNum + startPage)})
	
	# Iterate the page counter
	pageNum += 1
	
	# Stop when we have enough pages
	if pageNum > maxPages:
		break

# Next we create P101, the headlines
# Start by loading the template
newsIndexTemplate = loadTTI("news_index.tti")

# Create a page
teletextPage = {"number":220,"subpages":[{"packets":copy.deepcopy(newsIndexTemplate["subpages"][0]["packets"])}]}

line = 5

for headline in headlines:
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"white","text":headline["title"]}]},{"align":"right","content":[{"colour":"yellow","text":headline["number"]}]}]},
		line = line
	)
	
	# Is this going to make the page too long?
	if (len(paraBlock) + line) > 22:
		break
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add this paragraph to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	exportTTI(pageLegaliser(teletextPage))
# Load the template page for the header & footer
newsPageTemplate = loadTTI("news_page.tti")

# How many news pages do we want to create?
maxPages = 10
startPage = 161
# Download and parse an RSS Feed of news from NOS
newsData = feedparser.parse(" https://www.omroepwest.nl/rss/bollenstreek.xml ")

# Initialise a Page Counter
pageNum = 0

# Create a headlines list for P101
headlines = []

# Loop through each news story to produce pages
for newsArticle in newsData['entries']:
	# Set the first line we write on
	line = 5
	
	# Create a new teletext page
	teletextPage = {"number":(pageNum + startPage),"subpages":[{"packets":copy.deepcopy(newsPageTemplate["subpages"][0]["packets"])}]}
	
	# Create the title
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"yellow","text":newsArticle["title"]}]}]},
		line = line
	)
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add the title to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	# NOS provides news within the RSS feed, encoded as HTML
	# So we use BeautifulSoup to extract the HTML
	NOSSoup = BeautifulSoup(newsArticle['summary'], "lxml")
	NOSResults = NOSSoup.find_all('p')
	
	for paragraph in NOSResults:
		# Create a teletext paragraph
		paraBlock = toTeletextBlock(
			input = {"content":[{"align":"left","content":[{"colour":"white","text":paragraph.text}]}]},
			line = line
		)
		
		# Is this going to make the page too long?
		if (len(paraBlock) + line) > 22:
			break
		
		# Move on the line pointer
		line += (len(paraBlock) + 1)
		
		# Add this paragraph to the teletext page
		teletextPage["subpages"][0]["packets"] += paraBlock
	
	# Export the final page
	# We run it through "legaliser", this fixes the accented characters, but may be wrong for your country!
	exportTTI(pageLegaliser(teletextPage))
	
	headlines.append({"title":newsArticle["title"],"number":str(pageNum + startPage)})
	
	# Iterate the page counter
	pageNum += 1
	
	# Stop when we have enough pages
	if pageNum > maxPages:
		break

# Next we create P101, the headlines
# Start by loading the template
newsIndexTemplate = loadTTI("news_index.tti")

# Create a page
teletextPage = {"number":160,"subpages":[{"packets":copy.deepcopy(newsIndexTemplate["subpages"][0]["packets"])}]}

line = 5

for headline in headlines:
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"white","text":headline["title"]}]},{"align":"right","content":[{"colour":"yellow","text":headline["number"]}]}]},
		line = line
	)
	
	# Is this going to make the page too long?
	if (len(paraBlock) + line) > 22:
		break
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add this paragraph to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	exportTTI(pageLegaliser(teletextPage))
# Load the template page for the header & footer
newsPageTemplate = loadTTI("news_page.tti")

# How many news pages do we want to create?
maxPages = 10
startPage = 241
# Download and parse an RSS Feed of news from NOS
newsData = feedparser.parse(" https://feeds.nos.nl/nossportformule1 ")

# Initialise a Page Counter
pageNum = 0

# Create a headlines list for P101
headlines = []

# Loop through each news story to produce pages
for newsArticle in newsData['entries']:
	# Set the first line we write on
	line = 5
	
	# Create a new teletext page
	teletextPage = {"number":(pageNum + startPage),"subpages":[{"packets":copy.deepcopy(newsPageTemplate["subpages"][0]["packets"])}]}
	
	# Create the title
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"yellow","text":newsArticle["title"]}]}]},
		line = line
	)
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add the title to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	# NOS provides news within the RSS feed, encoded as HTML
	# So we use BeautifulSoup to extract the HTML
	NOSSoup = BeautifulSoup(newsArticle['summary'], "lxml")
	NOSResults = NOSSoup.find_all('p')
	
	for paragraph in NOSResults:
		# Create a teletext paragraph
		paraBlock = toTeletextBlock(
			input = {"content":[{"align":"left","content":[{"colour":"white","text":paragraph.text}]}]},
			line = line
		)
		
		# Is this going to make the page too long?
		if (len(paraBlock) + line) > 22:
			break
		
		# Move on the line pointer
		line += (len(paraBlock) + 1)
		
		# Add this paragraph to the teletext page
		teletextPage["subpages"][0]["packets"] += paraBlock
	
	# Export the final page
	# We run it through "legaliser", this fixes the accented characters, but may be wrong for your country!
	exportTTI(pageLegaliser(teletextPage))
	
	headlines.append({"title":newsArticle["title"],"number":str(pageNum + startPage)})
	
	# Iterate the page counter
	pageNum += 1
	
	# Stop when we have enough pages
	if pageNum > maxPages:
		break

# Next we create P101, the headlines
# Start by loading the template
newsIndexTemplate = loadTTI("news_index.tti")

# Create a page
teletextPage = {"number":240,"subpages":[{"packets":copy.deepcopy(newsIndexTemplate["subpages"][0]["packets"])}]}

line = 5

for headline in headlines:
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"white","text":headline["title"]}]},{"align":"right","content":[{"colour":"yellow","text":headline["number"]}]}]},
		line = line
	)
	
	# Is this going to make the page too long?
	if (len(paraBlock) + line) > 22:
		break
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add this paragraph to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	exportTTI(pageLegaliser(teletextPage))
# Load the template page for the header & footer
newsPageTemplate = loadTTI("news_page.tti")

# How many news pages do we want to create?
maxPages = 10
startPage = 261
# Download and parse an RSS Feed of news from NOS
newsData = feedparser.parse(" https://feeds.nos.nl/nosnieuwspolitiek ")

# Initialise a Page Counter
pageNum = 0

# Create a headlines list for P101
headlines = []

# Loop through each news story to produce pages
for newsArticle in newsData['entries']:
	# Set the first line we write on
	line = 5
	
	# Create a new teletext page
	teletextPage = {"number":(pageNum + startPage),"subpages":[{"packets":copy.deepcopy(newsPageTemplate["subpages"][0]["packets"])}]}
	
	# Create the title
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"yellow","text":newsArticle["title"]}]}]},
		line = line
	)
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add the title to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	# NOS provides news within the RSS feed, encoded as HTML
	# So we use BeautifulSoup to extract the HTML
	NOSSoup = BeautifulSoup(newsArticle['summary'], "lxml")
	NOSResults = NOSSoup.find_all('p')
	
	for paragraph in NOSResults:
		# Create a teletext paragraph
		paraBlock = toTeletextBlock(
			input = {"content":[{"align":"left","content":[{"colour":"white","text":paragraph.text}]}]},
			line = line
		)
		
		# Is this going to make the page too long?
		if (len(paraBlock) + line) > 22:
			break
		
		# Move on the line pointer
		line += (len(paraBlock) + 1)
		
		# Add this paragraph to the teletext page
		teletextPage["subpages"][0]["packets"] += paraBlock
	
	# Export the final page
	# We run it through "legaliser", this fixes the accented characters, but may be wrong for your country!
	exportTTI(pageLegaliser(teletextPage))
	
	headlines.append({"title":newsArticle["title"],"number":str(pageNum + startPage)})
	
	# Iterate the page counter
	pageNum += 1
	
	# Stop when we have enough pages
	if pageNum > maxPages:
		break

# Next we create P101, the headlines
# Start by loading the template
newsIndexTemplate = loadTTI("news_index.tti")

# Create a page
teletextPage = {"number":260,"subpages":[{"packets":copy.deepcopy(newsIndexTemplate["subpages"][0]["packets"])}]}

line = 5

for headline in headlines:
	paraBlock = toTeletextBlock(
		input = {"content":[{"align":"left","content":[{"colour":"white","text":headline["title"]}]},{"align":"right","content":[{"colour":"yellow","text":headline["number"]}]}]},
		line = line
	)
	
	# Is this going to make the page too long?
	if (len(paraBlock) + line) > 22:
		break
	
	# Move on the line pointer
	line += (len(paraBlock) + 1)
	
	# Add this paragraph to the teletext page
	teletextPage["subpages"][0]["packets"] += paraBlock
	
	exportTTI(pageLegaliser(teletextPage))

# Finally, let's make P100, the main service index.
frontPageTemplate = loadTTI("front_page.tti")

# Create a page
teletextPage = {"number":100,"subpages":[]}

for headline in headlines:
	paraBlock = toTeletextBlock(
		input = {
			"content":[
				{"align":"left","postWrapLimit":{"maxLines":2,"cutoff":36},"content":[{"colour":"white","text":headline["title"]}]},
				{"align":"right","content":[{"colour":"yellow","text":headline["number"]}]}
			]},
		line = 5
	)
	
	newSubpage = {"packets":copy.deepcopy(frontPageTemplate["subpages"][0]["packets"]) + paraBlock}
	
	teletextPage["subpages"].append(newSubpage)

exportTTI(pageLegaliser(teletextPage))