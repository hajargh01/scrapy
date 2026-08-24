from enum import Enum

from pydantic import BaseModel, Field


class Domaine(str, Enum):
    MATERIEL_INFORMATIQUE = "MATERIEL_INFORMATIQUE"
    LOGICIEL_SI = "LOGICIEL_SI"
    CYBERSECURITE = "CYBERSECURITE"
    TELECOM_RESEAU = "TELECOM_RESEAU"
    TRAVAUX_BTP = "TRAVAUX_BTP"
    MAINTENANCE = "MAINTENANCE"
    FORMATION = "FORMATION"
    ETUDES_CONSEIL = "ETUDES_CONSEIL"
    SANTE_MEDICAL = "SANTE_MEDICAL"
    MOBILIER_EQUIPEMENT = "MOBILIER_EQUIPEMENT"
    NETTOYAGE_GARDIENNAGE = "NETTOYAGE_GARDIENNAGE"
    TRANSPORT_VEHICULES = "TRANSPORT_VEHICULES"
    EVENEMENTIEL_COMMUNICATION = "EVENEMENTIEL_COMMUNICATION"
    AUTRE = "AUTRE"


class Confidence(str, Enum):
    HAUTE = "HAUTE"
    MOYENNE = "MOYENNE"
    FAIBLE = "FAIBLE"


class Classification(BaseModel):
    id: str = Field(
        description="L'identifiant fourni entre crochets, recopié tel quel."
    )
    domaines: list[Domaine] = Field(
        description="Tous les domaines applicables, du plus au moins central."
    )
    justification: str = Field(
        description="Une phrase courte citant les mots de l'objet qui justifient le choix."
    )
    confidence: Confidence


class Results(BaseModel):
    results: list[Classification]


SYSTEM = """Tu classifies des avis de marchés publics marocains par domaine d'achat.

Règles:
- Base-toi sur l'objet du marché. L'acheteur public n'est qu'un indice secondaire:
  un hôpital qui achète des PC relève de MATERIEL_INFORMATIQUE, pas de SANTE_MEDICAL.
- Plusieurs domaines sont possibles (ex: une formation en cybersécurité =
  FORMATION + CYBERSECURITE).
- MAINTENANCE ne s'utilise que si la prestation est explicitement de l'entretien
  ou du support, et se combine avec le domaine du matériel concerné.
- Si l'objet est vide, illisible ou trop vague pour trancher: AUTRE, confiance FAIBLE.
  Ne devine pas.
- Traite chaque avis indépendamment: la classification d'un avis ne doit pas
  influencer celle des suivants.
- Réponds pour CHAQUE identifiant reçu, exactement une fois."""
