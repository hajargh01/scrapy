from datetime import datetime
from time import perf_counter
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

from consultation import Consultation
from helpers import parse_number
from marchespublics._selectors import selectors


def page_state(soup):
    return soup.select_one(selectors["pagestate"])["value"]


def get_id(url):
    return f'marchespublics:{parse_qs(urlparse(url).query)["refConsultation"][0]}'

months = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}

class ConsultationListParser:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def references(self):
        ls = []
        for reference in self.soup.select(selectors["references"]):
            ls.append(reference.text)
        return ls

    def objets(self):
        ls = []
        for _object in self.soup.select(selectors["objets"]):
            ls.append(_object.contents[2].text.strip())
        return ls

    def acheteurs_publics(self):
        ls = []
        for acheteur in self.soup.select(selectors["acheteurs_publics"]):
            ls.append(acheteur.contents[1].contents[2].text.strip())
        return ls

    def lieux(self):
        ls = []
        for lieu in self.soup.select(selectors["lieux"]):
            ls.append(lieu.text.split("\n\r")[0].strip())
        return ls

    def dates_limites_de_remise_des_plis(self):
        ls = []
        for i in self.soup.select(selectors["dates_limites_de_remise_des_plis"]):
            date = i.contents[1].text.strip()

            day, month, year = date.split(' ')[1:]
            month = months[month]

            time = i.contents[3].text.strip()

            ls.append(datetime.strptime(f"{day}/{month}/{year} {time}", "%d/%m/%Y %H:%M"))
            print()
        return ls

    def estimations(self):
        ls = []
        for estimation in self.soup.select(selectors["estimations"]):
            if estimation.text.strip() == '':
                ls.append(None)
            else:
                ls.append(parse_number(estimation.text.strip()))
        return ls

    def consultations(self):
        ls = []
        for consultation in self.soup.select(selectors["consultations"]):
            ls.append(consultation["onclick"].split("\"")[1])
        return ls

    def pages(self):
        tag = self.soup.select_one(selectors["pages"])
        if tag is None:
            return 1
        return int(self.soup.select_one(selectors["pages"]).text)

    def collect_consultation_page(
        self,
        page,
    ):

        start = perf_counter()

        references = self.references()
        objets = self.objets()
        acheteurs_publics = self.acheteurs_publics()
        lieux = self.lieux()
        dates_limites = self.dates_limites_de_remise_des_plis()
        estimations = self.estimations()
        self.pages()
        urls = self.consultations()

        end = perf_counter()

        consultations = []

        for i in range(len(references)):
            consultation = Consultation()
            consultation.id = get_id(urls[i])
            consultation.reference = references[i]
            consultation.objet = objets[i]
            consultation.acheteur_public = acheteurs_publics[i]
            consultation.lieu = lieux[i]
            consultation.date_limite = dates_limites[i]
            consultation.estimation = estimations[i]
            consultation.url = urls[i]
            consultation.portail = 'marchespublics'

            consultations.append(consultation)

        print(f"Parse consultations [page: {page}]: " f"{end - start}")

        return consultations


class DetailsConsultationParser:
    def __init__(self, soup):
        self.soup = soup

    def caution(self):
        caution = self.soup.select_one(selectors["caution"])

        if caution is None:
            return None

        return float(parse_number(caution.text.replace("MAD", "")))
