from typing import List
from bs4 import BeautifulSoup
import bs4
import requests
import pycountry

import datetime

from enum import IntEnum

from dataclasses import dataclass
from dataclasses import field

ECB_TWO_EURO_URL = "https://www.ecb.europa.eu/euro/coins/comm/html/comm_{year}.{lang}.html"
START_YEAR = 2004
CURRENT_YEAR = datetime.datetime.now().year

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
            print(country_name)
            country = pycountry.countries.get(
                name=element.text.strip()
            ).alpha_2
            coin.countries = [country]
        elif element.name == "div":
            pass
        elif element.name == "hr":
            pass
        else:
            print("unknown element type")

        print(coin)


    

if __name__ == "__main__":
    print(get_commemorative_coins("de"))