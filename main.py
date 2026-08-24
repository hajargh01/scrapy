import os

from dotenv import load_dotenv
from openai import OpenAI

import repository
from _request import fetch_details_consultation, open_search_form, post_search
from ai import Results, SYSTEM
from parser import ConsultationListParser, DetailsConsultationParser, page_state
import threading
from time import perf_counter
from payload import (
    next_page_data,
    page_size_data,
    search_data,
)
from bs4 import BeautifulSoup

load_dotenv()

consultations = []


start = perf_counter()

response = open_search_form()
soup = BeautifulSoup(response.text, "html.parser")
response = post_search(search_data(page_state(soup)), "search")
soup = BeautifulSoup(response.text, "html.parser")
response = post_search(page_size_data(page_state(soup)), "page size")
soup = BeautifulSoup(response.text, "html.parser")

parser = ConsultationListParser(soup)
pages = parser.pages()
consultation = parser.collect_consultation_page(1)
consultations += consultation

for page in range(2, pages + 1):
    response = post_search(next_page_data(page_state(soup)), f"page {page}")

    soup = BeautifulSoup(response.text, "html.parser")

    parser = ConsultationListParser(soup)
    consultations_page = parser.collect_consultation_page(page)

    consultations += consultations_page

end = perf_counter()

print(f"Request and parse consultations pages: {end - start}")


def process_consultation(consultation, index):
    start = perf_counter()
    response = fetch_details_consultation(consultation.url)

    test = BeautifulSoup(response.text, "html.parser")
    details_consultation_parser = DetailsConsultationParser(test)

    estimation = details_consultation_parser.estimation()
    caution = details_consultation_parser.caution()

    end = perf_counter()

    print(f"Request and parse details consultation [#: {index+1}]: {end - start}")

    consultation.estimation = estimation
    consultation.caution = caution


stored = repository.read()

for consultation in consultations:
    if consultation.id in stored:
        consultation.estimation = stored[consultation.id]["estimation"]
        consultation.caution = stored[consultation.id]["caution"]

threads = []

for i in range(len(consultations)):
    if consultations[i].id in stored:
        continue
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

ls = []
for consultation in consultations:
    if consultation.id not in stored:
        ls.append(
            f"[{consultation.id}]\nObjet : {consultation.objet}\nAcheteur : {consultation.acheteurs_public}"
        )


user = "\n\n".join(ls)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.parse(
    model="gpt-5.6",
    input=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
    ],
    text_format=Results,
)

for consultation in consultations:
    if consultation.id not in stored:
        for result in response.output_parsed.results:
            if consultation.id == result.id:
                consultation.domaines = result.domaines
                consultation.justification = result.justification
                consultation.confidence = result.confidence


repository.write(consultations)

print(f" nbr cons {len(consultations)}")
