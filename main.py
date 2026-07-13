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
dates = soup.select("[headers=cons_ref] div:nth-child(4)")
l = []
for date in dates:
    l.append(date.text.strip())
references = soup.select("[headers=cons_intitule] .ref")
R = []
for reference in references:
    R.append(reference.text)
objects = soup.select("[headers=cons_intitule] .info-bulle")
O = []
for _object in objects:
    O.append(_object.text.strip())
achteursPubliques = soup.select("[headers=cons_intitule] .objet-line:nth-child(3)")

A = []
for _achteur in achteursPubliques:
    A.append(_achteur.contents[-1].text.strip())

lieux = soup.select("[headers=cons_lieuExe] > div > div:nth-of-type(1)")

L = []

for lieu in lieux:
    L.append(lieu.contents[0].text.strip())

datesr = soup.select("[headers=cons_dateEnd] > div:nth-of-type(1)")

DR = []

for i in datesr:
    s = i.contents[1].text.strip()
    date, time = re.match(r"(.*?)(\d{1,2}:\d{2})$", s).groups()
    DR.append({"date": date, "time": time})
