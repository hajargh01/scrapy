from parser import ConsultationListParser, DetailsConsultationParser
import threading
from time import perf_counter
from consultation import Consultation
import requests
from payload import p_data
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


def fetch_consultations(page):
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
        data=p_data(page),
    )
    end = perf_counter()
    print(f"Sent consultations POST request page {page}: {end - start}")
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


dates_de_publication = []
references = []
objets = []
acheteurs_publics = []
lieux = []
dates_limites_de_remise_des_plis = []
consultations = []


def consultation_page(page):
    global dates_de_publication, references, objets, acheteurs_publics, lieux, dates_limites_de_remise_des_plis, consultations

    start = perf_counter()

    response = fetch_consultations(page)

    test = BeautifulSoup(response.text, "html.parser")
    consultation_list_parser = ConsultationListParser(test)

    dates = consultation_list_parser.dates_de_publication()
    refs = consultation_list_parser.references()
    objs = consultation_list_parser.objets()
    acheteurs = consultation_list_parser.acheteurs_publics()
    lieux_page = consultation_list_parser.lieux()
    dates_limites = consultation_list_parser.dates_limites_de_remise_des_plis()
    consultations_page = consultation_list_parser.consultations()
    pages = consultation_list_parser.pages()

    end = perf_counter()

    print(f"Request and parse consultations [page: {page}]: " f"{end - start}")
    start = (page - 1) * 100
    end = start + 100

    dates_de_publication[start:end] = dates
    references[start:end] = refs
    objets[start:end] = objs
    acheteurs_publics[start:end] = acheteurs
    lieux[start:end] = lieux_page
    dates_limites_de_remise_des_plis[start:end] = dates_limites
    consultations[start:end] = consultations_page

    return pages


pages = consultation_page(1)

threads = []

start = perf_counter()

for page in range(2, pages + 1):
    thread = threading.Thread(
        target=consultation_page,
        args=(page,),
    )

    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end = perf_counter()
print(f"Request and parse consultations pages " f"{end - start}")

estimations = [None] * len(references)
cautions = [None] * len(references)
page = 1
sum_request = 0
sum_parsing = 0


def process_consultation(url, index):
    global sum_request, sum_parsing

    start = perf_counter()
    response = fetch_details_consultation(url)

    test = BeautifulSoup(response.text, "html.parser")
    details_consultation_parser = DetailsConsultationParser(test)

    estimation = details_consultation_parser.estimation()
    caution = details_consultation_parser.caution()

    end = perf_counter()

    print(f"Request and parse details consultation [#: {index+1}]: {end - start}")

    estimations[index] = estimation
    cautions[index] = caution


threads = []

for i in range(len(consultations)):
    thread = threading.Thread(
        target=process_consultation,
        args=(consultations[i], i),
    )
    threads.append(thread)
start = perf_counter()
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
end = perf_counter()
print(f"Request and parse details consultation pages: {end - start}")

# i*page -> page[1];
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

# for cons in data_consultation:
#     print(cons.date_publication)
#     print(cons.reference)
#     print(cons.date_limite)
#     print(cons.acheteurs_public)
#     print(cons.objet)
#     print(cons.lieux)
