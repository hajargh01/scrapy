import re

import requests
from payload import data
from bs4 import BeautifulSoup

response = requests.post(
    "https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseAdvancedSearch&searchAnnCons",
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
    },
    data=data,
)
text = response.text
with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)
# with open("index.html", encoding="utf-8") as f:
#     text = f.read()

soup = BeautifulSoup(text, "html.parser")

selectors = {
    "publie_le": "[headers=cons_ref] div:nth-child(4)",
    "references": "[headers=cons_intitule] .ref",
    "objets": "[headers=cons_intitule] .info-bulle",
    "achteurs_publiques": "[headers=cons_intitule] .objet-line:nth-child(3)",
    "lieux": "[headers=cons_lieuExe] > div > div:nth-of-type(1)",
    "date_limite_de_remise_des_plis": "[headers=cons_dateEnd] > div:nth-of-type(1)",
}


def publie_le():
    ls = []
    for _date in soup.select(selectors["publie_le"]):
        ls.append(_date.text.strip())
    return ls


def references():
    ls = []
    for reference in soup.select(selectors["references"]):
        ls.append(reference.text)
    return ls


def objets():
    ls = []
    for _object in soup.select(selectors["objets"]):
        ls.append(_object.text.strip())
    return ls


def achteurs_publiques():
    ls = []
    for _achteur in soup.select(selectors["achteurs_publiques"]):
        ls.append(_achteur.contents[-1].text.strip())
    return ls


def lieux():
    ls = []
    for lieu in soup.select(selectors["lieux"]):
        ls.append(lieu.contents[0].text.strip())
    return ls


def date_limite_de_remise_des_plis():
    ls = []
    for i in soup.select(selectors["date_limite_de_remise_des_plis"]):
        s = i.contents[1].text.strip()
        date, time = re.match(r"(.*?)(\d{1,2}:\d{2})$", s).groups()
        ls.append({"date": date, "time": time})
    return ls
