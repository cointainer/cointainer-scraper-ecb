# uses countries from https://github.com/mledoze/countries/blob/master/dist/countries.json

import json

import requests

response = requests.get("https://raw.githubusercontent.com/mledoze/countries/master/dist/countries.json")

countries = json.loads(response.text)

translations = {}
for country in countries:
    for translation in country["translations"].values():
        translated_country = translation["common"].lower()

        if translated_country in translations:
            continue

        translations[translated_country] = country["name"]["common"]

with open("cointainer_scraper_ecb/countries.json", "w", encoding="utf-8") as f:
    json.dump(translations, f)
