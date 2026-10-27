import requests

import config

session = requests.session()


def login_form():
    return session.get("https://client.sodipress.com/Account/Login")


def login(token):
    session.post(
        "https://client.sodipress.com/Account/Login",
        data={
            "username": "Cegelec",
            "password": "cegelec2014",
            "__RequestVerificationToken": token,
            "ReturnUrl": "/",
        },
    )


def fetch_consultations(page):
    return session.post(
        "https://client.sodipress.com/MesMarches/ResultatsMesMarchesByPage",
        data={
            "Listeactivite[]": ["1015", "1016", "2001", "4003"],
            "Nordre": "",
            "Nappeloffre": "",
            "operateur[]": ["0", "0"],
            "motcle[]": ["", "", ""],
            "dateparutiondebut": config.FROM,
            "dateparutionfin": config.TO,
            "datelimitedebut": "",
            "datelimitefin": "",
            "idregion": "-1",
            "reservepme": "on",
            "qualificationavec": "on",
            "AvecDao": "false",
            "caution": "",
            "operateurcaution": "<=",
            "estimation": "",
            "operateurestimation": "<=",
            "typeReponse": "",
            "publics": "true",
            "rectif": "",
            "pvvisite": "on",
            "trierPar": "dateparution",
            "sortDirection": "desc",
            "periode": "",
            "PageSize": "50",
            "pg": page,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
