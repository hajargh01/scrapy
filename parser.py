import re

from _selectors import selectors


def page_state(soup):
    return soup.select_one(selectors["pagestate"])["value"]


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
        return int(self.soup.select_one(selectors["pages"]).text)


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
