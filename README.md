# Dutch Teletext

Scripts om een Nederlandse teletext service te maken met RSS feeds van NOS, Omroep West, voetbal uitslagen en weerberichten.

## Beschrijving

Dit project genereert TTI (Teletext) bestanden uit verschillende Nederlandse nieuwsbronnen:

- **NOS Nieuws** (Algemeen, Sport, Jeugdjournaal, Voetbal, Formule 1, Politiek)
- **Omroep West** (Bollenstreek)  
- **Eredivisie & Eerste Divisie uitslagen**
- **Weerberichten** (actueel + 5-daagse verwachting)

Er zijn twee hoofdmodi:
1. **Individuele pagina's** (demo.py) - elke RSS entry wordt een aparte teletext pagina
2. **Newsreel** (newsreel_werkend.py) - alle artikelen in 1 pagina met doorlopende subpagina's

## Vereisten

```bash
pip install feedparser beautifulsoup4 lxml cchardet
```

- `feedparser` - RSS/Atom feed parsing
- `beautifulsoup4` - HTML content extractie
- `lxml` - XML/HTML parser backend
- `cchardet` - Karakterset detectie

## Bestanden

### Hoofdscripts
- **`demo.py`** - Genereert individuele teletext pagina's per nieuwsartikel
- **`newsreel_werkend.py`** - Genereert 1 newsreel pagina (P152) met alle artikelen als subpagina's
- **`Eredivisie_uitslagen.py`** - Haalt Eredivisie uitslagen op
- **`Eerste_divisie.py`** - Haalt Eerste Divisie uitslagen op

### Weerfunctionaliteit
- **`weertekst_now.py`** - Actuele weersgegevens voor Hillegom
- **`weertekst_5day.py`** - 5-daagse weerverwachting

### Hulpbestanden
- **`textBlock.py`** - Tekst naar teletext blok conversie
- **`page.py`** - TTI export/import functionaliteit
- **`legaliser.py`** - Karakterset correcties voor teletext

### Templates
- **`news_page.tti`** - Template voor nieuwspagina's (gebruikt door newsreel_werkend.py en demo.py)
- **`news_index.tti`** - Template voor nieuwsindex pagina's (gebruikt door demo.py)
- **`front_page.tti`** - Template voor hoofdpagina P100 (gebruikt door demo.py)

## Gebruik

### Demo.py - Individuele Pagina's
Genereert aparte teletext pagina's per nieuwsbron:
- P101-111: NOS Algemeen Nieuws
- P200-210: NOS Sport
- P180-190: Jeugdjournaal  
- P160-170: Omroep West Bollenstreek
- P220-230: NOS Voetbal
- P240-250: NOS Formule 1
- P260-270: NOS Politiek

```bash
python demo.py
```

### Newsreel - Doorlopende Subpagina's
Genereert 1 pagina (P152) met alle artikelen als doorlopende subpagina's:

```bash
python newsreel_werkend.py
```

Bevat:
- Intro scherm
- NOS artikelen (max 10)
- NOS Sport (max 5) 
- Jeugdjournaal (max 3)
- Omroep West (max 3)
- Actueel weer Hillegom
- 5-daagse weerverwachting

## Pagina Nummering

| Pagina | Inhoud |
|--------|---------|
| P100 | Hoofdindex |
| P101-111 | NOS Algemeen + Index (P101) |
| P152 | Newsreel (alle bronnen) |
| P160-170 | Omroep West + Index (P160) |
| P180-190 | Jeugdjournaal + Index (P180) |
| P200-210 | NOS Sport + Index (P200) |
| P220-230 | NOS Voetbal + Index (P220) |
| P240-250 | NOS Formule 1 + Index (P240) |
| P260-270 | NOS Politiek + Index (P260) |

## Template Aanpassing

Pas de specifieke `.tti` template bestanden aan:

- **`news_page.tti`** - Layout voor artikelpagina's (header, footer, kleuren)
- **`news_index.tti`** - Layout voor indexpagina's met headlines  
- **`front_page.tti`** - Layout voor hoofdpagina P100

Aanpassingen kunnen zijn:
- Header/footer styling
- Kleuren en layout
- Paginanummering
- Branding

## RSS Feeds

Gebruikte feeds:
- `https://feeds.nos.nl/nosnieuwsalgemeen`
- `https://feeds.nos.nl/nossportalgemeen`  
- `https://feeds.nos.nl/jeugdjournaal`
- `https://feeds.nos.nl/nosvoetbal`
- `https://feeds.nos.nl/nossportformule1`
- `https://feeds.nos.nl/nosnieuwspolitiek`
- `https://www.omroepwest.nl/rss/bollenstreek.xml`

## Weer API

Voor weerberichten wordt een externe API gebruikt (zie `weertekst_now.py` en `weertekst_5day.py` voor configuratie).

## Troubleshooting

### Geen inhoud in RSS feed
Sommige RSS feeds (vooral regionale) bevatten alleen titels. Het systeem valt terug op "Geen inhoud beschikbaar" of probeert de summary te gebruiken.

### Karakterset problemen  
`legaliser.py` converteert speciale karakters naar teletext-compatibele versies.

### TTI export problemen
Controleer of de template `.tti` bestanden aanwezig zijn.

## Output

Het script genereert `.tti` bestanden die geïmporteerd kunnen worden in teletext systemen of software zoals:
- VBI inserters
- DVB-T multiplexers  
- Teletext decoder software

## Licentie

Vrij te gebruiken - doe er mee wat je wilt. 

Bij toevoegingen van leuke features (weerkaarten, etc.), maak een GitHub Issue met screenshots en uitleg.
