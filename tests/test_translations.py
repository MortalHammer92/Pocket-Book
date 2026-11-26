"""Every interface sentence is translated, with the same {placeholders}."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_translations  # noqa: E402

import pocket_book  # noqa: E402
from translations import LANGUAGES  # noqa: E402


def test_no_missing_sentence():
    _sentences, errors = check_translations.problems()
    assert errors == []


@pytest.mark.parametrize("code", list(LANGUAGES))
def test_sentences_with_values(code):
    pocket_book.set_language(code)
    assert "3" in pocket_book.n_(3, "{n} card", "{n} cards")
    assert "Amazon" in pocket_book._("Do you really want to delete the card “{name}”?", name="Amazon")
