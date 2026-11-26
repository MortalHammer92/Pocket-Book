"""Document recognition: password, contact or other (made-up data)."""
import pytest

from pocket_book import classify_document, guess, guess_card


@pytest.mark.parametrize("text_value, expected_value", [
    ("Identifiant : jeanne42\nMot de passe : Tulipe-Lune-12", "account"),
    ("jeanne@exemple.fr\n\nSoleil2024", "account"),
    ("Username: granny42\nPassword: Blue-Sky-77", "account"),
    ("Usuario: abuela\nContraseña: Sol-Luna-12", "account"),
    ("Benutzername: oma\nPasswort: Apfel-Baum-3", "account"),
    ("Nome utente: nonna\nParola d'ordine: Pane-Vino-8", "account"),
    ("Mme Josette Durand\n12 rue des Lilas\n59700 Marcq\n06 12 34 56 78", "contact"),
    ("John Smith\n221B Baker Street\n+44 20 7946 0958", "contact"),
    ("Mary Jones\n(555) 123-4567\n742 Evergreen Terrace, Springfield 49007", "contact"),
    ("Carmen López\nCalle Mayor 3, 28013 Madrid\n+34 612 345 678", "contact"),
    ("Hans Müller\nHauptstraße 12\n10115 Berlin", "contact"),
    ("Giulia Rossi\nVia Roma 5, 00184 Roma\n+39 06 1234 5678", "contact"),
    ("Farine 200 g\nBeurre 100 g\nCuire 30 minutes", "other"),
    ("", "other"),
])
def test_classification(text_value, expected_value):
    assert classify_document(text_value) == expected_value


def test_email_blank_line_password():
    card = guess_card("Amazon", "jeanne@exemple.fr\n\nRiviere-Pomme-27")
    assert card["name"] == "Amazon"
    assert card["email"] == "jeanne@exemple.fr"
    assert card["password"] == "Riviere-Pomme-27"


def test_label_alone_value_on_next_line():
    card = guess_card("Orange", "Mot de passe\nLune-Pomme-12\nIdentifiant :\nmamie42")
    assert card["password"] == "Lune-Pomme-12"
    assert card["username"] == "mamie42"


def test_password_starting_with_colon():
    card = guess_card("Heroku", "jeanne@exemple.fr\n\n:abc123XYZ")
    assert card["password"] == ":abc123XYZ"


def test_site_guessed_from_file_name():
    assert guess_card("1fichier.com", "a@b.fr\n\nmotdepasse")["site"] == "1fichier.com"


def test_french_contact_is_formatted():
    card = guess("Josette", "Josette Durand\n12 rue des Lilas\n59700 Marcq\n"
                 "Tél : 03 20 12 34 56\n06.12.34.56.78\nAnniversaire : 14/03/1948")[0]
    assert card["type"] == "contact"
    assert card["mobile"] == "06 12 34 56 78"
    assert card["phone"] == "03 20 12 34 56"
    assert "rue des Lilas" in card["address"]
    assert card["birthday"] == "14/03/1948"


def test_foreign_number_kept_as_is():
    card = guess("John", "John Smith\n221B Baker Street\n+44 20 7946 0958")[0]
    assert card["phone"] == "+44 20 7946 0958"


def test_several_contacts_in_one_document():
    text_value = ("Josette Durand\n12 rue des Lilas\n59700 Marcq\n06 12 34 56 78\n\n"
                  "Paul Martin\n03 20 11 22 33\npaul@exemple.fr\n\n"
                  "Docteur Lefèvre\n5 av. Foch, 75016 Paris\n01 45 00 00 00")
    names = [f["name"] for f in guess("Carnet d'adresses", text_value)]
    assert names == ["Josette Durand", "Paul Martin", "Docteur Lefèvre"]
