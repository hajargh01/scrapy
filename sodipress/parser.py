from datetime import datetime

from bs4 import BeautifulSoup, Tag
from bs4.element import AttributeValueList

from sodipress._selectors import selectors
from consultation import Consultation
from helpers import parse_number
from math import ceil

def get_token(html: str) -> str | AttributeValueList | None:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.select_one("input[name=__RequestVerificationToken]")

    if tag:
        return tag.get("value")

    return None


class ConsultationParser:
    def __init__(self, tag: Tag):
        self.tag = tag

    def numero_ordre(self) -> str | None:
        if tag := self.tag.find(string="N°Ordre"):
            if tag := tag.find_next("span"):
                return f'{tag.text}'
        return None

    def date_de_publication(self) -> datetime | None:
        tag = self.tag.select(".text-muted.text-hover-primary.font-weight-bold")[0]

        if tag:
            return datetime.strptime(tag.text.strip(), "%d/%m/%Y")

        return None

    def reference(self) -> str | None:
        if tag := self.tag.find(string="N° AO "):
            if tag := tag.find_next("span"):
                return tag.text.strip()

        return None

    def objet(self) -> str | None:
        tag = self.tag.select_one(
            ".flex-grow-1.font-weight-bolder.font-size-h5.py-2.py-lg-2.mr-5"
        )

        if tag:
            return tag.text.strip()

        return None

    def acheteur_public(self) -> str | None:
        tag = self.tag.select_one(".DetailAO")

        if tag:
            return tag.text.strip()

        return None

    def lieu(self) -> str | None:
        tag = self.tag.select(".text-muted.text-hover-primary.font-weight-bold")[2]

        if tag:
            return tag.text.strip()

        return None

    def date_limite(self) -> datetime | None:
        date: str | None = None

        if tag := self.tag.find(string="Date Limite a été reportée"):
            if tag := tag.find_next("span"):
                date = tag.text.strip()
        elif tag := self.tag.find(string="Date Limite"):
            if tag := tag.find_next("span"):
                date = tag.text.strip()

        if date:
            try:
                return datetime.strptime(date.strip(), "%d/%m/%Y - %H:%M")

            except ValueError:
                try:
                    return datetime.strptime(date.strip(), "%d/%m/%Y")
                except ValueError:
                    return datetime.strptime(date.strip()[:-2], "%d/%m/%Y")

        return None

    def estimation(self) -> float:
        try:
            if tag := self.tag.find(name="span", string="Estimation"):
                if tag := tag.find_next("span"):
                    return parse_number(tag.text)

            return 0
        except IndexError:
            return 0

    def caution(self) -> float:
        try:
            if tag := self.tag.find(name="span", string="Caution"):
                if tag := tag.find_next("span"):
                    parse_number(tag.text)

            return 0

        except IndexError:
            return 0

    def url(self) -> str:
        return f'https://client.sodipress.com/MesMarches/Printing/{self.numero_ordre()}'

    def consultation(self) -> Consultation:
        consultation = Consultation()

        consultation.id = f'sodipress:{self.numero_ordre()}'
        consultation.date_publication = self.date_de_publication()
        consultation.reference = self.reference()
        consultation.objet = self.objet()
        consultation.acheteur_public = self.acheteur_public()
        consultation.lieu = self.lieu()
        consultation.date_limite = self.date_limite()
        consultation.estimation = self.estimation()
        consultation.caution = self.caution()
        consultation.url = self.url()
        consultation.portail = 'sodipress'

        return consultation

    def pages(self) -> int:
        count = self.tag.select_one(selectors["count"])
        if count:
            return ceil(int(count.text) / 50)
        return 0
