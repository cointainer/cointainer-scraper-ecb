# uses countries from https://github.com/mledoze/countries/blob/master/dist/countries.json

import json
from pathlib import Path

import requests

response = requests.get(
    "https://raw.githubusercontent.com/mledoze/countries/master/dist/countries.json"
)

countries = json.loads(response.text)

translations = {}
for country in countries:
    for translation in country["translations"].values():
        translated_country = translation["common"].lower()

        if translated_country in translations:
            continue

        translations[translated_country] = country["name"]["common"]

file_path = Path(__file__).parent.parent / Path(
    "cointainer_scraper_ecb/data/countries.json"
)
with file_path.open("w", encoding="utf-8") as f:
    json.dump(translations, f)
