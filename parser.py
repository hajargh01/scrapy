import re
from time import perf_counter
from urllib.parse import parse_qs, urlparse

from consultation import Consultation
from _selectors import selectors


def page_state(soup):
    return soup.select_one(selectors["pagestate"])["value"]


def get_id(url):
    return parse_qs(urlparse(url).query)["refConsultation"][0]


class ConsultationListParser:
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
        base_url = "https://www.marchespublics.gov.ma/index.php"
        for consultation in self.soup.select(selectors["consultations"]):
            ls.append(base_url + consultation["href"])
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

        dates_de_publication = self.dates_de_publication()
        references = self.references()
        objets = self.objets()
        acheteurs_publics = self.acheteurs_publics()
        lieux = self.lieux()
        dates_limites = self.dates_limites_de_remise_des_plis()
        pages = self.pages()
        urls = self.consultations()

        end = perf_counter()

        consultations = []

        for i in range(len(references)):
            consultation = Consultation(
                get_id(urls[i]),
                dates_de_publication[i],
                references[i],
                objets[i],
                acheteurs_publics[i],
                lieux[i],
                dates_limites[i],
                None,
                None,
                urls[i],
            )

            consultations.append(consultation)

        print(f"Parse consultations [page: {page}]: " f"{end - start}")

        return consultations


class DetailsConsultationParser:
    def __init__(self, soup):
        self.soup = soup

    def estimation(self):
        estimation = self.soup.select_one(selectors["estimation"])

        if estimation:
            return estimation.text.strip()

        return None

    def caution(self):
        caution = self.soup.select_one(selectors["caution"])

        if caution.text.strip() == "":
            return None

        return caution.text
