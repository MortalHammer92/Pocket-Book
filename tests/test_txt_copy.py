""".txt copy of each card: creation, update, renaming, trash."""
import pocket_book
from pocket_book import Book, file_name


def book_with_copy(tmp_path):
    book = Book(tmp_path / "pocketbook.json", tmp_path / "backups")
    book.settings["txt_folder"] = str(tmp_path / "copy")
    return book


def files(tmp_path):
    return sorted(p.relative_to(tmp_path / "copy").as_posix() for p in (tmp_path / "copy").rglob("*.txt"))


def test_create_update_rename(tmp_path):
    book = book_with_copy(tmp_path)
    card = book.new_card(name="Amazon", password="one")
    assert book.sync_txt()
    assert files(tmp_path) == ["Passwords/Amazon.txt"]
    card["password"] = "two"
    book.sync_txt()
    assert "two" in (tmp_path / "copy/Passwords/Amazon.txt").read_text(encoding="utf-8-sig")
    card["name"] = "Amazon Prime"
    book.sync_txt()
    assert files(tmp_path) == ["Passwords/Amazon Prime.txt"]


def test_deleted_card_goes_to_trash(tmp_path):
    book = book_with_copy(tmp_path)
    card = book.new_card(type="contact", name="Josette")
    book.sync_txt()
    book.delete(card["id"])
    book.sync_txt()
    assert files(tmp_path) == ["Deleted cards/Josette.txt"]


def test_never_overwrite_existing_file(tmp_path):
    book = book_with_copy(tmp_path)
    custom = tmp_path / "copy/Passwords/Netflix.txt"
    custom.parent.mkdir(parents=True)
    custom.write_text("my own file", encoding="utf-8")
    book.new_card(name="Netflix")
    book.sync_txt()
    assert custom.read_text(encoding="utf-8") == "my own file"
    assert "Passwords/Netflix (2).txt" in files(tmp_path)


def test_valid_windows_file_names():
    assert file_name('Josette / Durand?') == "Josette - Durand-"
    assert file_name("CON") == "CON (card)"
    assert file_name("") == "Untitled"


def test_folders_follow_the_interface_language(tmp_path):
    pocket_book.set_language("fr")
    book = book_with_copy(tmp_path)
    book.new_card(name="Amazon")
    book.sync_txt()
    assert files(tmp_path) == ["Mots de passe/Amazon.txt"]
