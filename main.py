import os

from dotenv import load_dotenv
from openai import OpenAI

import repository
from ai import Results, SYSTEM

import marchespublics.scraper
import sodipress.scraper
from consultation import Consultation

load_dotenv()

consultations: list[Consultation] = []

consultations += marchespublics.scraper.consultations()
consultations += sodipress.scraper.consultations()

# AI
ls = []
for consultation in consultations:
    ls.append(
        f"[{consultation.id}]\nObjet : {consultation.objet}\nAcheteur : {consultation.acheteur_public}"
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
    for result in response.output_parsed.results:
        if consultation.id == result.id:
            consultation.domaines = result.domaines
            consultation.justification = result.justification
            consultation.confidence = result.confidence


repository.write(consultations)

print(f" nbr cons {len(consultations)}")
