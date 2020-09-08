from typing import List
from bs4 import BeautifulSoup
import bs4
import requests
import pycountry

import datetime

from enum import IntEnum

from dataclasses import dataclass
from dataclasses import field

from pathlib import Path
import json

import logging

ECB_TWO_EURO_URL = "https://www.ecb.europa.eu/euro/coins/comm/html/comm_{year}.{lang}.html"
START_YEAR = 2004
CURRENT_YEAR = datetime.datetime.now().year

path = Path(__file__).parent / Path("./countries_de_en.json")
with path.open() as f:
    country_translations = json.load(f)

fuzzy_search_cache = {}

@dataclass
class TwoEuro:
    countries: List[str] = field(default_factory=list)
    feature: str = ""
    volume: int = 0
    circulation_dates: List[datetime.date] = field(default_factory=list)

class State(IntEnum):
    TITLE = 0
    CONTENT = 1
    SEPERATOR = 2

def get_commemorative_coins(lang=""):
    response = requests.get(ECB_TWO_EURO_URL.format(year=START_YEAR, lang=lang))
    soup = BeautifulSoup(response.content, "html.parser")
    coin_list = soup.find("div", {"class": "coinDesc"})

    for element in coin_list.children:
        if isinstance(element, bs4.element.NavigableString):
            continue

        coin = TwoEuro()

        if element.name == "h2":
            country_name = element.text.strip().capitalize()
            translated_country = country_translations[country_name.lower()]
            capitalized_translated_country = translated_country.capitalize()

            found_country = pycountry.countries.get(
                name=capitalized_translated_country
            )

            if found_country is None:
                try:
                    found_country = fuzzy_search_cache[capitalized_translated_country]
                except KeyError:
                    found_countries = pycountry.countries.search_fuzzy(capitalized_translated_country)
                    if not found_countries:
                        logging.warning("no country object matched country named: <%s>", translated_country)
                    found_country = found_countries[0]
                    logging.warning("found country <%s> with fuzzy search from <%s>", found_country.name, translated_country)
                    fuzzy_search_cache[capitalized_translated_country] = found_country

            coin.countries = [found_country.alpha_2]

        elif element.name == "div":
            pass
        elif element.name == "hr":
            pass
        else:
            print("unknown element type")

        print(coin)


    

if __name__ == "__main__":
    print(get_commemorative_coins("de"))