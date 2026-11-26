"""Password generator."""
import pocket_book
from pocket_book import AMBIGUOUS, SYMBOLS, generate_password, generate_passphrase


def test_length_and_groups():
    for _attempt in range(50):
        password = generate_password(16)
        assert len(password) == 16
        assert any(c.islower() for c in password)
        assert any(c.isupper() for c in password)
        assert any(c.isdigit() for c in password)
        assert any(c in SYMBOLS for c in password)


def test_no_lookalike_characters():
    assert not set(generate_password(500)) & AMBIGUOUS


def test_without_symbols():
    assert not set(generate_password(200, symbols=False)) & set(SYMBOLS)


def test_easy_passphrase_in_chosen_language():
    from translations import EASY_WORDS
    pocket_book.set_language("de")
    words = generate_passphrase(4).split("-")
    assert len(words) == 5 and words[-1].isdigit()
    assert all(m.lower() in EASY_WORDS["de"] for m in words[:-1])
