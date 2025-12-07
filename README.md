# Pokémon Cards CLI

Deze applicatie is een command line tool om een Pokémonkaartencollectie te beheren met behulp van een SQLite-database.  
Je kan Pokémon-sets en kaarten toevoegen, importeren via CSV, bekijken en exporteren.

---

## 1. Vereisten

- Python 3.9 of hoger
- Git

De applicatie gebruikt geen externe Python-packages. Alles werkt met standaard Python libraries.

## 2. Repository clonen

git clone https://github.com/jeeensxd/pokemon-cards-cli.git
cd pokemon-cards-cli


## 3. Virtuele omgeving maken en activeren

python3 -m venv venv
source venv/bin/activate

## 4. Packages installeren (In dit geval zijn er geen)

pip install -r requirements.txt

## 5. Configuratiebestand aanmaken

Maak een bestand config.ini aan in de hoofdmap van het project.

Inhoud van config.ini:

[database]
path = data/pokecards.db

## 6. Database initialiseren

python -m app.cli init-db

## 7. Voorbeelddata importeren via CSV
## 7.1 Sets importeren

Maak dit bestand aan:
data/sets.csv

Voorbeelddata:
code;name
BASE;Base Set
JNG;Jungle
TR;Team Rocket
RS;Ruby & Sapphire
SS;Sandstorm
DR;Dragon
BRS;Brilliant Stars
SV1;Scarlet & Violet Base
PAL;Paldea Evolved
PAR;Paradox Rift
TEF;Temporal Forces

Importeer data:
python -m app.cli import-sets --file data/sets.csv

Controleer data:
python -m app.cli list-sets

## 7.2 Kaarten importeren

Voorbeelddata: `data/cards.csv`

```csv
name;set_code;count;price
Charizard;BASE;1;350
Blastoise;BASE;1;180
Dark Charizard;TR;1;190
Sceptile ex;RS;1;110
Rayquaza ex;DR;1;220
Charizard VSTAR;BRS;2;35.5
Umbreon VMAX (Alt Art);EVS;1;520
Charizard ex (Tera);SV1;1;75
Roaring Moon ex;PAR;1;32
Walking Wake ex;TEF;1;35

Importeer data:
python -m app.cli import-cards --file data/cards.csv

Controleer data:
python -m app.cli list-cards

## 8. Manueel gegevens toevoegen via de terminal

Set toevoegen:
python -m app.cli add-set --code "OBF" --name "Obsidian Flames"

Kaart toevoegen:
python -m app.cli add-card --name "Charizard ex" --set-code "OBF" --count 1 --price 45

## Overzicht kaarten tonen

python -m app.cli list-cards

## 10. Export naar CSV

python -m app.cli export-cards --output reports/overzicht.csv

## 11. Database bekijken

Via SQLite in de terminal:
sqlite3 data/pokecards.db

Tabellen tonen:
.tables

Alle kaarten bekijken:
SELECT * FROM cards;

Afsluiten:
.exit

