"""Toutes les phrases de l'interface sont traduites, avec les mêmes {marqueurs}."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import verifier_traductions  # noqa: E402

import pocket_book  # noqa: E402
from langues import LANGUES  # noqa: E402


def test_aucune_phrase_manquante():
    _phrases, erreurs = verifier_traductions.problemes()
    assert erreurs == []


@pytest.mark.parametrize("code", list(LANGUES))
def test_phrases_avec_valeurs(code):
    pocket_book.choisir_langue(code)
    assert "3" in pocket_book.n_(3, "{n} fiche", "{n} fiches")
    assert "Amazon" in pocket_book._("Voulez-vous vraiment supprimer la fiche « {nom} » ?", nom="Amazon")
