#!/usr/bin/env python3
"""Check Pocket Book's translations.

Finds every sentence passed to _() or n_() in pocket_book.py (and the labels translated
when used), then reports for each language in langues.py:
  - sentences with no translation;
  - translations whose {placeholders} do not match.

Usage: python scripts/verifier_traductions.py      (exit code 1 if there is a problem)
"""
import ast
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE))
from langues import LANGUES, TRADUCTIONS  # noqa: E402

TRADUITS_A_L_USAGE = ["LIBELLES_CHAMPS", "ETIQUETTES_GENRE", "NOMS_GENRE", "SOUS_DOSSIERS_TXT"]
AUTRES = ["Banque", "Administration", "Santé", "Messagerie", "Factures", "Achats", "Loisirs",
          "Autres", "Tout"]


def phrases_du_programme():
    arbre = ast.parse((RACINE / "pocket_book.py").read_text(encoding="utf-8"))
    phrases = []

    def ajoute(valeur):
        if isinstance(valeur, str) and valeur.strip() and valeur not in phrases and valeur != "A":
            phrases.append(valeur)

    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Name):
            if noeud.func.id == "_" and noeud.args and isinstance(noeud.args[0], ast.Constant):
                ajoute(noeud.args[0].value)
            if noeud.func.id == "n_":
                for argument in noeud.args[1:3]:
                    if isinstance(argument, ast.Constant):
                        ajoute(argument.value)
    for noeud in arbre.body:
        if not isinstance(noeud, ast.Assign) or not isinstance(noeud.targets[0], ast.Name):
            continue
        nom = noeud.targets[0].id
        if nom in TRADUITS_A_L_USAGE:
            for valeur in ast.literal_eval(noeud.value).values():
                ajoute(valeur)
        elif nom == "CATEGORIES_DE_DEPART":
            for categorie in ast.literal_eval(noeud.value):
                ajoute(categorie["nom"])
        elif nom == "PALETTE_CATEGORIES":
            for libelle, _couleur in ast.literal_eval(noeud.value):
                ajoute(libelle)
        elif nom == "THEMES":
            for theme in ast.literal_eval(noeud.value).values():
                ajoute(theme["nom"])
    for phrase in AUTRES:
        ajoute(phrase)
    return phrases


def problemes():
    phrases = phrases_du_programme()
    erreurs = []
    for code in LANGUES:
        if code == "fr":
            continue
        table = TRADUCTIONS.get(code, {})
        for phrase in phrases:
            if phrase not in table:
                erreurs.append(f"[{code}] sans traduction : {phrase!r}")
                continue
            attendus = sorted(re.findall(r"\{\w+\}", phrase))
            trouves = sorted(re.findall(r"\{\w+\}", table[phrase]))
            if attendus != trouves:
                erreurs.append(f"[{code}] marqueurs différents : {phrase!r} -> {table[phrase]!r}")
    return phrases, erreurs


if __name__ == "__main__":
    phrases, erreurs = problemes()
    for erreur in erreurs:
        print(erreur)
    print(f"{len(phrases)} phrases, {len(LANGUES) - 1} langues, {len(erreurs)} problème(s).")
    sys.exit(1 if erreurs else 0)
