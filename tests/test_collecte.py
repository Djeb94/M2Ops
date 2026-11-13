"""Tests du parseur sur une fixture figée : aucun accès réseau."""
from pathlib import Path

from gazette.collecte import parse_feed

FIXTURE = Path(__file__).parent / "fixtures" / "lemonde_une.xml"
CHAMPS_ATTENDUS = {"source", "guid", "titre", "extrait", "lien", "date_publication", "rubrique"}


def _items():
    return parse_feed(FIXTURE.read_bytes(), "lemonde")


def test_lit_tous_les_items():
    assert len(_items()) == 3


def test_ne_garde_que_les_champs_du_bornage():
    # Pas d'image, pas de légende, pas de crédit photo : uniquement nos 7 champs.
    for item in _items():
        assert set(item) == CHAMPS_ATTENDUS


def test_date_convertie_en_utc():
    # Dans le flux : 11:42:43 +0100 -> 10:42:43 en UTC.
    assert _items()[0]["date_publication"] == "2026-11-13T10:42:43+00:00"


def test_rubrique_extraite_de_l_url():
    assert _items()[0]["rubrique"] == "pixels"
