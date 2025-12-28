import feedparser
from bs4 import BeautifulSoup
import copy
from datetime import datetime

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

def get_intro_template():
    """Bepaalt welke intro template te gebruiken op basis van de datum"""
    now = datetime.now()
    day = now.day
    month = now.month
    
    # 29 november t/m 27 december: kerst intro
    if month == 11 and day >= 29:
        return "kerst_intro.tti"
    elif month == 12 and day <= 27:
        return "kerst_intro.tti"
    
    # 31 december t/m 2 januari: nieuwjaar intro
    if month == 12 and day == 31:
        return "nieuwjaar_intro.tti"
    elif month == 1 and day <= 2:
        return "nieuwjaar_intro.tti"
    
    # Standaard intro voor alle andere dagen
    return "newsreel_intro.tti"

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

    # INTRO SUBPAGINA - laad uit TTI template op basis van datum
    intro_filename = get_intro_template()
    print(f"Loading intro template: {intro_filename}")
    intro_template = loadTTI(intro_filename)
    intro_subpage = {"packets": copy.deepcopy(intro_template["subpages"][0]["packets"])}
    subpages.append(intro_subpage)
    print(f"Intro loaded with {len(intro_subpage['packets'])} packets")

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
    
    print(f"\nNewsreel complete!")
    print(f"Total subpages: {len(subpages)}")
    print(f"  - Intro: 1 ({intro_filename})")
    print(f"  - Artikelen: {len(articles)}")
    print(f"  - Weerpagina's: {len(subpages) - len(articles) - 1}")

if True:
    print("=== NEWSREEL MET TTI INTRO ===")
    articles = fetch_articles()
    create_newsreel_page(articles)
    print("Klaar.")
