# uses countries from https://github.com/mledoze/countries/blob/master/dist/countries.json

import json
import requests

response = requests.get("https://raw.githubusercontent.com/mledoze/countries/master/dist/countries.json")

countries = json.loads(response.text)

translations = {}
for country in countries:
    deu = country["translations"]["deu"]["common"]
    translations[deu.lower()] = country["name"]["common"]

with open("coin_collector_parser_ecb/countries_de_en.json", "w", encoding='utf8') as f:
    json.dump(translations, f)