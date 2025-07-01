import requests
import copy
from bs4 import BeautifulSoup
from textBlock import toTeletextBlock
from page import exportTTI, loadTTI
from legaliser import pageLegaliser

def get_weather():
    api_key = "bfb1f2b8ee2cc2051070561815d83445"
    city = "Hillegom"
    country_code = "NL"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=metric&lang=nl"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "cloudcover": data["clouds"]["all"],
            "humidity": data["main"]["humidity"],
            "windspeed_kmh": round(data["wind"]["speed"] * 3.6),
            "wind_direction": data["wind"].get("deg", 0),
            "rain_chance": "Niet beschikbaar",  # OpenWeather geeft geen kans als aparte waarde in de current API
            "description": data["weather"][0]["description"]
        }
    else:
        print("Fout bij ophalen weergegevens:", response.status_code)
        return None

def wind_direction_to_str(degree):
    directions = ['Noord', 'Noordoost', 'Oost', 'Zuidoost', 'Zuid', 'Zuidwest', 'West', 'Noordwest']
    ix = round(degree / 45) % 8
    return directions[ix]

# Ophalen van weergegevens
weather = get_weather()
if not weather:
    exit()

temperature = weather["temperature"]
cloudcover = weather["cloudcover"]
humidity = weather["humidity"]
windspeed_kmh = weather["windspeed_kmh"]
wind_direction_str = wind_direction_to_str(weather["wind_direction"])
rain_chance = weather["rain_chance"]  # Placeholder, tenzij je forecast API gebruikt

# Bouw de teletext-pagina op
weatherPageTemplate = loadTTI("weather_page.tti")
teletextPage = {"number": 301, "subpages": [{"packets": copy.deepcopy(weatherPageTemplate["subpages"][0]["packets"])}]}
line = 7

def add_line(text, colour="white"):
    global line
    paraBlock = toTeletextBlock(
        input={"content": [{"align": "left", "content": [{"colour": colour, "text": text}]}]},
        line=line
    )
    teletextPage["subpages"][0]["packets"] += paraBlock
    line += len(paraBlock) + 1

add_line(f"Temperatuur: {temperature} °C", colour="yellow")
add_line(f"Bewolking: {cloudcover}%")
add_line(f"Luchtvochtigheid: {humidity}%")
add_line(f"Windsnelheid: {windspeed_kmh} km/u ({wind_direction_str})")
add_line(f"Neerslagkans: {rain_chance}")

# Exporteer als TTI
exportTTI(pageLegaliser(teletextPage))
