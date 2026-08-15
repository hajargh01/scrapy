from _request import fetch_details_consultation, open_search_form, post_search
from parser import ConsultationListParser, DetailsConsultationParser, page_state
import threading
from time import perf_counter
from consultation import Consultation
from payload import (
    next_page_data,
    page_size_data,
    search_data,
)
from bs4 import BeautifulSoup

dates_de_publication = []
references = []
objets = []
acheteurs_publics = []
lieux = []
dates_limites_de_remise_des_plis = []
consultations = []


start = perf_counter()

response = open_search_form()
soup = BeautifulSoup(response.text, "html.parser")
response = post_search(search_data(page_state(soup)), "search")
soup = BeautifulSoup(response.text, "html.parser")
response = post_search(page_size_data(page_state(soup)), "page size")
soup = BeautifulSoup(response.text, "html.parser")

parser = ConsultationListParser(soup)
pages = parser.collect_consultation_page(
    1,
    dates_de_publication,
    references,
    objets,
    acheteurs_publics,
    lieux,
    dates_limites_de_remise_des_plis,
    consultations,
)

for page in range(2, pages + 1):
    soup = post_search(next_page_data(page_state(soup)), f"page {page}")
    parser = ConsultationListParser
    parser.collect_consultation_page(
        page,
        dates_de_publication,
        references,
        objets,
        acheteurs_publics,
        lieux,
        dates_limites_de_remise_des_plis,
        consultations,
    )

end = perf_counter()

print(f"Request and parse consultations pages: {end - start}")

estimations = [None] * len(references)
cautions = [None] * len(references)
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
