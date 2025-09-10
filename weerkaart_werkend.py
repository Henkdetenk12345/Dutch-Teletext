import requests
import os
import re

# Temperatuurlocaties met hun placeholder tekst die vervangen moet worden
TEMPERATUUR_LOCATIES = {
    "10": {"locatie": "leeuwarden"},   # Friesland
    "20": {"locatie": "amsterdam"},    # Noord-Holland
    "30": {"locatie": "arnhem"},       # Gelderland
    "40": {"locatie": "eindhoven"},    # Brabant/Limburg
    "50": {"locatie": "zwolle"},       # Overijsel
    "60": {"locatie": "breda"},        # Brabant/Zeeland
}

def get_weer_voor_locatie(locatie, api_key):
    """Haalt weergegevens op voor een specifieke locatie"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={locatie},NL&appid={api_key}&units=metric&lang=nl"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "temp": round(data["main"]["temp"]),
                "weer_id": str(data["weather"][0]["id"]),
                "beschrijving": data["weather"][0]["description"]
            }
        else:
            print(f"Fout bij ophalen van weergegevens voor {locatie}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Fout bij ophalen van weergegevens voor {locatie}: {e}")
        return None


def _vervang_in_ol_content(tti_text, vervangingen, vaste_breedte=2):
    """
    Pas alleen OL-regelinhoud (na 'OL,<n>,') aan.
    - vervangingen: dict {'10': 17, '20': 19, ...}
    - vaste_breedte=2 houdt de uitlijning stabiel (bij -10 heb je 3 chars)
    """
    out_lines = []
    for line in tti_text.splitlines(keepends=True):
        if line.startswith("OL,"):
            parts = line.rstrip("\n").split(",", 2)
            if len(parts) == 3:
                head = f"{parts[0]},{parts[1]},"
                content = parts[2]

                # vervang alleen in CONTENT
                for placeholder, temp in vervangingen.items():
                    temp_str = f"{int(temp):2d}"  # altijd 2 tekens breed
                    pattern = rf'(?<!\d){re.escape(placeholder)}(?!\d)'
                    content = re.sub(pattern, temp_str, content)

                # Geen automatische padding - laat de originele content intact
                # Dit voorkomt het beschadigen van grafische karakters

                line = head + content + "\n"
        out_lines.append(line)
    return "".join(out_lines)


def maak_weer_kaart(input_bestand="kaart_template.tti"):
    """Maakt een teletext weerkaart van Nederland"""
    api_key = "bfb1f2b8ee2cc2051070561815d83445"
    
    if not os.path.exists(input_bestand):
        print(f"FOUT: Template bestand '{input_bestand}' niet gevonden.")
        print("Maak eerst een .tti bestand met je kaartdata en placeholders (10, 20, 30, etc.)")
        return
    
    try:
        # Lees het template bestand in met UTF-8 (zoals V1, die wel werkte)
        with open(input_bestand, 'r', encoding='utf-8', errors='ignore') as f:
            tti_inhoud = f.read()
        
        print("Template bestand ingelezen...")
        
        # Haal temperaturen op
        vervangingen = {}
        for placeholder, info in TEMPERATUUR_LOCATIES.items():
            weer_data = get_weer_voor_locatie(info["locatie"], api_key)
            if weer_data:
                vervangingen[placeholder] = weer_data["temp"]
                print(f"Temperatuur in {info['locatie']}: {weer_data['temp']}°C - {weer_data['beschrijving']}")
            else:
                print(f"Kon geen weerdata ophalen voor {info['locatie']}")
        
        # Vervang alleen in OL-content
        tti_inhoud = _vervang_in_ol_content(tti_inhoud, vervangingen, vaste_breedte=2)
        
        # Maak teletext directory als deze niet bestaat
        if not os.path.exists("teletext"):
            os.makedirs("teletext")
        
        # Schrijf het nieuwe TTI bestand met UTF-8 (zoals V1)
        output_bestand = "teletext/P303.tti"
        with open(output_bestand, 'w', encoding='utf-8') as f:
            f.write(tti_inhoud)
        
        print(f"Weerkaart opgeslagen als {output_bestand}")
        print("Je kunt dit bestand nu importeren in je teletext systeem")
        
    except Exception as e:
        print(f"Fout bij maken van weerkaart: {e}")
        import traceback
        traceback.print_exc()


def test_temperaturen():
    """Test functie om alleen de temperaturen op te halen"""
    api_key = "bfb1f2b8ee2cc2051070561815d83445"
    
    print("Test van weerdata ophalen:")
    print("-" * 50)
    
    for placeholder, info in TEMPERATUUR_LOCATIES.items():
        locatie = info["locatie"]
        weer_data = get_weer_voor_locatie(locatie, api_key)
        
        if weer_data:
            print(f"{locatie:12} (placeholder {placeholder:2}): {weer_data['temp']:2}°C - {weer_data['beschrijving']}")
        else:
            print(f"{locatie:12} (placeholder {placeholder:2}): FOUT - geen data")


def maak_template():
    """Maakt een voorbeeld template bestand"""
    template_inhoud = """PN,40300
SC,0000
PS,8000
RE,0
CT,20,T
OL,1,         NEDERLAND WEERKAART
OL,2,
OL,3,              10
OL,4,
OL,5,          20      30
OL,6,
OL,7,              40
OL,8,
OL,9,          50      60
OL,10,
"""
    
    with open("kaart_template.tti", 'w', encoding='utf-8') as f:
        f.write(template_inhoud)
    
    print("Voorbeeld template 'kaart_template.tti' aangemaakt")
    print("Vervang dit door je echte kaartdata met placeholders 10, 20, 30, 40, 50, 60")


# Automatisch uitvoeren bij import (voor demo.py)
if os.path.exists("kaart_template.tti"):
    maak_weer_kaart("kaart_template.tti")
else:
    print("Weerkaart: Template 'kaart_template.tti' niet gevonden - sla over")

# Voor handmatige uitvoering vanaf command line
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_temperaturen()
        elif sys.argv[1] == "template":
            maak_template()
        else:
            # Gebruik aangegeven bestand als template
            maak_weer_kaart(sys.argv[1])
    else:
        print("Weerkaart al uitgevoerd bij import")
        print("Gebruik 'python script.py test' of 'python script.py template' voor andere opties")
