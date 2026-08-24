FORM_URL = "https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseAdvancedSearch"
SEARCH_URL = FORM_URL + "&searchAnnCons"

PAGE_SIZE = 100

LANCER_RECHERCHE = "ctl0$CONTENU_PAGE$AdvancedSearch$lancerRecherche"
LISTE_PAGE_SIZE = "ctl0$CONTENU_PAGE$resultSearch$listePageSizeTop"
PAGE_SUIVANTE = "ctl0$CONTENU_PAGE$resultSearch$PagerTop$ctl2"

CRITERIA = {
    "ctl0$CONTENU_PAGE$AdvancedSearch$dateMiseEnLigneStart": "",
    "ctl0$CONTENU_PAGE$AdvancedSearch$dateMiseEnLigneEnd": "",
    "ctl0$CONTENU_PAGE$AdvancedSearch$dateMiseEnLigneCalculeStart": "18/08/2026",
    "ctl0$CONTENU_PAGE$AdvancedSearch$dateMiseEnLigneCalculeEnd": "24/08/2026",
    "ctl0$CONTENU_PAGE$AdvancedSearch$domaineActivite$idsDomaines": "1.13.11#1.13.12#1.16.5#2.18.1#2.18.3#2.18.4#2.18.5#3.11.6#3.12.6#3.19#",
}


def _postback(pagestate, target, **fields):
    return {
        "PRADO_PAGESTATE": pagestate,
        "PRADO_POSTBACK_TARGET": target,
        "PRADO_POSTBACK_PARAMETER": "",
        **fields,
    }


def search_data(pagestate):
    return _postback(pagestate, LANCER_RECHERCHE, **CRITERIA)


def page_size_data(pagestate):
    return _postback(pagestate, LISTE_PAGE_SIZE, **{LISTE_PAGE_SIZE: PAGE_SIZE})


def next_page_data(pagestate):
    return _postback(pagestate, PAGE_SUIVANTE, **{LISTE_PAGE_SIZE: PAGE_SIZE})
