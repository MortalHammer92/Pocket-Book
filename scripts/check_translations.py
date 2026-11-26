#!/usr/bin/env python3
"""Check Pocket Book's translations.

Finds every sentence passed to _() or n_() in pocket_book.py (and the labels translated
when used), then reports for each language in translations.py:
  - sentences with no translation;
  - translations whose {placeholders} do not match.

Usage: python scripts/check_translations.py      (exit code 1 if there is a problem)
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from translations import LANGUAGES, TRANSLATIONS  # noqa: E402

TRANSLATED_WHEN_USED = ["FIELD_LABELS", "KIND_LABELS", "KIND_NAMES", "TXT_SUBFOLDERS"]
OTHERS = ["Bank", "Administration", "Health", "Email", "Bills", "Shopping", "Leisure",
          "Other", "All"]


def program_sentences():
    tree = ast.parse((ROOT / "pocket_book.py").read_text(encoding="utf-8"))
    sentences = []

    def add_sentence(value):
        if isinstance(value, str) and value.strip() and value not in sentences and value != "A":
            sentences.append(value)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "_" and node.args and isinstance(node.args[0], ast.Constant):
                add_sentence(node.args[0].value)
            if node.func.id == "n_":
                for argument in node.args[1:3]:
                    if isinstance(argument, ast.Constant):
                        add_sentence(argument.value)
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.targets[0], ast.Name):
            continue
        name = node.targets[0].id
        if name in TRANSLATED_WHEN_USED:
            for value in ast.literal_eval(node.value).values():
                add_sentence(value)
        elif name == "DEFAULT_CATEGORIES":
            for category in ast.literal_eval(node.value):
                add_sentence(category["name"])
        elif name == "CATEGORY_PALETTE":
            for label, _color in ast.literal_eval(node.value):
                add_sentence(label)
        elif name == "THEMES":
            for theme in ast.literal_eval(node.value).values():
                add_sentence(theme["name"])
    for sentence in OTHERS:
        add_sentence(sentence)
    return sentences


def problems():
    sentences = program_sentences()
    errors = []
    for code in LANGUAGES:
        if code == "en":
            continue
        table = TRANSLATIONS.get(code, {})
        for sentence in sentences:
            if sentence not in table:
                errors.append(f"[{code}] missing translation: {sentence!r}")
                continue
            expected = sorted(re.findall(r"\{\w+\}", sentence))
            found = sorted(re.findall(r"\{\w+\}", table[sentence]))
            if expected != found:
                errors.append(f"[{code}] placeholders differ: {sentence!r} -> {table[sentence]!r}")
    return sentences, errors


if __name__ == "__main__":
    sentences, errors = problems()
    for error in errors:
        print(error)
    print(f"{len(sentences)} sentences, {len(LANGUAGES) - 1} languages, {len(errors)} problem(s).")
    sys.exit(1 if errors else 0)
