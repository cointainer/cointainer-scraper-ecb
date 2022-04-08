import datetime
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
import sys
from typing import Any, Dict, List, Literal, Optional, Tuple, cast, Union
from bs4.element import NavigableString, Tag

import pycountry
from pycountry.db import Data
import requests

# TODO: try to remove this dependeny by just declaring a long list with the mappings?
import dateparser
from bs4 import BeautifulSoup

COIN_IMAGE_URL_REGEX = ""

LOG = logging.getLogger("coin_collector")
LOG.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[{asctime}] [{levelname:<7}] [{name}] {message}",
    datefmt="%d.%m.%Y %H:%M:%S",
    style="{",
)

import pprint

stream = logging.StreamHandler(sys.stdout)
stream.setFormatter(formatter)
LOG.addHandler(stream)

ECB_BASE_URL = "https://www.ecb.europa.eu"
ECB_TWO_EURO_URL = (
    "https://www.ecb.europa.eu/euro/coins/comm/html/comm_{year}.{lang}.html"
)
START_YEAR = 2004
CURRENT_YEAR = datetime.datetime.now().year

path = Path(__file__).parent / Path("./countries.json")
with path.open() as f:
    country_translations = json.load(f)

fuzzy_search_cache: Dict[str, Data] = {
    "Vatican City".capitalize(): pycountry.countries.get(alpha_2="VA"),
    "Vatican".capitalize(): pycountry.countries.get(alpha_2="VA"),
    "Italia".capitalize(): pycountry.countries.get(alpha_2="IT"),
}

info_description_mapping = {
    0: "feature",
    1: "description",
    2: "issuing volume",
    3: "issuing date",
}

million_mapping = {
    "милиона монети",
    "milionů mincí",
    "mio. mønter",
    "Millionen Münzen",
    "εκατομμύρια κέρματα",
    "million coins",
    "millones de monedas",
    "miljonit münti",
    "miljoonaa kolikkoa",
    "millions de pièces",
    "000 000 kovanica",
    "millió érme",
    "milioni di pezzi",
    "mln. monetų",
    "milj. monētu",
    "miljun munita",
    "miljoen munten",
    "milionów monet",
    "milhões de moedas",
    "milioane de monede",
    "miliónov mincí",
    "milijonov kovancev",
    "miljoner mynt",
}


@dataclass
class Coinage:
    country: Optional[str]
    image_default_url: Optional[str]
    volume: Optional[int]
    image_default_url_info: Optional[str] = None
    country_info: Optional[str] = None
    circulation_date: Optional[datetime.date] = None
    image_attribution: Optional[str] = None
    circulation_date_info: Optional[str] = None
    volume_info: Optional[str] = None


@dataclass
class TwoEuro:
    feature: str = ""
    # volume: int = 0
    # volume_info: str = ""
    description: str = ""
    # countries: List[str] = field(default_factory=list)
    # image_urls: List[str] = field(default_factory=list)
    # image_attributions: List[str] = field(default_factory=list)
    # circulation_dates: List[datetime.date] = field(default_factory=list)
    # circulation_dates_info: str = ""
    coinages: List[Coinage] = field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"Coin(countries='{[coinage for coinage in self.coinages]}', "
            f"feature='{self.feature[:25]}...', "
            f"description='{self.description[:25]}...')"
        )


def _get_alpha2_country_from_string(
    text: str, year: int, paragraph_index: int, language: str = "en"
) -> Union[str, None]:
    if text.strip().lower() == "euro area countries":
        return None

    translate = language != "en"
    country_name = text.strip().capitalize()
    if translate:
        country_name = country_translations[country_name.lower()]
    capitalized_translated_country = country_name.capitalize()

    found_country = pycountry.countries.get(name=capitalized_translated_country)

    if found_country is None:
        try:
            found_country = fuzzy_search_cache[capitalized_translated_country]
        except KeyError:
            try:
                found_country = pycountry.countries.lookup(
                    capitalized_translated_country
                )
            except LookupError:
                return None
            LOG.info(
                f"({year}, {paragraph_index}) found country '{found_country.name}' "
                f"with fuzzy search from '{capitalized_translated_country}'"
            )
            fuzzy_search_cache[capitalized_translated_country] = found_country

    return found_country.alpha_2


def get_commemorative_coins(lang: str = "en", year: int = START_YEAR) -> List[TwoEuro]:
    response = requests.get(ECB_TWO_EURO_URL.format(year=year, lang=lang))
    return _get_commemorative_coins(response.content, lang, year)


@dataclass
class Content:
    feature: str = ""
    description: str = ""
    raw_issuing_volume: str = ""
    raw_issuing_date: str = ""


def _parse_content_fields(coin_box: Any, year: int, paragraph_index: int):
    # get all descriptions fields assumed to be in order:
    #     'Feature:', 'Description:', 'Issuing volume:', 'Issuing date:'
    infos: List[str] = []
    paragraphs = coin_box.find_all("p")

    # description (can be composed of multiple paragraphs)
    current_paragraph_content = ""
    while len(paragraphs) > 0:
        paragraph = paragraphs.pop(0)
        paragraph_type = paragraph.find("strong")

        if paragraph_type is None:
            current_paragraph_content += f" {paragraph.text}"
            continue

        if not paragraph_type.text.strip().endswith(":"):
            LOG.warning(
                f"({year}, {paragraph_index}) could not found ':' on strong tag. Possible missing info "
                f"description: '{info_description_mapping[len(infos)]}' with "
                f"paragraph tag: {paragraph.text.encode('string_escape')}"
            )
            infos.append("")
            continue

        current_paragraph_content = paragraph.text.lstrip(
            paragraph_type.text.strip()
        ).strip()

        infos.append(current_paragraph_content)

    if len(infos) != 4:
        infos += [""] * (4 - len(infos))

    return Content(
        feature=infos[0],
        description=infos[1],
        raw_issuing_volume=infos[2].strip(),
        raw_issuing_date=infos[3].strip(),
    )


def _parse_volume(box_content: Content) -> Tuple[Optional[int], Optional[str]]:
    volume_str = "".join([c for c in box_content.raw_issuing_volume if c.isdigit()])
    if len(volume_str) != 0:
        volume = int(volume_str)
        volume_word_suffix: List[str] = []
        for word in reversed(
            box_content.raw_issuing_volume.replace("\xa0", " ").split(" ")
        ):
            if any(c.isdigit() for c in word):
                break
            volume_word_suffix.append(word)

        if " ".join(reversed(volume_word_suffix)) in million_mapping:
            volume *= 1_000_000
        return (volume, None)
    else:
        return (None, box_content.raw_issuing_volume)


def _parse_image_urls(coin_box: Any) -> List[str]:
    image_container = coin_box.find("div", {"class": "coins"})
    images = image_container.find_all("img")

    return [
        ECB_BASE_URL + image["src"].removeprefix(".")
        for image in images
        if not image["src"].endswith(".html")
    ]


def _parse_circulation_date(
    box_content: Content, language: str, year: int, paragraph_index: int
) -> Tuple[Optional[datetime.date], Optional[str]]:
    parsed_datetime = dateparser.parse(
        box_content.raw_issuing_date, languages=[language]
    )
    if parsed_datetime is not None:
        return (parsed_datetime.date(), None)
    else:
        LOG.warning(
            f"({year}, {paragraph_index}) could not extract datetime from"
            f" given circulation date: '{box_content.raw_issuing_date}'. The string will be "
            f"stored inside the 'circulation_dates_info' attribute."
        )
        return (None, box_content.raw_issuing_date)


def _get_commemorative_coins(
    content: bytes, lang: str = "", year: int = START_YEAR
) -> List[TwoEuro]:
    soup = BeautifulSoup(content, "html.parser")
    coin_boxes_div = soup.find("div", {"class": "boxes"})

    if coin_boxes_div is None:
        LOG.error(
            f"({year}) could not find 'div' with class 'boxes'. No coins can be crawled!"
        )
        return []

    if coin_boxes_div is NavigableString:
        LOG.error(
            f"({year}) soup result is a NavigableString. No coins can be crawled!"
        )
        return []

    coin_boxes = cast(Tag, coin_boxes_div).find_all("div", {"class": "box"})
    assert len(coin_boxes)  == 30, len(coin_boxes)

    coins: List[TwoEuro] = []
    for paragraph_index, coin_box in enumerate(coin_boxes):
        box_content = _parse_content_fields(coin_box, year, paragraph_index)

        volume, volume_info = _parse_volume(box_content)

        circulation_date, circulation_date_info = _parse_circulation_date(
            box_content, lang, year, paragraph_index
        )

        # coin fall back country
        title_header = coin_box.find("h3")
        fall_back_country = _get_alpha2_country_from_string(
            title_header.text, year, paragraph_index, lang
        )
        if (
            fall_back_country is None
            and title_header.text.lower() != "euro area countries"
        ):
            LOG.warning(
                f"({year}, {paragraph_index}) no country object matched country "
                f"named: '{title_header.text}'"
            )

        image_urls = _parse_image_urls(coin_box)

        if len(image_urls) == 0:
            if fall_back_country is None:
                warning = (
                    f"({year}, {paragraph_index}) no image urls found and failed to "
                    f"parse fall back country name from h3 tag "
                    f"with content: '{title_header}'. Country and image default url"
                    "will be 'None'"
                )
                LOG.warning(warning)
                coinages = [
                    Coinage(
                        country=None,
                        country_info=warning,
                        image_default_url=None,
                        image_attribution="",
                        circulation_date=circulation_date,
                        circulation_date_info=circulation_date_info,
                        volume=volume,
                        volume_info=volume_info,
                    )
                ]
            else:
                warning = (
                    f"({year}, {paragraph_index}) Could not find any images for "
                    f"the coin feature: '{box_content.feature}'. Using fall back "
                    f"country from h3 tag: '{fall_back_country}'"
                )
                LOG.warning(warning)
                coinages = [
                    Coinage(
                        country=fall_back_country,
                        image_default_url=None,
                        image_default_url_info=warning,
                        image_attribution="",
                        circulation_date=circulation_date,
                        circulation_date_info=circulation_date_info,
                        volume=volume,
                        volume_info=volume_info,
                    )
                ]

        coinages: List[Coinage] = []
        for image_url in image_urls:
            country_alpha2 = None
            # /euro/coins/comm/shared/img/joint_comm_2009_Luxembourg_Face.jpg
            # try to extract the country out of the image file name
            searched_words: List[str] = []
            for word in reversed(
                image_url.rsplit(".", maxsplit=1)[0]
                .rsplit("/", maxsplit=1)[1]
                .split("_")
            ):
                searched_words.append(word)
                if word.isnumeric():
                    continue

                country_alpha2 = _get_alpha2_country_from_string(
                    word, year, paragraph_index, lang
                )
                if country_alpha2 is not None:
                    break
            else:
                # if no country_alpha2 could be extracted. Try to use the
                # fall back country
                if fall_back_country is not None:
                    country_alpha2 = fall_back_country
                else:
                    LOG.warning(
                        f"({year}, {paragraph_index}) no country object could be extracted "
                        f"from the given image file name tokens: '{searched_words}' and "
                        f"it also failed to parse "
                        f"fall back country name from h3 tag "
                        f"with content: '{title_header}'. Country "
                        "will be 'None'"
                    )

            coinages.append(
                Coinage(
                    country=country_alpha2,
                    image_default_url=image_url,
                    image_attribution="",
                    circulation_date=circulation_date,
                    circulation_date_info=circulation_date_info,
                    volume=volume,
                    volume_info=volume_info,
                )
            )

        coins.append(
            TwoEuro(
                feature=box_content.feature,
                description=box_content.description,
                coinages=coinages,
            )
        )
    return coins


if __name__ == "__main__":
    pprint.pprint(get_commemorative_coins("de", year=2006))
