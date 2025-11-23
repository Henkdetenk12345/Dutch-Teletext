import feedparser
from bs4 import BeautifulSoup
import copy

from textBlock import toTeletextBlock
from page import exportTTI, loadTTI
from legaliser import pageLegaliser

# RSS feeds en instellingen
rss_feeds = [
    {"url": "https://feeds.nos.nl/nosnieuwsalgemeen", "max_articles": 10},
    {"url": "https://feeds.nos.nl/nossportalgemeen", "max_articles": 5},
    {"url": "https://feeds.nos.nl/jeugdjournaal", "max_articles": 3},
    {"url": "https://www.omroepwest.nl/rss/bollenstreek.xml", "max_articles": 3}
]

def fetch_articles():
    all_articles = []
    for feed in rss_feeds:
        parsed = feedparser.parse(feed["url"])
        count = 0
        for entry in parsed["entries"]:
            if count >= feed["max_articles"]:
                break
            
            # Gebruik dezelfde methode als demo.py
            soup = BeautifulSoup(entry.get("summary", ""), "lxml")
            paragraphs_elements = soup.find_all("p")
            
            # Converteer naar tekst, net zoals demo.py
            paragraphs = []
            for p in paragraphs_elements:
                text = p.text.strip()
                if text:  # Alleen toevoegen als er daadwerkelijk tekst is
                    paragraphs.append(text)
            
            # Fallback als er geen paragraphs zijn
            if not paragraphs:
                # Probeer de hele summary als plain text
                summary_text = soup.get_text().strip()
                if summary_text:
                    paragraphs = [summary_text]
                else:
                    paragraphs = ["Geen inhoud beschikbaar"]
            
            all_articles.append({
                "title": entry.get("title", "Geen titel"),
                "content": paragraphs
            })
            count += 1
    return all_articles

def create_newsreel_page(articles, page_number=152):
    template = loadTTI("news_page.tti")
    subpages = []

    # Intro subpagina
    intro_lines = [
        {"line": 3, "text": "        U KIJKT NAAR BMN Teletekst", "align": "center", "colour": "white"},
        {"line": 5, "text": "NIEUWS EN INFORMATIE VAN", "align": "center", "colour": "white"},
        {"line": 7, "text": "    DE NOS & OMROEP WEST", "align": "center", "colour": "yellow"},
        {"line": 11, "text": " De volledige service biedt vele", "align": "left", "colour": "white"},
        {"line": 12, "text": "  pagina's en is beschikbaar voor", "align": "left", "colour": "white"},
        {"line": 13, "text": "   iedereen met een geschikt", "align": "left", "colour": "white"},
        {"line": 14, "text": "        televisietoestel.", "align": "left", "colour": "white"}
    ]
    intro_packets = copy.deepcopy(template["subpages"][0]["packets"])
    for item in intro_lines:
        block = toTeletextBlock(
            input={"content": [{"align": item["align"], "content": [{"colour": item["colour"], "text": item["text"]}]}]},
            line=item["line"]
        )
        intro_packets += block
    subpages.append({"packets": intro_packets})

    # Artikel subpagina's
    for article in articles:
        packets = copy.deepcopy(template["subpages"][0]["packets"])
        line = 5

        title_block = toTeletextBlock(
            input={"content": [{"align": "left", "content": [{"colour": "yellow", "text": article["title"]}]}]},
            line=line
        )
        line += len(title_block) + 1
        packets += title_block

        for paragraph in article["content"]:
            para_block = toTeletextBlock(
                input={"content": [{"align": "left", "content": [{"colour": "white", "text": paragraph}]}]},
                line=line
            )
            if line + len(para_block) > 22:
                break
            line += len(para_block) + 1
            packets += para_block

        subpages.append({"packets": packets})

    # Actuele weertekst toevoegen
    try:
        from weertekst_now import get_weather, wind_direction_to_str

        weer = get_weather()
        if weer:
            packets = copy.deepcopy(template["subpages"][0]["packets"])
            line = 5

            def add_line(text, colour="white"):
                nonlocal line
                paraBlock = toTeletextBlock(
                    input={"content": [{"align": "left", "content": [{"colour": colour, "text": text}]}]},
                    line=line
                )
                packets.extend(paraBlock)
                line += len(paraBlock) + 1

            add_line("Actueel weer in Hillegom", colour="yellow")
            add_line(f"Temp.: {weer['temperature']} °C")
            add_line(f"Gevoelstemp.: {weer['feels_like']} °C")
            add_line(f"Bewolking: {weer['cloudcover']}%")
            add_line(f"Luchtvochtigheid: {weer['humidity']}%")
            add_line(f"Windsnelheid: {weer['windspeed_kmh']} km/u ({wind_direction_to_str(weer['wind_direction'])})")
            add_line(f"Neerslagkans: {weer['rain_chance']}")

            subpages.append({"packets": packets})
    except Exception as e:
        print("Kon actuele weerpagina niet toevoegen:", e)

    # 5-daagse verwachting toevoegen
    try:
        from weertekst_5day import get_5_day_forecast

        forecast = get_5_day_forecast()
        if forecast:
            packets = copy.deepcopy(template["subpages"][0]["packets"])
            line = 5

            def add_line(text, colour="white"):
                nonlocal line
                paraBlock = toTeletextBlock(
                    input={"content": [{"align": "left", "content": [{"colour": colour, "text": text}]}]},
                    line=line
                )
                packets.extend(paraBlock)
                line += len(paraBlock) + 1

            add_line("5-daagse verwachting Hillegom", colour="yellow")
            for dag in forecast:
                add_line(dag)

            subpages.append({"packets": packets})
    except Exception as e:
        print("Kon 5-daagse weerpagina niet toevoegen:", e)

    # Voeg erasePage en update flags toe voor PS,c008
    page = {
        "number": page_number, 
        "subpages": subpages, 
        "control": {
            "cycleTime": "25,T",
            "erasePage": True,
            "update": True
        }
    }
    exportTTI(pageLegaliser(page))
    print(f"Newsreel met {len(subpages)} subpagina's opgeslagen als pagina {page_number}.")

if True:
    print("=== NEWSREEL MET SUBPAGINA'S ZONDER BRON ===")
    articles = fetch_articles()
    create_newsreel_page(articles)
    print("Klaar.")