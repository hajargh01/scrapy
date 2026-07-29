from parser import ConsultationListParser, DetailsConsultationParser
import requests
from payload import data
from bs4 import BeautifulSoup


def fetch_consultations():
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
    return response


def fetch_details_consultation(url):
    response = requests.get(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
        },
    )
    return response


soup = BeautifulSoup(fetch_consultations().text, "html.parser")
consultation_list_parser = ConsultationListParser(soup)

dates_de_publication = consultation_list_parser.dates_de_publication()
references = consultation_list_parser.references()
objets = consultation_list_parser.objets()
acheteurs_publics = consultation_list_parser.acheteurs_publics()
lieux = consultation_list_parser.lieux()
dates_limites_de_remise_des_plis = (
    consultation_list_parser.dates_limites_de_remise_des_plis()
)
consultations = consultation_list_parser.consultations()

test = BeautifulSoup(fetch_details_consultation(consultations[1]).text, "html.parser")
details_consultation_parser = DetailsConsultationParser(test)

estimation = details_consultation_parser.estimation()
caution = details_consultation_parser.caution()
print()
