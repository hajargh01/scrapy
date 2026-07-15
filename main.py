from parser import Parser
import requests
from payload import data
from bs4 import BeautifulSoup

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

soup = BeautifulSoup(response.text, "html.parser")
parser = Parser(soup)

dates_de_publication = parser.dates_de_publication()
references = parser.references()
objets = parser.objets()
acheteurs_publics = parser.acheteurs_publics()
lieux = parser.lieux()
dates_limites_de_remise_des_plis = parser.dates_limites_de_remise_des_plis()
consultations = parser.consultations()
print()
