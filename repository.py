import csv
from urllib.parse import parse_qs, urlparse

from parser import get_id


def read():
    stored = {}

    with open("consultations.csv", newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            stored[row["url"]] = {
                "estimation": row["estimation"],
                "caution": row["caution"],
            }

    return stored


def write(consultations):
    with open("consultations.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
        fieldnames = [
            "id",
            "date_publication",
            "reference",
            "objet",
            "acheteurs_public",
            "lieux",
            "date_limite",
            "estimation",
            "caution",
            "url",
        ]

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for cons in consultations:
            writer.writerow(
                {
                    "id": get_id(cons.url),
                    "date_publication": cons.date_publication,
                    "reference": cons.reference,
                    "objet": cons.objet,
                    "acheteurs_public": cons.acheteurs_public,
                    "lieux": cons.lieux,
                    "date_limite": cons.date_limite,
                    "estimation": cons.estimation,
                    "caution": cons.caution,
                    "url": cons.url,
                }
            )
