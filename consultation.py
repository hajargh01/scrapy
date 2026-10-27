from dataclasses import dataclass, field
from datetime import datetime

from ai import Domaine, Confidence


@dataclass
class Consultation:
    id = None
    reference: str | None = None
    objet: str | None = None
    acheteur_public: str | None = None
    lieu: str | None = None
    date_limite: datetime | None = None
    estimation: float | None = None
    caution: float | None = None
    url: str | None = None
    domaines: list[Domaine] = field(default_factory=list)
    justification: str = None
    confidence: Confidence | None = None
    portail: str | None = None
