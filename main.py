from parser import ConsultationListParser, DetailsConsultationParser, page_state
import threading
from time import perf_counter
from consultation import Consultation
import requests
from payload import (
    FORM_URL,
    SEARCH_URL,
    next_page_data,
    page_size_data,
    search_data,
)
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


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)


def post_search(data, label):
    start = perf_counter()
    response = session.post(
        SEARCH_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
        },
        data=data,
    )
    end = perf_counter()
    print(f"Sent consultations POST request [{label}]: {end - start}")
    return BeautifulSoup(response.text, "html.parser")


def open_search_form():
    start = perf_counter()
    response = session.get(FORM_URL, headers={"User-Agent": USER_AGENT})
    end = perf_counter()
    print(f"Sent search form GET request: {end - start}")
    return BeautifulSoup(response.text, "html.parser")


def fetch_details_consultation(url):
    start = perf_counter()
    response = session.get(url, headers={"User-Agent": USER_AGENT})
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


def collect_consultation_page(soup, page):
    global dates_de_publication, references, objets, acheteurs_publics, lieux, dates_limites_de_remise_des_plis, consultations

    start = perf_counter()

    consultation_list_parser = ConsultationListParser(soup)

    dates_de_publication += consultation_list_parser.dates_de_publication()
    references += consultation_list_parser.references()
    objets += consultation_list_parser.objets()
    acheteurs_publics += consultation_list_parser.acheteurs_publics()
    lieux += consultation_list_parser.lieux()
    dates_limites_de_remise_des_plis += (
        consultation_list_parser.dates_limites_de_remise_des_plis()
    )
    consultations += consultation_list_parser.consultations()
    pages = consultation_list_parser.pages()

    end = perf_counter()

    print(f"Parse consultations [page: {page}]: " f"{end - start}")

    return pages


start = perf_counter()

soup = open_search_form()
soup = post_search(search_data(page_state(soup)), "search")
soup = post_search(page_size_data(page_state(soup)), "page size")

pages = collect_consultation_page(soup, 1)

for page in range(2, pages + 1):
    soup = post_search(next_page_data(page_state(soup)), f"page {page}")
    collect_consultation_page(soup, page)

end = perf_counter()

print(f"Request and parse consultations pages: {end - start}")

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
