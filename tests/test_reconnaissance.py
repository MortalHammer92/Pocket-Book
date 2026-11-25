"""Reconnaissance des documents : mot de passe, contact ou autre (données inventées)."""
import pytest

from pocket_book import classer_document, deviner, deviner_fiche


@pytest.mark.parametrize("texte, attendu", [
    ("Identifiant : jeanne42\nMot de passe : Tulipe-Lune-12", "compte"),
    ("jeanne@exemple.fr\n\nSoleil2024", "compte"),
    ("Username: granny42\nPassword: Blue-Sky-77", "compte"),
    ("Usuario: abuela\nContraseña: Sol-Luna-12", "compte"),
    ("Benutzername: oma\nPasswort: Apfel-Baum-3", "compte"),
    ("Nome utente: nonna\nParola d'ordine: Pane-Vino-8", "compte"),
    ("Mme Josette Durand\n12 rue des Lilas\n59700 Marcq\n06 12 34 56 78", "contact"),
    ("John Smith\n221B Baker Street\n+44 20 7946 0958", "contact"),
    ("Mary Jones\n(555) 123-4567\n742 Evergreen Terrace, Springfield 49007", "contact"),
    ("Carmen López\nCalle Mayor 3, 28013 Madrid\n+34 612 345 678", "contact"),
    ("Hans Müller\nHauptstraße 12\n10115 Berlin", "contact"),
    ("Giulia Rossi\nVia Roma 5, 00184 Roma\n+39 06 1234 5678", "contact"),
    ("Farine 200 g\nBeurre 100 g\nCuire 30 minutes", "autre"),
    ("", "autre"),
])
def test_classement(texte, attendu):
    assert classer_document(texte) == attendu


def test_email_ligne_vide_mot_de_passe():
    fiche = deviner_fiche("Amazon", "jeanne@exemple.fr\n\nRiviere-Pomme-27")
    assert fiche["nom"] == "Amazon"
    assert fiche["email"] == "jeanne@exemple.fr"
    assert fiche["mdp"] == "Riviere-Pomme-27"


def test_libelle_seul_valeur_sur_la_ligne_suivante():
    fiche = deviner_fiche("Orange", "Mot de passe\nLune-Pomme-12\nIdentifiant :\nmamie42")
    assert fiche["mdp"] == "Lune-Pomme-12"
    assert fiche["identifiant"] == "mamie42"


def test_mot_de_passe_qui_commence_par_deux_points():
    fiche = deviner_fiche("Heroku", "jeanne@exemple.fr\n\n:abc123XYZ")
    assert fiche["mdp"] == ":abc123XYZ"


def test_site_deduit_du_nom_de_fichier():
    assert deviner_fiche("1fichier.com", "a@b.fr\n\nmotdepasse")["site"] == "1fichier.com"


def test_contact_francais_mis_en_forme():
    fiche = deviner("Josette", "Josette Durand\n12 rue des Lilas\n59700 Marcq\n"
                               "Tél : 03 20 12 34 56\n06.12.34.56.78\nAnniversaire : 14/03/1948")[0]
    assert fiche["type"] == "contact"
    assert fiche["portable"] == "06 12 34 56 78"
    assert fiche["telephone"] == "03 20 12 34 56"
    assert "rue des Lilas" in fiche["adresse"]
    assert fiche["anniversaire"] == "14/03/1948"


def test_numero_etranger_garde_tel_quel():
    fiche = deviner("John", "John Smith\n221B Baker Street\n+44 20 7946 0958")[0]
    assert fiche["telephone"] == "+44 20 7946 0958"


def test_plusieurs_contacts_dans_un_document():
    texte = ("Josette Durand\n12 rue des Lilas\n59700 Marcq\n06 12 34 56 78\n\n"
             "Paul Martin\n03 20 11 22 33\npaul@exemple.fr\n\n"
             "Docteur Lefèvre\n5 av. Foch, 75016 Paris\n01 45 00 00 00")
    noms = [f["nom"] for f in deviner("Carnet d'adresses", texte)]
    assert noms == ["Josette Durand", "Paul Martin", "Docteur Lefèvre"]
