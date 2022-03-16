import datetime
import json
import logging
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Dict, List, cast
from bs4.element import NavigableString, Tag

import pycountry
from pycountry.db import Data
import requests

# TODO: try to remove this dependeny by just declaring a long list with the mappings?
import dateparser
from bs4 import BeautifulSoup

COIN_IMAGE_URL_REGEX = ""

LOG = logging.getLogger(__name__)

ECB_BASE_URL = "https://www.ecb.europa.eu"
ECB_TWO_EURO_URL = (
    "https://www.ecb.europa.eu/euro/coins/comm/html/comm_{year}.{lang}.html"
)
START_YEAR = 2004
CURRENT_YEAR = datetime.datetime.now().year

path = Path(__file__).parent / Path("./countries.json")
with path.open() as f:
    country_translations = json.load(f)

fuzzy_search_cache: Dict[str, Data] = {}

info_description_mapping = {
    0: "feature",
    1: "description",
    2: "issuing volume",
    3: "issuing date",
}


@dataclass
class TwoEuro:
    countries: List[str] = field(default_factory=list)
    feature: str = ""
    volume: int = 0
    description: str = ""
    image_urls: List[str] = field(default_factory=list)
    image_attributions: List[str] = field(default_factory=list)
    circulation_dates: List[datetime.date] = field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"Coin(countries='{self.countries}', "
            f"feature='{self.feature[:25]}...', "
            f"volume='{self.volume}', "
            f"description='{self.description[:25]}...')"
        )

def _get_alpha2_country_from_string(text: str, translate: bool = True) -> str:
    country_name = text.strip().capitalize()
    if translate:
        country_name = country_translations[country_name.lower()]
    capitalized_translated_country = country_name.capitalize()

    found_country = pycountry.countries.get(name=capitalized_translated_country)

    if found_country is None:
        try:
            found_country = fuzzy_search_cache[capitalized_translated_country]
        except KeyError:
            found_countries = pycountry.countries.search_fuzzy(
                capitalized_translated_country
            )
            if not found_countries:
                LOG.warning(
                    f"no country object matched country named: '{country_name}'"
                )
            found_country = found_countries[0]
            LOG.info(
                "found country '{found_country.name}' with fuzzy search from '{translated_country}'"
            )
            fuzzy_search_cache[capitalized_translated_country] = found_country

    return found_country.alpha_2


def get_commemorative_coins(lang: str = "", year: int = START_YEAR) -> List[TwoEuro]:
    response = requests.get(ECB_TWO_EURO_URL.format(year=year, lang=lang))
    soup = BeautifulSoup(response.content, "html.parser")
    coin_boxes_div = soup.find("div", {"class": "boxes"})

    if coin_boxes_div is None:
        LOG.error("could not find 'div' with class 'boxes'. No coins can be crawled!")
        return []

    if coin_boxes_div is NavigableString:
        LOG.error("soup result is a NavigableString. No coins can be crawled!")
        return []

    coin_boxes = cast(Tag, coin_boxes_div).find_all("div", {"class": "box"})

    coins: List[TwoEuro] = []
    for coin_box in coin_boxes:
        # get all descriptions fields assumed to be in order:
        #     'Feature:', 'Description:', 'Issuing volume:', 'Issuing date:'
        infos: List[str] = []
        for index, paragraph in enumerate(coin_box.find_all("p")):
            paragraph_type: str = paragraph.find("strong").text
            if not paragraph_type.strip().endswith(":"):
                LOG.warning(
                    "could not found ':' on strong tag. Possible missing info "
                    f"description: '{info_description_mapping[index]}' with "
                    f"paragraph tag: {paragraph.text.encode('string_escape')}"
                )
                infos.append("")
                continue

            infos.append(paragraph.text.lstrip(paragraph_type).strip())

        feature = infos[0]
        description = infos[1]
        volume = infos[2]
        raw_datetime = infos[3].strip()
        parsed_datetime = dateparser.parse(raw_datetime, languages=[lang])
        circulation_dates = []
        if parsed_datetime is not None:
            circulation_dates = [parsed_datetime.date()]
        else:
            LOG.warning(
                "could not extract datetime from"
                f" given circulation date: '{raw_datetime}'"
            )

        # coin image(s)
        image_container = coin_box.find("div", {"class": "coins"})
        images = image_container.find_all("img")

        countries: List[str] = []
        image_urls = [ECB_BASE_URL + image["src"] for image in images]
        if len(image_urls) > 1:
            for image_url in image_urls:
                reminder, country = image_url.rsplit(".", maxsplit=1)[0].rsplit(
                    "_", maxsplit=1
                )
                country_alpha2 = _get_alpha2_country_from_string(country, lang != "en")
                coin_year = int(reminder.rsplit("_", maxsplit=1)[1])
                assert coin_year == year
                countries.append(country_alpha2)
        else:
            # coin country
            title_header = coin_box.find("h3")
            countries = [
                _get_alpha2_country_from_string(title_header.text, lang != "en")
            ]

        coin = TwoEuro(
            countries=countries,
            feature=feature,
            volume=volume,
            description=description,
            image_urls=image_urls,
            circulation_dates=circulation_dates,
        )
        coins.append(coin)
    return coins


if __name__ == "__main__":
    get_commemorative_coins("de", year=2006)
