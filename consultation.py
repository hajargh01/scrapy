class Consultation:
    def __init__(
        self,
        id,
        date_publication,
        reference,
        objet,
        acheteurs_public,
        lieux,
        date_limite,
        estimation,
        caution,
        url,
    ):
        self.id = id
        self.date_publication = date_publication
        self.reference = reference
        self.objet = objet
        self.acheteurs_public = acheteurs_public
        self.lieux = lieux
        self.date_limite = date_limite
        self.estimation = estimation
        self.caution = caution
        self.url = url
