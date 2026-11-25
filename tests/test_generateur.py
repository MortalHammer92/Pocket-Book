"""Générateur de mots de passe."""
import pocket_book
from pocket_book import AMBIGUS, SYMBOLES, generer_mot_de_passe, generer_phrase


def test_longueur_et_groupes():
    for _essai in range(50):
        mdp = generer_mot_de_passe(16)
        assert len(mdp) == 16
        assert any(c.islower() for c in mdp)
        assert any(c.isupper() for c in mdp)
        assert any(c.isdigit() for c in mdp)
        assert any(c in SYMBOLES for c in mdp)


def test_sans_caracteres_qui_se_ressemblent():
    assert not set(generer_mot_de_passe(500)) & AMBIGUS


def test_sans_symboles():
    assert not set(generer_mot_de_passe(200, symboles=False)) & set(SYMBOLES)


def test_phrase_facile_dans_la_langue_choisie():
    from langues import MOTS_FACILES
    pocket_book.choisir_langue("de")
    mots = generer_phrase(4).split("-")
    assert len(mots) == 5 and mots[-1].isdigit()
    assert all(m.lower() in MOTS_FACILES["de"] for m in mots[:-1])
