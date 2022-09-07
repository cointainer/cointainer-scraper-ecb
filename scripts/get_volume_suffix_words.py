from time import sleep
from typing import cast
from bs4.element import Tag
import requests
from bs4 import BeautifulSoup

# words = []
# for lang in [
#     {"bg": "Български"},
#     {"cs": "Čeština"},
#     {"da": "Dansk"},
#     {"de": "Deutsch"},
#     {"el": "Eλληνικά"},
#     {"en": "English"},
#     {"es": "Español"},
#     {"et": "Eesti keel"},
#     {"fi": "Suomi"},
#     {"fr": "Français"},
#     {"hr": "Hrvatski"},
#     {"hu": "Magyar"},
#     {"it": "Italiano"},
#     {"lt": "Lietuvių"},
#     {"lv": "Latviešu"},
#     {"mt": "Malti"},
#     {"nl": "Nederlands"},
#     {"pl": "Polski"},
#     {"pt": "Português"},
#     {"ro": "Română"},
#     {"sk": "Slovenčina"},
#     {"sl": "Slovenščina"},
#     {"sv": "Svenska"},
# ]:
#     key = list(lang.keys())[0]
#     response = requests.get(f"https://www.ecb.europa.eu/euro/coins/comm/html/comm_2005.{key}.html")
#     soup = BeautifulSoup(response.content, "html.parser")
#     coin_boxes_div = soup.find("div", {"class": "boxes"})
#     coin_boxes = cast(Tag, coin_boxes_div).find_all("div", {"class": "box"})
#     word = coin_boxes[3].find_all("p")[2].text.replace("\xa0", " ").split(" ")
#     words.append(word)
#     sleep(2)

# print(words)







# non million

words = []
for lang in [
    {"bg": "Български"},
    {"cs": "Čeština"},
    {"da": "Dansk"},
    {"de": "Deutsch"},
    {"el": "Eλληνικά"},
    {"en": "English"},
    {"es": "Español"},
    {"et": "Eesti keel"},
    {"fi": "Suomi"},
    {"fr": "Français"},
    {"hr": "Hrvatski"},
    {"hu": "Magyar"},
    {"it": "Italiano"},
    {"lt": "Lietuvių"},
    {"lv": "Latviešu"},
    {"mt": "Malti"},
    {"nl": "Nederlands"},
    {"pl": "Polski"},
    {"pt": "Português"},
    {"ro": "Română"},
    {"sk": "Slovenčina"},
    {"sl": "Slovenščina"},
    {"sv": "Svenska"},
]:
    key = list(lang.keys())[0]
    response = requests.get(f"https://www.ecb.europa.eu/euro/coins/comm/html/comm_2005.{key}.html")
    soup = BeautifulSoup(response.content, "html.parser")
    coin_boxes_div = soup.find("div", {"class": "boxes"})
    coin_boxes = cast(Tag, coin_boxes_div).find_all("div", {"class": "box"})
    word = coin_boxes[0].find_all("p")[2].text.replace("\xa0", " ").split(" ")
    words.append(word)
    sleep(2)

print(words)

exit()




# words = [
#   ["Тираж:", "18", "милиона", "монети"],
#   ["Objem", "emise:", "18", "milionů", "mincí"],
#   ["Antal:", "18", "mio.", "mønter"],
#   ["Ausgabevolumen:", "18", "Millionen", "Münzen"],
#   ["Ποσότητα:", "18", "εκατομμύρια", "κέρματα"],
#   ["Issuing", "volume:", "18", "million", "coins", ""],
#   ["Volumen", "de", "emisión:", "18", "millones", "de", "monedas"],
#   ["Emissiooni", "maht:", "18", "miljonit", "münti"],
#   [
#     "Liikkeeseen",
#     "laskettujen",
#     "rahojen",
#     "määrä:",
#     "18",
#     "miljoonaa",
#     "kolikkoa"
#   ],
#   ["Volume", "d’émission", ":", "18", "millions", "de", "pièces"],
#   ["Opseg", "izdanja:", "18", "000", "000", "kovanica"],
#   ["A", "kibocsátás", "mennyisége:", "18", "millió", "érme"],
#   ["Tiratura:", "18", "milioni", "di", "pezzi"],
#   ["Tiražas:", "18", "mln.", "monetų"],
#   ["Emisijas", "apjoms:", "18", "milj.", "monētu"],
#   ["Volum", "tal-ħruġ:", "18-il", "miljun", "munita"],
#   ["Oplage:", "18", "miljoen", "munten"],
#   ["Nakład:", "18", "milionów", "monet"],
#   ["Volume", "de", "emissão:", "18", "milhões", "de", "moedas"],
#   ["Tirajul", "emisiunii:", "18", "milioane", "de", "monede"],
#   ["Náklad:", "18", "miliónov", "mincí"],
#   ["Obseg", "izdaje:", "18", "milijonov", "kovancev"],
#   ["Upplaga:", "18", "miljoner", "mynt"]
# ]

words = [['Тираж:', '2', 'милиона', 'монети'], ['Objem', 'emise:', '2', 'miliony', 'mincí'], ['Antal:', '2', 'mio.', 'mønter'], ['Ausgabevolumen:', '2', 'Millionen', 'Münzen'], ['Ποσότητα:', '2', 'εκατομμύρια', 'κέρματα'], ['Issuing', 'volume:', '2', 'million', 'coins', ''], ['Volumen', 'de', 'emisión:', '2', 'millones', 'de', 'monedas'], ['Emissiooni', 'maht:', '2', 'miljonit', 'münti'], ['Liikkeeseen', 'laskettujen', 'rahojen', 'määrä:', '2', 'miljoonaa', 'kolikkoa'], ['Volume', 'd’émission', ':', '2', 'millions', 'de', 'pièces'], ['Opseg', 'izdanja:', '2', '000', '000', 'kovanica'], ['A', 'kibocsátás', 'mennyisége:', '2', 'millió', 'érme'], ['Tiratura:', '2', 'milioni', 'di', 'pezzi'], ['Tiražas:', '2', 'mln.', 'monetų'], ['Emisijas', 'apjoms:', '2', 'milj.', 'monētu'], ['Volum', 'tal-ħruġ:', '2-il', 'miljun', 'munita'], ['Oplage:', '2', 'miljoen', 'munten'], ['Nakład:', '2', 'miliony', 'monet'], ['Volume', 'de', 'emissão:', '2', 'milhões', 'de', 'moedas'], ['Tirajul', 'emisiunii:', '2', 'milioane', 'de', 'monede'], ['Náklad:', '2', 'milióny', 'mincí'], ['Obseg', 'izdaje:', '2', 'milijona', 'kovancev'], ['Upplaga:', '2', 'miljoner', 'mynt']]

mapping = {}
for word in words:
    filtered_word = []
    for c in reversed(word):
        if "2" in c:
            break
        
        filtered_word.append(c)

    key = " ".join(reversed(filtered_word))
    mapping[key] = 1_000_000

print(mapping)




words = [['Тираж:', '100', '000', 'монети'], ['Objem', 'emise:', '100', '000', 'mincí'], ['Antal:', '100.000', 'mønter'], ['Ausgabevolumen:', '100', '000', 'Münzen'], ['Ποσότητα:', '100.000', 'κέρματα'], ['Issuing', 'volume:', '100,000', 'coins', ''], ['Volumen', 'de', 'emisión:', '100', '000', 'monedas'], ['Emissiooni', 'maht:', '100', '000', 'münti'], ['Liikkeeseen', 'laskettujen', 'rahojen', 'määrä:', '100', '000', 'kolikkoa'], ['Volume', 'd’émission', ':', '100', '000', 'pièces'], ['Opseg', 'izdanja:', '100', '000', 'kovanica'], ['A', 'kibocsátás', 'mennyisége:', '100', '000', 'érme'], ['Tiratura:', '100.000', 'pezzi'], ['Tiražas:', '100', '000', 'monetų'], ['Emisijas', 'apjoms:', '100', '000', 'monētu'], ['Volum', 'tal-ħruġ:', '100,000', 'munita'], ['Oplage:', '100.000', 'munten'], ['Nakład:', '100', '000', 'monet'], ['Volume', 'de', 'emissão:', '100', 'mil', 'moedas'], ['Tirajul', 'emisiunii:', '100', '000', 'de', 'monede'], ['Náklad:', '100', '000', 'mincí'], ['Obseg', 'izdaje:', '100.000', 'kovancev'], ['Upplaga:', '100', '000', 'mynt']]
