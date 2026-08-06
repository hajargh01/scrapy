from parser import ConsultationListParser, DetailsConsultationParser
import threading
from time import perf_counter
from consultation import Consultation
import requests
from payload import data
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
session.mount("https://", HTTPAdapter(max_retries=retries, pool_maxsize=10))


def fetch_consultations():
    start = perf_counter()
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
    end = perf_counter()
    print("Sent consultations POST request: ", end - start)
    return response


def fetch_details_consultation(url):
    start = perf_counter()
    response = session.get(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
        },
    )
    end = perf_counter()
    print(f"Sent details consultation GET request: {end - start}")
    return response


start = perf_counter()

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

end = perf_counter()
print("Parsed consultations page: ", end - start)


estimations = []
cautions = []
page = 1
sum_request = 0
sum_parsing = 0


def process_consultation(url):
    global page, sum_request, sum_parsing

    start = perf_counter()
    response = fetch_details_consultation(url)
    end = perf_counter()
    sum_request += end - start

    start = perf_counter()
    test = BeautifulSoup(response.text, "html.parser")
    details_consultation_parser = DetailsConsultationParser(test)

    estimation = details_consultation_parser.estimation()
    caution = details_consultation_parser.caution()

    end = perf_counter()
    sum_parsing += end - start

    print(f"Parsed details consultation [page: {page}]: {end - start}")

    estimations.append(estimation)
    cautions.append(caution)

    page += 1


threads = []

for url in consultations:
    thread = threading.Thread(
        target=process_consultation,
        args=(url,),
    )
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f"Sent details consultation GET requests: {sum_request}")
print(f"Parsed details consultation pages: {sum_parsing}")


data_consultation: list[Consultation] = []
for i in range(len(references)):
    consultation = Consultation(
        dates_de_publication[i],
        references[i],
        objets[i],
        acheteurs_publics[i],
        lieux[i],
        dates_limites_de_remise_des_plis[i],
        estimations[i],
        cautions[i],
    )
    data_consultation.append(consultation)
#
# for cons in data_consultation:
#     print(cons.date_publication)
#     print(cons.reference)
#     print(cons.date_limite)
#     print(cons.acheteurs_public)
#     print(cons.objet)
#     print(cons.lieux)
