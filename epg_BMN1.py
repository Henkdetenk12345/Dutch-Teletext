import json
import requests
from datetime import datetime
from textBlock import toTeletextBlock
from page import exportTTI, loadTTI
from legaliser import pageLegaliser
import copy

# Laad de EPG data van de URL
response = requests.get('https://intern.bollenstreekmedianetwerk.nl/textbulletin/nmptv_epg.json')
epg_data = response.json()

# Load de template voor EPG pagina's
epgPageTemplate = loadTTI("news_page.tti")

# Filter het testbeeld eruit
epg_data = [item for item in epg_data if item.get('title') != 'TestBeeld']

# Huidige tijd in seconds
current_time = datetime.now().timestamp()

# Filter programma's die al voorbij zijn
epg_data = [item for item in epg_data if item.get('start_seconds', 0) >= current_time]

# Sorteer op starttijd
epg_data_sorted = sorted(epg_data, key=lambda x: x.get('start_seconds', 0))

# Maak pagina 401 met subpagina's
teletextPage = {"number": 401, "subpages": []}

# Index voor het doorlopen van programma's
program_index = 0

# Maak subpagina's tot alle programma's verwerkt zijn
while program_index < len(epg_data_sorted):
    # Nieuwe subpagina
    subpage = {"packets": copy.deepcopy(epgPageTemplate["subpages"][0]["packets"])}
    
    line = 5
    
    # Titel
    titleBlock = toTeletextBlock(
        input = {"content": [{"align": "left", "content": [{"colour": "yellow", "text": "BMN 1 TV PROGRAMMA VOOR VANDAAG"}]}]},
        line = line
    )
    subpage["packets"] += titleBlock
    line += len(titleBlock) + 1
    
    # Voeg programma's toe totdat de pagina vol is
    while program_index < len(epg_data_sorted):
        program = epg_data_sorted[program_index]
        
        start_time = program.get('start', '')
        title = program.get('title', 'Onbekend')
        description = program.get('description', '')
        
        # Tijd en titel in één regel
        header = f"{start_time} {title}"
        headerBlock = toTeletextBlock(
            input = {"content": [{"align": "left", "content": [{"colour": "cyan", "text": header}]}]},
            line = line
        )
        
        # Bereken beschrijving blok
        descBlock = []
        if description:
            descBlock = toTeletextBlock(
                input = {"content": [{"align": "left", "content": [{"colour": "white", "text": description}]}]},
                line = line + len(headerBlock)
            )
        
        # Check of het HELE programma (header + beschrijving + extra regel) past
        total_lines_needed = len(headerBlock) + len(descBlock) + (1 if descBlock else 0)
        
        if (line + total_lines_needed) > 22:
            # Past niet meer op deze pagina, ga naar volgende subpagina
            break
            
        # Voeg header toe
        subpage["packets"] += headerBlock
        line += len(headerBlock)
        
        # Voeg beschrijving toe als die er is
        if descBlock:
            subpage["packets"] += descBlock
            line += len(descBlock) + 1
        
        # Ga naar volgend programma
        program_index += 1
    
    teletextPage["subpages"].append(subpage)

exportTTI(pageLegaliser(teletextPage))

print(f"EPG pagina P401 aangemaakt met {len(teletextPage['subpages'])} subpagina's")
