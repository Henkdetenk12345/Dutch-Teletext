import requests
import re
import copy

from bs4 import BeautifulSoup
from textBlock import toTeletextBlock, tableRow
from page import exportTTI, loadTTI
from legaliser import pageLegaliser

url = "https://keukenkampioendivisie.nl/klassement"
response = requests.get(url)
response.raise_for_status()  # Controleer of de request succesvol was

html_content = response.text
print(html_content)

soup = BeautifulSoup(html_content, "html.parser")

table = soup.find("table", {"class": "table"})  # Vind de tabel met resultaten
rows = table.find_all("tr")  # Vind alle tabelrijen

eredivisie_resultaten = []  # Lijst om resultaten in op te slaan
for row in rows[1:]:  # Sla eerste rij (koptekst) over
    cells = row.find_all("td")  # Vind alle tabelcellen
    if len(cells) >= 4:  # Controleer of er voldoende cellen zijn
        team1 = cells[1].text.strip()
        team2 = cells[6].text.strip()
        team3 = cells[5].text.strip()
        score = cells[3].text.strip()  # Verwacht een "score" cel
        eredivisie_resultaten.append({
            "Stand": team1,
            "Club": score,
            "P": team2,
            "W | V | G": team3
            
        })
print(eredivisie_resultaten)

# Start by loading the template
newsIndexTemplate = loadTTI("Voetbal.tti")

# Create a page
teletextPage = {"number":282,"subpages":[{"packets":copy.deepcopy(newsIndexTemplate["subpages"][0]["packets"])}]}

line = 6

for headline in eredivisie_resultaten:
    paraBlock = tableRow(
        [
            {"width":17,"data":"Club","colour":"cyan"},
            {"width":16,"data":"W | V | G","colour":"white"},
            {"width":3,"data":"P","colour":"cyan","align":"right"},
        ],
        headline
    )
    
    paraBlock = [{"number":line,"text":paraBlock}]
    
    # Is this going to make the page too long?
    if (len(paraBlock) + line) > 22:
        break
    
    # Move on the line pointer
    line += (len(paraBlock))
    
    # Add this paragraph to the teletext page
    teletextPage["subpages"][0]["packets"] += paraBlock
    
exportTTI(pageLegaliser(teletextPage))