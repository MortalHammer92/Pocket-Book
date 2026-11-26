"""Saving, backups, recovery from a damaged file, categories."""
import json

from pocket_book import Book, upgrade_data


def new_book(tmp_path):
    return Book(tmp_path / "pocketbook.json", tmp_path / "backups")


def test_save_and_reload(tmp_path):
    book = new_book(tmp_path)
    book.new_card(name="Bank", password="secret")
    book.new_card(type="contact", name="Josette", mobile="06 12 34 56 78")
    book.save()
    reloaded = new_book(tmp_path)
    reloaded.load()
    assert [(f["type"], f["name"]) for f in reloaded.cards] == [("account", "Bank"), ("contact", "Josette")]


def test_damaged_file_restores_latest_backup(tmp_path):
    book = new_book(tmp_path)
    book.new_card(name="Kept")
    book.save()
    book.daily_backup(force=True)
    (tmp_path / "pocketbook.json").write_text("{damaged", encoding="utf-8")
    reloaded = new_book(tmp_path)
    reloaded.load()
    assert [f["name"] for f in reloaded.cards] == ["Kept"]
    assert reloaded.recovery_message
    assert list(tmp_path.glob("pocketbook_unreadable_*.json"))


def test_write_never_leaves_half_written_file(tmp_path):
    book = new_book(tmp_path)
    book.new_card(name="A")
    book.save()
    assert not list(tmp_path.glob("*.tmp"))
    assert json.loads((tmp_path / "pocketbook.json").read_text(encoding="utf-8"))["cards"]


def test_rename_and_delete_category(tmp_path):
    book = new_book(tmp_path)
    card = book.new_card(name="BNP", category="Bank")
    assert book.rename_category("Bank", "My banks")
    assert card["category"] == "My banks"
    book.delete_category("My banks")
    assert card["category"] == "" and "My banks" not in book.category_names()


def test_deleted_card_is_not_recreated_by_sync(tmp_path):
    book = new_book(tmp_path)
    source = str(tmp_path / "Amazon.txt")
    card = book.new_card(name="Amazon", source=source)
    book.delete(card["id"])
    documents = {source: {"name": "Amazon", "text": "a@b.fr\n\nmdp", "kind": "account",
                          "mtime": 1.0, "error": ""}}
    summary = book.sync_documents(documents, lambda suggestions: suggestions)
    assert summary["created"] == 0 and not book.cards


def test_book_from_older_version_is_converted(tmp_path):
    old = {"version": 1, "reglages": {"theme": "sombre", "taille_texte": 2, "langue": "fr",
                                      "categories": [{"nom": "Banque", "couleur": "#D6E6FA"}]},
           "fiches": [{"id": "1", "type": "compte", "nom": "Impots", "mdp": "Lune-12",
                       "categorie": "Banque", "champs_ajoutes": ["site"],
                       "perso": [{"libelle": "Code client", "valeur": "42"}]},
                      {"id": "2", "type": "contact", "nom": "Josette", "portable": "06 12 34 56 78"}]}
    (tmp_path / "pocketbook.json").write_text(json.dumps(old), encoding="utf-8")
    book = new_book(tmp_path)
    book.load()
    account, contact = book.cards
    assert (account["type"], account["name"], account["password"]) == ("account", "Impots", "Lune-12")
    assert account["added_fields"] == ["site"]
    assert account["custom"] == [{"label": "Code client", "value": "42"}]
    assert contact["mobile"] == "06 12 34 56 78"
    assert book.settings["theme"] == "dark" and book.settings["text_size"] == 2
    assert book.category_names()[:1] == ["Banque"]


def test_current_format_is_left_alone():
    data = {"version": 2, "settings": {}, "cards": [{"name": "A"}]}
    assert upgrade_data(data) is data
