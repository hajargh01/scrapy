import csv

def write(consultations):
    with open("consultations.csv", "a", newline="", encoding="utf-8-sig") as csvfile:
        fieldnames = [
            "id",
            "reference",
            "objet",
            "acheteurs_public",
            "lieux",
            "date_limite",
            "estimation",
            "caution",
            "url",
            "portail",
            "domaines",
            "justification",
            "confidence",
        ]

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
        )

        # writer.writeheader()

        for consultation in consultations:
            writer.writerow(
                {
                    "id": consultation.id,
                    "reference": consultation.reference,
                    "objet": consultation.objet,
                    "acheteurs_public": consultation.acheteur_public,
                    "lieux": consultation.lieu,
                    "date_limite": consultation.date_limite.isoformat(timespec="minutes"),
                    "estimation": consultation.estimation,
                    "caution": consultation.caution,
                    "url": consultation.url,
                    "portail": consultation.portail,
                    "domaines": "|".join(consultation.domaines),
                    "justification": consultation.justification,
                    "confidence": consultation.confidence,
                }
            )
