import re

from selectors import selectors


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
