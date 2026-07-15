import re

from _selectors import selectors
import requests


class Parser:
    def __init__(self, soup):
        self.soup = soup

    def dates_de_publication(self):
        ls = []
        for _date in self.soup.select(selectors["dates_de_publication"]):
            ls.append(_date.text.strip())
        return ls

    def references(self):
        ls = []
        for reference in self.soup.select(selectors["references"]):
            ls.append(reference.text)
        return ls

    def objets(self):
        ls = []
        for _object in self.soup.select(selectors["objets"]):
            ls.append(_object.text.strip())
        return ls

    def acheteurs_publics(self):
        ls = []
        for acheteur in self.soup.select(selectors["acheteurs_publics"]):
            ls.append(acheteur.contents[-1].text.strip())
        return ls

    def lieux(self):
        ls = []
        for lieu in self.soup.select(selectors["lieux"]):
            ls.append(lieu.contents[0].text.strip())
        return ls

    def dates_limites_de_remise_des_plis(self):
        ls = []
        for i in self.soup.select(selectors["dates_limites_de_remise_des_plis"]):
            s = i.contents[1].text.strip()
            date, time = re.match(r"(.*?)(\d{1,2}:\d{2})$", s).groups()
            ls.append({"date": date, "time": time})
        return ls

    def consultations(self):
        ls = []
        for consultation in self.soup.select(selectors["consultations"]):
            ls.append(consultation["href"])
        return ls


def consultation_page(self, consultation):

    response = requests.get(
        "https://www.marchespublics.gov.ma/index.php" + consultation,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
        },
    )
    return response
