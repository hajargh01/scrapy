import requests
from payload import data
from bs4 import BeautifulSoup

# response = requests.post(
#     "https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseAdvancedSearch&searchAnnCons",
#     headers={
#         "Content-Type": "application/x-www-form-urlencoded",
#         "User-Agent": (
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#             "AppleWebKit/537.36 (KHTML, like Gecko) "
#             "Chrome/125.0.0.0 Safari/537.36"
#         ),
#     },
#     data=data,
# )
# text = response.text
# with open("index.html", "w", encoding="utf-8") as f:
#     f.write(text)
with open("index.html", encoding="utf-8") as f:
    text = f.read()

soup = BeautifulSoup(text, "html.parser")
dates = soup.select("[headers=cons_ref] div:nth-child(4)")
l = []
for date in dates:
    l.append(date.text.strip())
references = soup.select("[headers=cons_intitule] .ref")
R = []
for reference in references:
    R.append(reference.text)
objects = soup.select("[headers=cons_intitule] div:nth-child(2) div")
O = []
for _object in objects:
    O.append(_object.text)

