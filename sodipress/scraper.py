from bs4 import BeautifulSoup

from consultation import Consultation
from sodipress._request import login_form, login, fetch_consultations
from sodipress.parser import get_token, ConsultationParser


def consultations():
    consultations_list: list[Consultation] = []

    response = login_form()
    token = get_token(response.text)

    if token:
        login(token)

        response = fetch_consultations(page=1)

        soup = BeautifulSoup(response.text, "html.parser")
        parser = ConsultationParser(soup)
        pages = parser.pages()

        # page 1
        cards = soup.select("div.card.card-dashed")
        for card in cards:
            parser = ConsultationParser(card)
            consultations_list.append(parser.consultation())

        for page in range(2, pages + 1):
            response = fetch_consultations(page=page)
            soup = BeautifulSoup(response.text, "html.parser")

            # page x
            cards = soup.select("div.card.card-dashed")
            for card in cards:
                parser = ConsultationParser(card)
                consultations_list.append(parser.consultation())

    return consultations_list
