import requests
import copy
from datetime import datetime
from collections import defaultdict
from textBlock import toTeletextBlock
from page import exportTTI, loadTTI
from legaliser import pageLegaliser

# Nederlandse vertalingstabellen
dagen_nl = {
    "Mon": "ma", "Tue": "di", "Wed": "wo", "Thu": "do",
    "Fri": "vr", "Sat": "za", "Sun": "zo"
}
maanden_nl = {
    "Jan": "jan", "Feb": "feb", "Mar": "mrt", "Apr": "apr",
    "May": "mei", "Jun": "jun", "Jul": "jul", "Aug": "aug",
    "Sep": "sep", "Oct": "okt", "Nov": "nov", "Dec": "dec"
}

def get_5_day_forecast():
    api_key = "bfb1f2b8ee2cc2051070561815d83445"
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Hillegom,NL&appid={api_key}&units=metric&lang=nl"
    response = requests.get(url)
    if response.status_code != 200:
        print("Fout bij ophalen van data:", response.status_code)
        return None

    data = response.json()
    daily_data = defaultdict(list)

    for entry in data["list"]:
        dt = datetime.fromtimestamp(entry["dt"])
        date_str = dt.strftime("%Y-%m-%d")
        daily_data[date_str].append(entry)

    forecast_summary = []
    for i, (date, entries) in enumerate(sorted(daily_data.items())):
        temps = [e["main"]["temp"] for e in entries]
        weather_descriptions = [e["weather"][0]["description"] for e in entries]
        pop_values = [e.get("pop", 0) * 100 for e in entries]

        avg_temp = round(sum(temps) / len(temps))
        main_description = max(set(weather_descriptions), key=weather_descriptions.count)
        rain_chance = round(max(pop_values))

        dt_obj = datetime.strptime(date, "%Y-%m-%d")
        day_label = f"{dagen_nl[dt_obj.strftime('%a')]} {dt_obj.strftime('%d')} {maanden_nl[dt_obj.strftime('%b')]}"

        forecast_summary.append(f"{day_label:<11} {avg_temp}°C, {main_description}, {rain_chance}% regen")

        if i >= 4:
            break

    return forecast_summary

# Bouw Teletekstpagina
weatherPageTemplate = loadTTI("weather_page.tti")
teletextPage = {"number": 302, "subpages": [{"packets": copy.deepcopy(weatherPageTemplate["subpages"][0]["packets"])}]}
line = 7

def add_line(text, colour="white"):
    global line
    paraBlock = toTeletextBlock(
        input={"content": [{"align": "left", "content": [{"colour": colour, "text": text}]}]},
        line=line
    )
    teletextPage["subpages"][0]["packets"] += paraBlock
    line += len(paraBlock) + 1

forecast = get_5_day_forecast()
if not forecast:
    exit()

for dag in forecast:
    add_line(dag)

exportTTI(pageLegaliser(teletextPage))
