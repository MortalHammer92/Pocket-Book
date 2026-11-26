# -*- coding: utf-8 -*-
"""
Pocket Book — a very simple, offline password and contact keeper,
designed for people who are not at ease with computers.

- Password and contact cards, saved automatically.
- Password generator (easy to read or very strong).
- Reads old documents (.docx and .txt) WITHOUT EVER CHANGING THEM:
  each recognized document becomes a card, updated when it changes.
- .txt copy of each card, A to Z sorting, categories, themes, text size.
- Interface in French, English, Spanish, German and Italian (langues.py).
- Windows, macOS and Linux. Python standard library only.

Data is stored in "Documents/Pocket Book":
    pocketbook.json        cards and settings (not encrypted: see README)
    index_documents.json   document reading cache (can be deleted)
    backups/               one automatic copy per day (30 kept)
"""

import json
import os
import queue
import re
import secrets
import shutil
import string
import sys
import threading
import unicodedata
import uuid
import webbrowser
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------

from langues import LANGUES, TRADUCTIONS, MOTS_FACILES as MOTS_PAR_LANGUE  # noqa: E402

# ---------------------------------------------------------------------------
# Interface language
# ---------------------------------------------------------------------------
# The program's text is written in French; _("text") returns its translation
# in the chosen language (langues.py). To add a language: see langues.py.

_LANGUE = ["fr"]
LANGUE_IMPOSEE = [None]   # language passed by the installation window


def _(texte, **valeurs):
    traduit = TRADUCTIONS.get(_LANGUE[0], {}).get(texte, texte)
    return traduit.format(**valeurs) if valeurs else traduit


def n_(nombre, singulier, pluriel, **valeurs):
    """Singular or plural sentence depending on the number (in French, 0 and 1 are singular)."""
    un = nombre <= 1 if _LANGUE[0] == "fr" else nombre == 1
    return _(singulier if un else pluriel, n=nombre, **valeurs)


def deux_points(libelle):
    """"Libellé :" in French, "Label:" in the other languages."""
    return f"{libelle} :" if _LANGUE[0] == "fr" else f"{libelle}:"


def choisir_langue(code):
    if code in LANGUES:
        _LANGUE[0] = code


def langue_actuelle():
    return _LANGUE[0]


def langue_du_systeme():
    """fr, en, es, de or it depending on the system; English by default."""
    codes = []
    if sys.platform.startswith("win"):
        try:
            import ctypes
            import locale
            ident = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            codes.append(locale.windows_locale.get(ident, ""))
        except Exception:
            pass
    for variable in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        codes.append(os.environ.get(variable, ""))
    try:
        import locale
        codes.append(locale.getlocale()[0] or "")
    except Exception:
        pass
    if sys.platform == "darwin":
        try:
            import subprocess
            codes.append(subprocess.run(["defaults", "read", "-g", "AppleLanguages"],
                                        capture_output=True, text=True, timeout=5).stdout)
        except Exception:
            pass
    noms = {"french": "fr", "english": "en", "spanish": "es", "german": "de", "italian": "it"}
    for code in codes:
        bas = (code or "").lower()
        for nom, abrege in noms.items():
            if bas.startswith(nom):
                return abrege
        bas = bas.strip(' ("\n')
        if bas[:2] in LANGUES:
            return bas[:2]
    return "en"


NOM_APPLI = "Pocket Book"
VERSION = "1.0.0"
EST_WINDOWS = sys.platform.startswith("win")
EST_MAC = sys.platform == "darwin"
EST_LINUX = sys.platform.startswith("linux")


def dossier_mes_documents():
    """The user's "Documents" folder (Windows: even when moved to OneDrive)."""
    if EST_LINUX:
        try:  # localized folder name (Documents, Dokumente, Documenti…)
            import subprocess
            chemin = subprocess.run(["xdg-user-dir", "DOCUMENTS"], capture_output=True,
                                    text=True, timeout=5).stdout.strip()
            if chemin and os.path.isdir(chemin) and os.path.normpath(chemin) != str(Path.home()):
                return Path(chemin)
        except Exception:
            pass
    if EST_WINDOWS:
        try:
            import ctypes
            from ctypes import wintypes
            tampon = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            if ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, tampon) == 0:
                return Path(tampon.value)
        except Exception:
            pass
    return Path.home() / "Documents"


DOSSIER_DONNEES = dossier_mes_documents() / "Pocket Book"
ANCIEN_DOSSIER_DONNEES = dossier_mes_documents() / "Mon carnet"   # name used by the first versions


def migrer_ancien_dossier():
    """The first versions were called "Mon carnet": their cards are carried over.

    The old folder is copied (never deleted) to "Pocket Book".
    """
    ancien = ANCIEN_DOSSIER_DONNEES / "carnet.json"
    if DOSSIER_DONNEES.exists() or not ancien.exists():
        return False
    try:
        shutil.copytree(ANCIEN_DOSSIER_DONNEES, DOSSIER_DONNEES)
        os.replace(DOSSIER_DONNEES / "carnet.json", DOSSIER_DONNEES / "pocketbook.json")
        anciennes = DOSSIER_DONNEES / "sauvegardes"
        if anciennes.exists():
            os.replace(anciennes, DOSSIER_DONNEES / "backups")
            for f in (DOSSIER_DONNEES / "backups").glob("carnet_*.json"):
                os.replace(f, f.with_name(f.name.replace("carnet_", "pocketbook_", 1)))
        # the settings pointed to the old folder (.txt copy…)
        chemin = DOSSIER_DONNEES / "pocketbook.json"
        donnees = json.loads(chemin.read_text(encoding="utf-8"))
        reglages = donnees.get("reglages", {})
        ancien_txt = reglages.get("dossier_txt", "")
        if ancien_txt.startswith(str(ANCIEN_DOSSIER_DONNEES)):
            reglages["dossier_txt"] = str(DOSSIER_DONNEES) + ancien_txt[len(str(ANCIEN_DOSSIER_DONNEES)):]
        chemin.write_text(json.dumps(donnees, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except (OSError, ValueError):
        return False


def ressource(nom):
    """File shipped with the program (also works inside the .exe / app)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    for candidat in (os.path.join(base, nom), os.path.join(base, "assets", nom)):
        if os.path.exists(candidat):
            return candidat
    return os.path.join(base, nom)


def ouvrir_avec_systeme(chemin):
    """Open a file or folder with the system's usual program."""
    import subprocess
    if EST_WINDOWS:
        os.startfile(chemin)  # noqa: S606
    elif EST_MAC:
        subprocess.Popen(["open", str(chemin)])
    else:
        subprocess.Popen(["xdg-open", str(chemin)])


def montrer_dans_dossier(chemin):
    """Open the folder containing the file, with the file selected if possible."""
    import subprocess
    if EST_WINDOWS:
        subprocess.Popen(["explorer", "/select,", os.path.normpath(chemin)])
    elif EST_MAC:
        subprocess.Popen(["open", "-R", str(chemin)])
    else:
        subprocess.Popen(["xdg-open", str(Path(chemin).parent)])
FICHIER_CARNET = DOSSIER_DONNEES / "pocketbook.json"
FICHIER_INDEX = DOSSIER_DONNEES / "index_documents.json"
DOSSIER_SAUVEGARDES = DOSSIER_DONNEES / "backups"
NB_SAUVEGARDES_GARDEES = 30

EXTENSIONS_LUES = (".docx", ".txt")

CHAMPS = {
    "compte": ["nom", "categorie", "site", "identifiant", "email", "mdp", "notes", "source"],
    "contact": ["nom", "portable", "telephone", "email", "adresse", "anniversaire", "notes", "source"],
}

def sans_categorie():
    """Text for the "no category" choice (the category is optional)."""
    return _("(aucune)")


def toutes_categories():
    return _("Toutes")

# Card fields: display order, and the ones that can be added / removed
ORDRE_CHAMPS = {
    "compte": ["categorie", "site", "identifiant", "email", "mdp", "notes"],
    "contact": ["categorie", "portable", "telephone", "email", "adresse", "anniversaire", "notes"],
}
CHAMPS_FACULTATIFS = {
    "compte": ["categorie", "site"],
    "contact": ["categorie", "telephone", "adresse", "anniversaire"],
}
LIBELLES_CHAMPS = {
    "nom": "Nom", "categorie": "Catégorie", "site": "Site internet",
    "identifiant": "Identifiant", "email": "Adresse e-mail", "mdp": "Mot de passe",
    "notes": "Notes", "portable": "Portable", "telephone": "Téléphone fixe",
    "adresse": "Adresse", "anniversaire": "Anniversaire",
}

# Category colors: pale backgrounds, text always dark (easy to read)
PALETTE_CATEGORIES = [
    ("Bleu", "#D6E6FA"), ("Vert", "#D6F0DC"), ("Jaune", "#FFF0B8"), ("Orange", "#FFDDC2"),
    ("Rouge", "#F8D3D3"), ("Violet", "#E6DAF5"), ("Rose", "#F8D6E8"),
    ("Turquoise", "#CDEFEA"), ("Gris", "#E4E2DC"), ("Marron", "#E8D9C7"),
]
TEXTE_SUR_PASTEL = "#1B1A17"
CATEGORIES_DE_DEPART = [
    {"nom": "Banque", "couleur": "#D6E6FA"}, {"nom": "Administration", "couleur": "#E4E2DC"},
    {"nom": "Santé", "couleur": "#D6F0DC"}, {"nom": "Messagerie", "couleur": "#CDEFEA"},
    {"nom": "Achats", "couleur": "#FFDDC2"}, {"nom": "Factures", "couleur": "#FFF0B8"},
    {"nom": "Loisirs", "couleur": "#E6DAF5"}, {"nom": "Famille", "couleur": "#F8D6E8"},
    {"nom": "Travail", "couleur": "#E8D9C7"},
]

# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------


def normaliser(texte):
    """Lowercase without accents, so "impot" finds "Impôts"."""
    texte = unicodedata.normalize("NFD", texte or "")
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return texte.casefold()


def premiere_lettre(nom):
    """Sorting letter: A to Z, or "#" for a digit or a symbol."""
    for c in normaliser(nom).upper():
        if c.isalpha() and "A" <= c <= "Z":
            return c
        if c.isalnum():
            return "#"
    return "#"


def cle_tri(nom):
    return normaliser(nom).strip()


# ---------------------------------------------------------------------------
# Reading documents (never writing)
# ---------------------------------------------------------------------------

_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def texte_docx(chemin):
    """Text of a .docx, paragraph by paragraph (tables included)."""
    with zipfile.ZipFile(chemin, "r") as z:
        xml = z.read("word/document.xml")
    racine = ElementTree.fromstring(xml)
    lignes = []

    def texte_paragraphe(p):
        morceaux = []
        for el in p.iter():
            if el.tag == _W + "t" and el.text:
                morceaux.append(el.text)
            elif el.tag == _W + "tab":
                morceaux.append("\t")
            elif el.tag in (_W + "br", _W + "cr"):
                morceaux.append("\n")
        return "".join(morceaux)

    def parcourir(element):
        for enfant in element:
            if enfant.tag == _W + "p":
                lignes.append(texte_paragraphe(enfant))
            elif enfant.tag == _W + "tbl":
                # A table: one line per row, cells separated by a tab
                for rangee in enfant.iter(_W + "tr"):
                    cellules = [" ".join(texte_paragraphe(p) for p in cellule.iter(_W + "p")).strip()
                                for cellule in rangee.findall(_W + "tc")]
                    lignes.append("\t".join(cellules))
            else:
                parcourir(enfant)

    parcourir(racine)
    return "\n".join(lignes)


def texte_txt(chemin):
    brut = Path(chemin).read_bytes()
    for codage in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return brut.decode(codage)
        except UnicodeDecodeError:
            continue
    return brut.decode("utf-8", errors="replace")


def lire_document(chemin):
    ext = Path(chemin).suffix.lower()
    if ext == ".docx":
        return texte_docx(chemin)
    if ext == ".txt":
        return texte_txt(chemin)
    raise ValueError(_("Type de fichier non pris en charge"))


def lister_documents(dossier, exclure=()):
    """Every .docx / .txt in the folder and its subfolders.

    Also returns the number of old .doc files (Word 97-2003), which are not read.
    """
    resultats, anciens = [], 0
    for racine, sous_dossiers, fichiers in os.walk(dossier):
        exclus = {os.path.normcase(os.path.abspath(e)) for e in exclure if e}
        sous_dossiers[:] = [d for d in sous_dossiers if not d.startswith(".")
                            and os.path.normcase(os.path.abspath(os.path.join(racine, d))) not in exclus]
        for f in fichiers:
            if f.startswith("~$") or f.startswith("."):
                continue  # Word temporary files
            if f.lower().endswith(EXTENSIONS_LUES):
                resultats.append(os.path.join(racine, f))
            elif f.lower().endswith(".doc"):
                anciens += 1
    return resultats, anciens


# ---------------------------------------------------------------------------
# Guessing a card from a document
# ---------------------------------------------------------------------------

# Labels recognized in documents (French, English, Spanish, German, Italian)
_LIBELLES = {
    "mdp": ["mot de passe", "mdp", "password", "pass", "pwd", "code secret",
            "code", "mot passe", "passcode", "pin",
            "contrasena", "clave", "clave de acceso",
            "passwort", "kennwort", "pw",
            "parola d'ordine", "parola chiave", "chiave"],
    "email": ["e-mail", "email", "mail", "adresse mail", "adresse e-mail",
              "courriel", "gmail", "hotmail", "outlook", "orange", "laposte",
              "yahoo", "free", "email address", "e-mail address",
              "correo", "correo electronico", "e-mail-adresse", "posta", "posta elettronica"],
    "identifiant": ["identifiant", "id", "login", "utilisateur",
                    "nom d'utilisateur", "nom d utilisateur", "pseudo", "user",
                    "numero client", "n client", "n° client", "numero fiscal",
                    "n° fiscal", "client", "numero", "n°",
                    "username", "user name", "user id", "account", "account number",
                    "customer number", "usuario", "nombre de usuario", "cuenta",
                    "benutzer", "benutzername", "kundennummer", "konto",
                    "utente", "nome utente", "account utente", "codice cliente"],
    "site": ["site", "url", "lien", "adresse du site", "site internet",
             "website", "web site", "link", "sitio", "sitio web", "pagina",
             "webseite", "seite", "sito", "sito web"],
}

_RE_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_RE_URL = re.compile(r"^(https?://|www\.)\S+$", re.IGNORECASE)
_RE_LIBELLE = re.compile(r"^\s*([^:=\t]{1,30}?)\s*(?:[:=]|\t+)\s*(.*)$")


def _quel_libelle(libelle):
    lib = normaliser(libelle).strip(" .-_*:=")
    for champ, mots in _LIBELLES.items():
        for mot in mots:
            if lib == normaliser(mot):
                return champ
    return None


def deviner_categorie(nom):
    n = normaliser(nom)
    regles = [
        ("Banque", ["banque", "bnp", "credit", "caisse d", "societe generale",
                    "lcl", "boursorama", "cofidis", "cetelem", "cep", "paypal",
                    "bank", "banco", "banca", "sparkasse", "revolut", "n26"]),
        ("Administration", ["impot", "caf", "urssaf", "gouv", "retraite",
                            "ants", "france connect", "franceconnect", "inpi",
                            "pole emploi", "france travail", "tax", "hacienda",
                            "finanzamt", "agenzia entrate", "gov"]),
        ("Santé", ["ameli", "doctolib", "mutuelle", "pharma", "sante",
                   "health", "salud", "gesundheit", "salute", "krankenkasse"]),
        ("Messagerie", ["mail", "gmail", "outlook", "hotmail", "laposte.net",
                        "orange", "yahoo"]),
        ("Factures", ["edf", "engie", "free", "sfr", "bouygues", "veolia",
                      "eau", "gaz", "assurance"]),
        ("Achats", ["amazon", "cdiscount", "fnac", "leboncoin", "dominos",
                    "mcdonald", "carrefour", "leclerc"]),
        ("Loisirs", ["netflix", "deezer", "spotify", "disney", "canal",
                     "battlenet", "ea", "nvidia"]),
    ]
    for categorie, mots in regles:
        for mot in mots:
            if re.search(r"(^|[^a-z])" + re.escape(mot), n):
                return _(categorie)
    return ""  # nothing certain: no category rather than a wrong one


def deviner_fiche(nom, texte):
    """Suggest a card (dictionary) from a document's text.

    Recognized formats, for example:
        adresse@mail.fr            Identifiant : 12345      1234567890
        (empty line)               MDP : xxxxx
        MotDePasse
    """
    fiche = {"identifiant": "", "email": "", "mdp": "", "site": ""}
    emails, urls, jetons, textes = [], [], [], []
    champ_en_attente = None

    for ligne in (texte or "").splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue

        if champ_en_attente:
            if not fiche[champ_en_attente]:
                fiche[champ_en_attente] = ligne
                champ_en_attente = None
                continue
            champ_en_attente = None

        # A label on its own ("Mot de passe"): the value is on the next line.
        champ_seul = _quel_libelle(ligne)
        if champ_seul:
            champ_en_attente = champ_seul
            continue

        m = _RE_LIBELLE.match(ligne)
        if m and not _RE_URL.match(ligne):
            champ = _quel_libelle(m.group(1))
            if champ:
                valeur = m.group(2).strip()
                if champ == "email" and valeur and not _RE_EMAIL.match(valeur):
                    champ = "identifiant"
                if not valeur:
                    champ_en_attente = champ
                elif not fiche[champ]:
                    fiche[champ] = valeur
                else:
                    textes.append(ligne)
                continue

        if _RE_EMAIL.match(ligne):
            emails.append(ligne)
        elif _RE_URL.match(ligne):
            urls.append(ligne)
        elif " " not in ligne and "\t" not in ligne:
            jetons.append(ligne)
        else:
            textes.append(ligne)

    for e in emails:
        if not fiche["email"]:
            fiche["email"] = e
        else:
            textes.append(e)
    for u in urls:
        if not fiche["site"]:
            fiche["site"] = u
        else:
            textes.append(u)

    if jetons:
        if not fiche["mdp"]:
            if len(jetons) >= 2:
                fiche["mdp"] = jetons[-1]
                reste = jetons[:-1]
                if not fiche["identifiant"]:
                    fiche["identifiant"] = reste.pop(0)
                textes.extend(reste)
            else:
                seul = jetons[0]
                deja_un_compte = fiche["email"] or fiche["identifiant"]
                if not deja_un_compte and seul.isdigit() and len(seul) >= 8:
                    fiche["identifiant"] = seul
                else:
                    fiche["mdp"] = seul
        else:
            if not fiche["identifiant"]:
                fiche["identifiant"] = jetons.pop(0)
            textes.extend(jetons)

    if not fiche["site"] and re.search(r"\.[a-z]{2,4}$", normaliser(nom)):
        fiche["site"] = nom.strip()

    return {
        "type": "compte",
        "nom": nom.strip() or _("Sans nom"),
        "categorie": deviner_categorie(nom),
        "site": fiche["site"],
        "identifiant": fiche["identifiant"],
        "email": fiche["email"],
        "mdp": fiche["mdp"],
        "notes": "\n".join(textes),
    }


# ---------------------------------------------------------------------------
# Contacts: recognize and fill in
# ---------------------------------------------------------------------------

_RE_TEL = re.compile(
    # France: 06 12 34 56 78, +33 6 12 34 56 78
    r"(?<!\d)(?:(?:\+|00)33\s?\(?0?\)?\s?[1-9]|0[1-9])(?:[\s.\-]?\d{2}){4}(?!\d)"
    # International: +44 20 7946 0958, +49 30 1234567, +56 9 1234 5678…
    r"|(?<![\d+])\+(?!33)\d{1,3}(?:[\s.\-]?\(?\d{1,4}\)?){2,5}(?!\d)"
    # North America: (555) 123-4567, 555-123-4567
    r"|(?<!\d)\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?!\d)")
_RE_CP = re.compile(r"(?<!\d)\d{5}(?!\d)\s+[A-Za-zÀ-ÿ]")
_MOTS_RUE = re.compile(
    r"(?:^|\s)(?:\d+\s*(?:bis|ter)?\s*,?\s*)?(?:rue|avenue|av\.|boulevard|bd|chemin|allee|"
    r"impasse|place|route|residence|batiment|bat\.|lieu-dit|cedex|quai|square|"
    r"cours|faubourg|hameau|lotissement|appartement|appt|bp|"
    r"street|st\.|road|rd\.|lane|drive|dr\.|ave\.?|way|court|ct\.|apt\.?|suite|terrace|blvd\.?|"
    r"calle|avenida|pasaje|camino|plaza|paseo|piso|"
    r"strasse|str\.|weg|platz|gasse|allee|"
    r"via|viale|piazza|corso|vicolo|largo)(?=[\s,])"
    # number after the street name (Hauptstraße 12, Via Roma 5, Calle Mayor 3)
    r"|[a-z]+(?:strasse|str\.|weg|platz|gasse)\s+\d")


_RE_ADRESSE_NUMERO_PUIS_CP = re.compile(r"^\s*\d+[a-z]?\s+[^\d@]+[\s,]+\d{5}(?:-\d{4})?\s*$", re.IGNORECASE)


def ligne_adresse(ligne):
    """A postal address line: postcode + city, "12 rue …", "742 Main St, City 49007"."""
    if " " not in ligne.strip():
        return False
    if _RE_CP.search(ligne) or _RE_ADRESSE_NUMERO_PUIS_CP.match(ligne):
        return True
    return bool(_MOTS_RUE.search(normaliser(ligne) + " ") and re.search(r"\d", ligne))
_RE_DATE = re.compile(r"(?<!\d)(\d{1,2})[/.\-](\d{1,2})(?:[/.\-](\d{2,4}))?(?!\d)")
_MOTS_ANNIV = re.compile(r"(anniv|ne le|nee le|naissance|ne\(e\)|birthday|born|date of birth|"
                         r"cumpleanos|nacimiento|nacio|geburtstag|geboren|compleanno|nato|nata|nascita)")
_MOTS_COMPTE = re.compile(r"(mot de passe|mdp|password|identifiant|login|code secret|pseudo|"
                          r"username|contrasena|usuario|passwort|kennwort|benutzername|"
                          r"nome utente|parola d'ordine)")


def _est_mot_de_passe_possible(ligne):
    """A single "word" that is neither an e-mail, nor a phone number, nor a website."""
    return (" " not in ligne and "\t" not in ligne and not _RE_EMAIL.match(ligne)
            and not _RE_URL.match(ligne) and not _RE_TEL.search(ligne))


def classer_document(texte):
    """"compte", "contact" or "autre".

    Simple, predictable rules; when in doubt: "autre".
    """
    lignes = [l.strip() for l in (texte or "").splitlines() if l.strip()]
    if not lignes:
        return "autre"
    tout = normaliser("\n".join(lignes))

    signes_compte = bool(_MOTS_COMPTE.search(tout))
    telephone = bool(_RE_TEL.search("\n".join(lignes)))
    adresse = any(ligne_adresse(l) for l in lignes)
    anniversaire = bool(_MOTS_ANNIV.search(tout) and _RE_DATE.search(tout))
    signes_contact = telephone or adresse or anniversaire

    if signes_compte:
        return "compte"
    emails = [l for l in lignes if _RE_EMAIL.match(l)]
    mots_seuls = [l for l in lignes if _est_mot_de_passe_possible(l)]
    if signes_contact:
        return "contact"
    if emails and mots_seuls:
        return "compte"
    if len(lignes) <= 3 and mots_seuls:
        return "compte"
    return "autre"


def deviner_contact(nom, texte):
    lignes = [l.strip() for l in (texte or "").splitlines() if l.strip()]
    portables, fixes, emails, adresse, notes = [], [], [], [], []
    anniversaire = ""
    for ligne in lignes:
        n = normaliser(ligne)
        reste = ligne
        for tel in [m.group(0) for m in _RE_TEL.finditer(ligne)]:
            chiffres = re.sub(r"\D", "", tel)
            francais = (re.match(r"^0[1-9]\d{8}$", chiffres) or re.match(r"^\s*(\+|00)33", tel))
            if francais:  # French number: written "06 12 34 56 78"
                if chiffres.startswith("0033"):
                    chiffres = chiffres[2:]
                if chiffres.startswith("33"):
                    chiffres = "0" + chiffres[2:].lstrip("0")
                joli = " ".join(chiffres[i:i + 2] for i in range(0, len(chiffres), 2))
                mobile = chiffres[:2] in ("06", "07")
            else:  # other country: kept as is
                joli = re.sub(r"\s+", " ", tel.strip())
                mobile = False
            (portables if mobile else fixes).append(joli)
            reste = reste.replace(tel, " ")
        for mot in reste.split():
            if _RE_EMAIL.match(mot.strip(",;()<>")):
                emails.append(mot.strip(",;()<>"))
                reste = reste.replace(mot, " ")
        reste_net = re.sub(r"^[\s:;,\-–]*(tel|tél|telephone|téléphone|portable|fixe|mobile|"
                           r"e-mail|email|mail|courriel)?\s*[:.]?\s*", "", reste,
                           flags=re.IGNORECASE).strip(" :;,-–")
        if not reste_net:
            continue
        if not anniversaire and _MOTS_ANNIV.search(n) and _RE_DATE.search(ligne):
            anniversaire = _RE_DATE.search(ligne).group(0)
            continue
        if ligne_adresse(reste_net):
            adresse.append(re.sub(r"^(adresse)\s*[:.]?\s*", "", reste_net, flags=re.IGNORECASE))
            continue
        if normaliser(reste_net) == normaliser(nom):
            continue
        notes.append(reste_net)
    return {
        "type": "contact",
        "nom": nom.strip() or _("Sans nom"),
        "portable": " / ".join(dict.fromkeys(portables)),
        "telephone": " / ".join(dict.fromkeys(fixes)),
        "email": emails[0] if emails else "",
        "adresse": "\n".join(adresse),
        "anniversaire": anniversaire,
        "notes": "\n".join(notes + emails[1:]),
    }


def _titre_possible(ligne):
    return not (_RE_TEL.search(ligne) or ligne_adresse(ligne) or _RE_EMAIL.match(ligne)
                or _RE_URL.match(ligne))


def decouper_contacts(nom, texte):
    """A document may hold several contacts (a small address book).

    - blocks separated by an empty line, each starting with a name;
    - or a Word table: one row per person (name | phone | address…).
    Otherwise: a single contact, named after the file.
    """
    texte = (texte or "").strip()
    blocs = [b for b in re.split(r"\n\s*\n", texte) if b.strip()]
    trouves = []
    for bloc in blocs:
        lignes = [l.strip() for l in bloc.splitlines() if l.strip()]
        if classer_document(bloc) == "contact" and _titre_possible(lignes[0]):
            trouves.append((lignes[0], bloc))
    if len(trouves) >= 2 and len(trouves) >= len(blocs) - 1:
        return [deviner_contact(titre, bloc) for titre, bloc in trouves]

    rangees = [l for l in texte.splitlines() if "\t" in l and _RE_TEL.search(l)]
    if len(rangees) >= 2:
        fiches = []
        for rangee in rangees:
            cellules = [c.strip() for c in rangee.split("\t") if c.strip()]
            if cellules and _titre_possible(cellules[0]):
                fiches.append(deviner_contact(cellules[0], "\n".join(cellules)))
        if len(fiches) >= 2:
            return fiches
    return [deviner_contact(nom, texte)]


def deviner(nom, texte, genre=None):
    """Card(s) suggested for a document, according to its kind (guessed if missing)."""
    genre = genre or classer_document(texte)
    if genre == "contact":
        return decouper_contacts(nom, texte)
    return [deviner_fiche(nom, texte)]


# ---------------------------------------------------------------------------
# Password generator
# ---------------------------------------------------------------------------

MOTS_FACILES = """
abeille abricot agneau aigle album amande ananas ancre arbre arc argent
automne avion balcon baleine bambou banane bateau berger biscuit bleuet
bougie bouleau boussole brioche brume cabane cactus caillou camion canard
canne carotte cerf cerise chalet chameau champ chanson chapeau chaton
chemin chene cheval chocolat cigale citron clairon colline comete coquille
corbeau coton crayon criquet dauphin domino dragon dune eclair ecureuil
erable etoile facteur falaise farine faucon fenetre fleur flute foret
fourmi fraise framboise fromage fusee gateau girafe glacier grenier grillon
guitare hamac hibou hiver horloge ile jardin jasmin jonquille kiwi lac
lampe lapin laurier lavande lilas lion loutre lune lutin manteau marmotte
melon meteore miel moineau montagne moulin mouette muguet nuage oasis olive
orange orchidee ours palmier panda papillon parapluie pastel pelican
phare piano pingouin pinceau pivoine plage plume poire pomme pont potager
prairie prune puits radis rameau renard requin riviere robinet rocher rose
ruisseau sabot sapin sardine saule sentier sirop soleil source tambour
theiere tigre tilleul tomate tortue train trefle tulipe vallee vanille
velo verger violette voilier volcan zebre
""".split()

AMBIGUS = set("0O1lI|")
SYMBOLES = "!?@#$%&*+-=_"


def generer_mot_de_passe(longueur=16, majuscules=True, chiffres=True,
                         symboles=True, sans_ambigus=True):
    groupes = [string.ascii_lowercase]
    if majuscules:
        groupes.append(string.ascii_uppercase)
    if chiffres:
        groupes.append(string.digits)
    if symboles:
        groupes.append(SYMBOLES)
    if sans_ambigus:
        groupes = ["".join(c for c in g if c not in AMBIGUS) for g in groupes]
    longueur = max(longueur, len(groupes))
    # at least one character from each chosen group
    caracteres = [secrets.choice(g) for g in groupes]
    tous = "".join(groupes)
    caracteres += [secrets.choice(tous) for _i in range(longueur - len(caracteres))]
    for i in range(len(caracteres) - 1, 0, -1):  # secure shuffle
        j = secrets.randbelow(i + 1)
        caracteres[i], caracteres[j] = caracteres[j], caracteres[i]
    return "".join(caracteres)


def generer_phrase(nb_mots=4):
    liste = MOTS_PAR_LANGUE.get(langue_actuelle(), MOTS_FACILES)  # words in the chosen language
    mots = [secrets.choice(liste).capitalize() for _i in range(nb_mots)]
    return "-".join(mots) + "-" + str(secrets.randbelow(90) + 10)


# ---------------------------------------------------------------------------
# The book on disk
# ---------------------------------------------------------------------------


def ecrire_json_sur(chemin, donnees):
    """Write to a temporary file then replace: never a half-written file."""
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    temporaire = chemin.with_suffix(chemin.suffix + ".tmp")
    with open(temporaire, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temporaire, chemin)


class Carnet:
    def __init__(self, fichier=FICHIER_CARNET, sauvegardes=DOSSIER_SAUVEGARDES):
        self.fichier = Path(fichier)
        self.sauvegardes = Path(sauvegardes)
        self.fiches = []
        self.reglages = {"taille_texte": 1, "dossier_documents": "", "theme": "clair",
                         "synchro_auto": True,
                         "dossier_txt": str(DOSSIER_DONNEES / _("Fiches en texte")),
                         "txt_connus": [],
                         "categories": [{"nom": _(c["nom"]), "couleur": c["couleur"]}
                                        for c in CATEGORIES_DE_DEPART]}
        self._cache_txt = {}
        self.message_txt = ""
        self.message_recuperation = ""

    # -- loading -------------------------------------------------------------
    def charger(self):
        if not self.fichier.exists():
            return
        try:
            self._charger_depuis(self.fichier)
        except Exception:
            # Damaged file: set it aside and fall back to the latest backup.
            date = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            abime = self.fichier.with_name("pocketbook_illisible_" + date + ".json")
            try:
                shutil.copy2(self.fichier, abime)
            except OSError:
                pass
            for sauvegarde in self.liste_sauvegardes():
                try:
                    self._charger_depuis(sauvegarde)
                    self.message_recuperation = _(
                        "Le carnet était abîmé. La sauvegarde du {date} a été reprise.",
                        date=sauvegarde.stem.replace("pocketbook_", ""))
                    return
                except Exception:
                    continue
            self.message_recuperation = _(
                "Le carnet était abîmé et aucune sauvegarde n'a pu être lue. "
                "Une copie a été gardée : {fichier}", fichier=abime.name)

    def _charger_depuis(self, chemin):
        with open(chemin, "r", encoding="utf-8") as f:
            donnees = json.load(f)
        fiches = donnees.get("fiches", [])
        for fiche in fiches:
            fiche.setdefault("id", uuid.uuid4().hex)
            fiche.setdefault("type", "compte")
            for champ in CHAMPS[fiche["type"] if fiche["type"] in CHAMPS else "compte"]:
                fiche.setdefault(champ, "")
        self.fiches = fiches
        self.reglages.update(donnees.get("reglages", {}))
        self.assurer_categories()

    # -- saving --------------------------------------------------------------
    def enregistrer(self):
        ecrire_json_sur(self.fichier, {
            "version": 1,
            "enregistre_le": datetime.now().isoformat(timespec="seconds"),
            "reglages": self.reglages,
            "fiches": self.fiches,
        })

    def liste_sauvegardes(self):
        if not self.sauvegardes.exists():
            return []
        return sorted(self.sauvegardes.glob("pocketbook_*.json"), reverse=True)

    def sauvegarde_du_jour(self, force=False):
        """One copy per day (or on demand, e.g. before an import)."""
        if not self.fichier.exists():
            return
        self.sauvegardes.mkdir(parents=True, exist_ok=True)
        if force:
            nom = "pocketbook_" + datetime.now().strftime("%Y-%m-%d_%Hh%M") + ".json"
        else:
            nom = "pocketbook_" + datetime.now().strftime("%Y-%m-%d") + ".json"
        cible = self.sauvegardes / nom
        if force or not cible.exists():
            shutil.copy2(self.fichier, cible)
        for ancienne in self.liste_sauvegardes()[NB_SAUVEGARDES_GARDEES:]:
            try:
                ancienne.unlink()
            except OSError:
                pass

    # -- cards ---------------------------------------------------------------
    def nouvelle_fiche(self, type="compte", **champs):
        fiche = {"id": uuid.uuid4().hex, "type": type}
        fiche.update({c: "" for c in CHAMPS[type]})
        fiche["nom"] = _("Nouveau contact") if type == "contact" else _("Nouvelle fiche")
        fiche["cree_le"] = datetime.now().isoformat(timespec="seconds")
        fiche.update({k: v for k, v in champs.items() if v is not None})
        self.fiches.append(fiche)
        return fiche

    def trouver(self, id_fiche):
        for fiche in self.fiches:
            if fiche["id"] == id_fiche:
                return fiche
        return None

    def supprimer(self, id_fiche):
        fiche = self.trouver(id_fiche)
        self.fiches = [f for f in self.fiches if f["id"] != id_fiche]
        source = (fiche or {}).get("source", "")
        if source and os.path.normcase(source) not in self.sources_connues():
            # Deleted on purpose: synchronization must not recreate it.
            ecartees = self.reglages.setdefault("sources_ecartees", [])
            if os.path.normcase(source) not in ecartees:
                ecartees.append(os.path.normcase(source))

    def reprendre_source(self, chemin):
        """Filing requested by hand: the document is no longer set aside."""
        ecartees = self.reglages.get("sources_ecartees", [])
        if os.path.normcase(chemin) in ecartees:
            ecartees.remove(os.path.normcase(chemin))

    # -- categories ------------------------------------------------------------
    def categories(self):
        return self.reglages.setdefault("categories", [])

    def noms_categories(self):
        return [c["nom"] for c in self.categories()]

    def couleur_categorie(self, nom):
        for c in self.categories():
            if c["nom"] == nom:
                return c.get("couleur", "")
        return ""

    def assurer_categories(self):
        """Every category used by a card exists in the list."""
        connues = {normaliser(n) for n in self.noms_categories()}
        for fiche in self.fiches:
            nom = fiche.get("categorie", "")
            if nom and normaliser(nom) not in connues:
                self.categories().append({"nom": nom, "couleur": "#E4E2DC"})
                connues.add(normaliser(nom))

    def ajouter_categorie(self, nom):
        nom = nom.strip()
        if not nom or normaliser(nom) in {normaliser(n) for n in self.noms_categories()}:
            return False
        utilisees = {c.get("couleur") for c in self.categories()}
        libres = [hexa for _nom, hexa in PALETTE_CATEGORIES if hexa not in utilisees]
        couleur = (libres or [PALETTE_CATEGORIES[len(self.categories()) % len(PALETTE_CATEGORIES)][1]])[0]
        self.categories().append({"nom": nom, "couleur": couleur})
        return True

    def renommer_categorie(self, ancien, nouveau):
        nouveau = nouveau.strip()
        if not nouveau:
            return False
        if normaliser(nouveau) != normaliser(ancien) and normaliser(nouveau) in {
                normaliser(n) for n in self.noms_categories()}:
            return False
        for c in self.categories():
            if c["nom"] == ancien:
                c["nom"] = nouveau
        for fiche in self.fiches:
            if fiche.get("categorie") == ancien:
                fiche["categorie"] = nouveau
        return True

    def supprimer_categorie(self, nom):
        self.reglages["categories"] = [c for c in self.categories() if c["nom"] != nom]
        for fiche in self.fiches:
            if fiche.get("categorie") == nom:
                fiche["categorie"] = ""

    def nb_fiches_categorie(self, nom):
        return sum(1 for f in self.fiches if f.get("categorie") == nom)

    def categorie_existante(self, nom):
        """Keep a guessed category only if it still exists."""
        for n in self.noms_categories():
            if normaliser(n) == normaliser(nom or ""):
                return n
        return ""

    # -- synchronization with the documents folder -----------------------------
    def synchroniser_documents(self, documents, filtre_categories=None):
        """Create cards for new documents, update those of changed documents.

        - A card edited by hand in the book is never overwritten: it only gets
          a "the document has changed" note.
        - A deleted document does not delete its card.
        - Unrecognized documents create nothing.
        Returns a summary {"crees", "mises_a_jour", "a_verifier"}.
        """
        filtre = filtre_categories or (lambda p: p)
        maintenant = datetime.now().isoformat(timespec="seconds")
        par_source = {}
        for fiche in self.fiches:
            if fiche.get("source"):
                par_source.setdefault(os.path.normcase(fiche["source"]), []).append(fiche)
        resume = {"crees": 0, "mises_a_jour": 0, "a_verifier": 0}
        ecartees = set(self.reglages.get("sources_ecartees", []))

        for chemin, doc in sorted(documents.items(), key=lambda kv: cle_tri(kv[1]["nom"])):
            genre = doc.get("genre", "autre")
            existantes = par_source.get(os.path.normcase(chemin), [])
            if not existantes:
                if os.path.normcase(chemin) in ecartees:
                    continue  # card deleted on purpose: do not recreate it
                if genre in ("compte", "contact") and not doc.get("erreur"):
                    for champs in filtre(deviner(doc["nom"], doc["texte"], genre)):
                        self.nouvelle_fiche(source=chemin, source_mtime=doc["mtime"],
                                            importe_le=maintenant, **champs)
                        resume["crees"] += 1
                continue
            if all(f.get("source_mtime") == doc["mtime"] for f in existantes):
                continue  # nothing new
            if any(f.get("source_mtime") is None for f in existantes):
                for f in existantes:   # card from before synchronization existed: just record the date
                    f["source_mtime"] = doc["mtime"]
                continue
            modifiees = [f for f in existantes if f.get("modifiee_a_la_main")
                         or f.get("modifie_le", "") > f.get("importe_le", "")]
            if modifiees:
                date = datetime.now().strftime("%d/%m/%Y")
                for f in existantes:
                    f["source_mtime"] = doc["mtime"]
                    note = _("⚠ Le document « {nom} » a changé le {date} : "
                             "vérifiez cette fiche (elle n'a pas été remplacée).",
                             nom=doc["nom"], date=date)
                    f["notes"] = (f.get("notes", "").rstrip() + "\n" + note).strip()
                resume["a_verifier"] += 1
                continue
            # Card never edited by hand: rebuild it from the document
            genre_fiche = genre if genre in ("compte", "contact") else existantes[0].get("type", "compte")
            propositions = filtre(deviner(doc["nom"], doc["texte"], genre_fiche))
            if len(propositions) == 1 and len(existantes) == 1:
                fiche = existantes[0]
                for cle in CHAMPS.get(fiche.get("type", "compte"), []):
                    if cle != "source":
                        fiche[cle] = ""
                fiche.update(propositions[0])
                fiche.update(source_mtime=doc["mtime"], importe_le=maintenant,
                             modifie_le=maintenant)
            else:
                ids = {f["id"] for f in existantes}
                self.fiches = [f for f in self.fiches if f["id"] not in ids]
                for champs in propositions:
                    self.nouvelle_fiche(source=chemin, source_mtime=doc["mtime"],
                                        importe_le=maintenant, **champs)
            resume["mises_a_jour"] += 1
        return resume

    def sources_connues(self):
        return {os.path.normcase(f.get("source", "")) for f in self.fiches if f.get("source")}

    # -- .txt copy of each card ------------------------------------------------
    def synchroniser_txt(self):
        """One .txt per card in the chosen folder; only writes what changed.

        Returns True if all is well (otherwise the problem is in self.message_txt).
        """
        dossier = self.reglages.get("dossier_txt", "")
        if not dossier:
            return True
        dossier = Path(dossier)
        self.message_txt = ""
        voulus = {}   # relative path -> content
        pris = set()

        renommages = {}   # new relative path -> old one (renamed card)
        connus = {os.path.normcase(r) for r in self.reglages.get("txt_connus", [])}

        def place(fiche, rel):
            pris.add(os.path.normcase(rel))
            voulus[rel] = texte_de_fiche(fiche)
            ancien = fiche.get("fichier_txt", "")
            if ancien and os.path.normcase(ancien) != os.path.normcase(rel):
                renommages[rel] = ancien
            fiche["fichier_txt"] = rel

        # 1) each card keeps its file if it still matches its name
        a_placer = []
        for fiche in sorted(self.fiches, key=lambda f: f.get("cree_le", "")):
            sous = _(SOUS_DOSSIERS_TXT.get(fiche.get("type", "compte"), "Autres"))
            base = nom_de_fichier(fiche.get("nom", ""))
            ancien = fiche.get("fichier_txt", "")
            ancien_dans_bon_dossier = ancien and Path(ancien).parent.name == sous
            stem = Path(ancien).stem if ancien else ""
            garde = (ancien_dans_bon_dossier and os.path.normcase(ancien) not in pris
                     and (stem == base or re.fullmatch(re.escape(base) + r" \(\d+\)", stem)))
            if garde:
                place(fiche, ancien)
            else:
                a_placer.append((fiche, sous, base))
        # 2) new (or renamed) cards get a free name
        for fiche, sous, base in a_placer:
            n = 1
            while True:
                rel = os.path.join(sous, (base if n == 1 else f"{base} ({n})") + ".txt")
                libre = os.path.normcase(rel) not in pris and (
                    os.path.normcase(rel) in connus or not (dossier / rel).exists())
                if libre:  # never overwrite a file that was not created by the book
                    break
                n += 1
            place(fiche, rel)

        try:
            voulus_n = {os.path.normcase(r) for r in voulus}
            # Renamed card: rename its file (instead of creating a new one)
            for rel, ancien in renommages.items():
                source, cible = dossier / ancien, dossier / rel
                if (os.path.normcase(ancien) not in voulus_n and source.exists()
                        and not cible.exists()):
                    cible.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(source, cible)
                    self._cache_txt.pop(str(source), None)
            for rel, contenu in voulus.items():
                chemin = dossier / rel
                if self._cache_txt.get(str(chemin)) == contenu:
                    continue
                try:
                    actuel = chemin.read_text(encoding="utf-8-sig")
                except OSError:
                    actuel = None
                if actuel != contenu:
                    chemin.parent.mkdir(parents=True, exist_ok=True)
                    temporaire = chemin.with_name(chemin.name + ".tmp")
                    with open(temporaire, "w", encoding="utf-8-sig", newline="\r\n") as f:
                        f.write(contenu)
                    os.replace(temporaire, chemin)
                self._cache_txt[str(chemin)] = contenu
            # 3) files of deleted cards: moved aside, never erased
            for rel in self.reglages.get("txt_connus", []):
                if os.path.normcase(rel) in voulus_n:
                    continue
                chemin = dossier / rel
                if chemin.exists():
                    if not any(os.path.normcase(r) == os.path.normcase(rel) for r in voulus):
                        corbeille = dossier / _("Fiches supprimées")
                        corbeille.mkdir(parents=True, exist_ok=True)
                        cible = corbeille / chemin.name
                        n = 2
                        while cible.exists():
                            cible = corbeille / f"{chemin.stem} ({n}){chemin.suffix}"
                            n += 1
                        os.replace(chemin, cible)
                self._cache_txt.pop(str(chemin), None)
            self.reglages["txt_connus"] = sorted(voulus)
            return True
        except OSError as exc:
            self.message_txt = str(exc)
            return False

    def changer_dossier_txt(self, nouveau):
        """New folder: everything is rewritten there (the old one is left as is)."""
        self.reglages["dossier_txt"] = str(nouveau)
        self.reglages["txt_connus"] = []
        self._cache_txt = {}
        for fiche in self.fiches:
            fiche.pop("fichier_txt", None)


SOUS_DOSSIERS_TXT = {"compte": "Mots de passe", "contact": "Contacts"}   # translated when used
_INTERDITS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_RESERVES = {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}


def nom_de_fichier(nom):
    """Valid Windows file name built from the card's name."""
    propre = _INTERDITS.sub("-", nom or "").strip().strip(".").strip()
    propre = re.sub(r"\s+", " ", propre)[:80].strip()
    if not propre or propre.upper() in _RESERVES:
        propre = (propre + " (" + _("fiche") + ")").strip() if propre else _("Sans nom")
    return propre


def _date_lisible(iso):
    try:
        return datetime.fromisoformat(iso).strftime(_("%d/%m/%Y à %H:%M"))
    except (TypeError, ValueError):
        return ""


def champ_visible(fiche, champ):
    """An optional field only appears if it is filled in or added on purpose."""
    genre = fiche.get("type", "compte")
    return (champ not in CHAMPS_FACULTATIFS.get(genre, []) or bool(fiche.get(champ))
            or champ in fiche.get("champs_ajoutes", []))


def texte_de_fiche(fiche):
    """Content of a card's .txt file (readable in Notepad)."""
    genre = fiche.get("type", "compte")
    lignes = [fiche.get("nom", "") or _("Sans nom"), "=" * max(len(fiche.get("nom", "")), 8), ""]
    blocs = []
    for champ in ORDRE_CHAMPS.get(genre, []):
        if champ == "notes" or not champ_visible(fiche, champ):
            continue
        valeur = fiche.get(champ, "")
        if champ == "adresse":
            blocs += ["", deux_points(_("Adresse")), valeur or "-"]
        else:
            lignes.append(f"{deux_points(_(LIBELLES_CHAMPS[champ]))} {valeur}")
    for perso in fiche.get("perso", []):
        lignes.append(f"{deux_points(perso.get('libelle', ''))} {perso.get('valeur', '')}")
    lignes += blocs
    lignes += ["", deux_points(_("Notes")), fiche.get("notes", "") or "-", ""]
    date = _date_lisible(fiche.get("modifie_le") or fiche.get("cree_le"))
    lignes.append("-" * 60)
    lignes.append(_("Copie automatique faite par Pocket Book (fiche modifiée le {date}).", date=date)
                  if date else _("Copie automatique faite par Pocket Book."))
    lignes.append(_("Ce fichier est réécrit à chaque changement : modifiez la fiche dans le carnet."))
    return "\n".join(lignes) + "\n"


def fiche_correspond(fiche, recherche):
    if not recherche:
        return True
    tout = " ".join(str(v) for k, v in fiche.items()
                    if k not in ("id", "type", "source", "mdp", "cree_le", "modifie_le",
                                 "perso", "champs_ajoutes", "fichier_txt"))
    tout += " " + " ".join(f"{p.get('libelle', '')} {p.get('valeur', '')}"
                           for p in fiche.get("perso", []))
    return recherche in normaliser(tout)


# ---------------------------------------------------------------------------
# Document index (background reading, with a cache)
# ---------------------------------------------------------------------------


def charger_index():
    try:
        with open(FICHIER_INDEX, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"dossier": "", "documents": {}}


def indexer(dossier, ancien_index, progression=None, exclure=()):
    """Read new or changed documents; reuse the cache for the others."""
    anciens = ancien_index.get("documents", {}) if ancien_index.get("dossier") == dossier else {}
    chemins, anciens_doc = lister_documents(dossier, exclure)
    total = len(chemins)
    nouveaux = {}
    for i, chemin in enumerate(chemins, 1):
        try:
            st = os.stat(chemin)
        except OSError:
            continue
        ancien = anciens.get(chemin)
        if ancien and ancien.get("mtime") == st.st_mtime and ancien.get("taille") == st.st_size:
            ancien.setdefault("genre", classer_document(ancien.get("texte", "")))
            nouveaux[chemin] = ancien
        else:
            try:
                texte = lire_document(chemin)
                erreur = ""
            except Exception as exc:  # damaged or protected document, renamed old .doc…
                texte = ""
                erreur = _("Impossible de lire ce document ({erreur}).", erreur=type(exc).__name__)
            nouveaux[chemin] = {"nom": Path(chemin).stem, "mtime": st.st_mtime,
                                "taille": st.st_size, "texte": texte, "erreur": erreur,
                                "genre": classer_document(texte)}
        if progression and (i % 25 == 0 or i == total):
            progression(i, total)
    return {"dossier": dossier, "documents": nouveaux, "anciens_doc": anciens_doc}


# ===========================================================================
# Interface
# ===========================================================================

import tkinter as tk  # noqa: E402  (after the logic, so it can be tested on its own)
from tkinter import filedialog, messagebox, ttk  # noqa: E402
import tkinter.font as tkfont  # noqa: E402

# Readable fonts available on each system (the first one found is used)
POLICES_TEXTE = ["Verdana", "Segoe UI", "DejaVu Sans", "Noto Sans", "Helvetica"]
POLICES_MONO = ["Consolas", "Menlo", "DejaVu Sans Mono", "Noto Sans Mono", "Courier New"]


def police_disponible(candidates):
    try:
        presentes = {f.lower() for f in tkfont.families()}
    except Exception:
        return candidates[0]
    for nom in candidates:
        if nom.lower() in presentes:
            return nom
    return candidates[-1]


def mettre_icone(fenetre):
    """Window icon: .ico on Windows, .png elsewhere."""
    try:
        if EST_WINDOWS:
            fenetre.iconbitmap(default=ressource("pocketbook.ico"))
        else:
            image = tk.PhotoImage(file=ressource("pocketbook.png"))
            fenetre.iconphoto(True, image)
            fenetre._icone = image  # keep the image in memory
    except Exception:
        pass

# Color themes (all checked for good text contrast)
THEMES = {
    "clair": {"nom": "Clair", "BLEU_TEXTE": "#1E4F91", "VERT_TEXTE": "#1F6B3A", "FOND": "#F6F4EF", "BLANC": "#FFFFFF", "ENCRE": "#1B1A17",
              "GRIS": "#4A4740", "BORDURE": "#CFC9BC", "BORDURE_FORTE": "#8C8578",
              "BLEU": "#1E4F91", "BLEU_CLAIR": "#E3ECF8", "BLEU_FONCE": "#163B6D",
              "VERT": "#1F6B3A", "VERT_FONCE": "#174F2B", "ROUGE": "#A4321F",
              "ROUGE_CLAIR": "#F6E3DF", "JAUNE_FOND": "#FFF6E5", "JAUNE_BORD": "#E0B867",
              "JAUNE_TEXTE": "#6B4A0C", "BARRE": "#EDE9E0", "LETTRE_ETEINTE": "#A8A296",
              "FOND_TEXTE": "#FBFAF7"},
    "sombre": {"nom": "Sombre", "BLEU_TEXTE": "#8DB8F0", "VERT_TEXTE": "#7FD09E", "FOND": "#1C1D20", "BLANC": "#2A2C30", "ENCRE": "#F1F0EC",
               "GRIS": "#C8C5BE", "BORDURE": "#4A4D53", "BORDURE_FORTE": "#8B8E94",
               "BLEU": "#2F6DBA", "BLEU_CLAIR": "#2F3B4E", "BLEU_FONCE": "#24578F",
               "VERT": "#23784A", "VERT_FONCE": "#1A5C38", "ROUGE": "#FF9C8A",
               "ROUGE_CLAIR": "#4A2C28", "JAUNE_FOND": "#3A3020", "JAUNE_BORD": "#B48B35",
               "JAUNE_TEXTE": "#F3D58E", "BARRE": "#25262A", "LETTRE_ETEINTE": "#6E7076",
               "FOND_TEXTE": "#232528"},
    "contraste": {"nom": "Contraste fort", "BLEU_TEXTE": "#0033A0", "VERT_TEXTE": "#00591F", "FOND": "#FFFFFF", "BLANC": "#FFFFFF",
                  "ENCRE": "#000000", "GRIS": "#000000", "BORDURE": "#000000",
                  "BORDURE_FORTE": "#000000", "BLEU": "#0033A0", "BLEU_CLAIR": "#D6E4FF",
                  "BLEU_FONCE": "#00226B", "VERT": "#00591F", "VERT_FONCE": "#003D15",
                  "ROUGE": "#B00000", "ROUGE_CLAIR": "#FFE0E0", "JAUNE_FOND": "#FFF4B3",
                  "JAUNE_BORD": "#000000", "JAUNE_TEXTE": "#000000", "BARRE": "#F0F0F0",
                  "LETTRE_ETEINTE": "#8A8A8A", "FOND_TEXTE": "#FFFFFF"},
    "sepia": {"nom": "Sépia doux", "BLEU_TEXTE": "#7A4416", "VERT_TEXTE": "#3D6B29", "FOND": "#F2E8D5", "BLANC": "#FBF5E9", "ENCRE": "#2B2116",
              "GRIS": "#5B4A36", "BORDURE": "#D5C3A1", "BORDURE_FORTE": "#9C8768",
              "BLEU": "#7A4416", "BLEU_CLAIR": "#EEDCC0", "BLEU_FONCE": "#5C3210",
              "VERT": "#3D6B29", "VERT_FONCE": "#2C5020", "ROUGE": "#9E2F1C",
              "ROUGE_CLAIR": "#F3DCD3", "JAUNE_FOND": "#FFF3D6", "JAUNE_BORD": "#D2A852",
              "JAUNE_TEXTE": "#5E410B", "BARRE": "#EADCC2", "LETTRE_ETEINTE": "#B0A089",
              "FOND_TEXTE": "#FDF9F0"},
}
SUR_ACCENT = "#FFFFFF"   # text on blue / green buttons, whatever the theme


def appliquer_theme_couleurs(nom):
    """Change the colors used by the whole interface."""
    globals().update({k: v for k, v in THEMES.get(nom, THEMES["clair"]).items() if k != "nom"})


appliquer_theme_couleurs("clair")

TAILLES = [12, 14, 17, 20]          # text sizes (points)
LETTRES = ["Tout"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["#"]
ETIQUETTES_GENRE = {"compte": "Mot de passe", "contact": "Contact", "autre": "?"}
NOMS_GENRE = {"compte": "un mot de passe", "contact": "un contact", "autre": "non reconnu"}
def couleur_genre(genre):
    return {"compte": BLEU_TEXTE, "contact": VERT_TEXTE}.get(genre, GRIS)


class Application:
    def __init__(self, racine):
        self.racine = racine
        self.carnet = Carnet()
        self.carnet.charger()
        try:
            self.carnet.sauvegarde_du_jour()
        except OSError:
            pass

        self.page = "compte"
        self.lettre = "Tout"
        self.id_courant = None
        self._chargement = False
        self._minuterie = None
        self._minuterie_recherche = None
        self.index = charger_index()
        self.file_messages = queue.Queue()
        self.lecture_en_cours = False
        self.chemins_affiches = []
        self.ids_affiches = []
        self._cache_recherche = {}
        self._alerte_txt_montree = False
        self._synchro_demandee = False

        # Language: the book's, otherwise the system's (or the one chosen at installation)
        if LANGUE_IMPOSEE[0]:
            self.carnet.reglages["langue"] = LANGUE_IMPOSEE[0]
        choisir_langue(self.carnet.reglages.get("langue") or langue_actuelle())
        self.carnet.reglages["langue"] = langue_actuelle()
        appliquer_theme_couleurs(self.carnet.reglages.get("theme", "clair"))
        self._polices()
        self._fenetre()
        self._construire()
        self.appliquer_taille(self.carnet.reglages.get("taille_texte", 1), enregistrer=False)
        self.afficher_page("compte")
        self.racine.after(50, self._apres_ouverture)
        self.racine.after(300, self._activer_glisser_deposer)
        self.racine.after(60000, self._synchro_periodique)

    # ------------------------------------------------------------------ base
    def _polices(self):
        famille = police_disponible(POLICES_TEXTE)
        self.famille = famille
        self.f_base = tkfont.Font(family=famille, size=14)
        self.f_gras = tkfont.Font(family=famille, size=14, weight="bold")
        self.f_petit = tkfont.Font(family=famille, size=12)
        self.f_titre = tkfont.Font(family=famille, size=20, weight="bold")
        self.f_mdp = tkfont.Font(family=police_disponible(POLICES_MONO), size=20, weight="bold")
        self.f_lettre = tkfont.Font(family=famille, size=13, weight="bold")

    def _fenetre(self):
        r = self.racine
        r.title(NOM_APPLI)
        r.configure(bg=FOND)
        r.minsize(900, 600)
        try:
            if EST_LINUX:
                r.attributes("-zoomed", True)
            else:
                r.state("zoomed")
        except tk.TclError:
            r.geometry("1280x860")
        r.protocol("WM_DELETE_WINDOW", self.quitter)
        mettre_icone(r)
        r.option_add("*TCombobox*Listbox.font", self.f_base)
        self._style()

    def _style(self):
        """Colors of drop-down lists and scrollbars (according to the theme)."""
        r = self.racine
        r.option_add("*TCombobox*Listbox.background", BLANC)
        r.option_add("*TCombobox*Listbox.foreground", ENCRE)
        r.option_add("*TCombobox*Listbox.selectBackground", BLEU)
        r.option_add("*TCombobox*Listbox.selectForeground", SUR_ACCENT)
        style = ttk.Style(r)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TCombobox", padding=6, fieldbackground=BLANC, background=BLANC,
                        foreground=ENCRE, arrowcolor=ENCRE, arrowsize=22,
                        bordercolor=BORDURE_FORTE)
        style.map("TCombobox", fieldbackground=[("readonly", BLANC)],
                  foreground=[("readonly", ENCRE)], selectbackground=[("readonly", BLANC)],
                  selectforeground=[("readonly", ENCRE)])
        style.configure("Vertical.TScrollbar", arrowsize=22, width=22, background=BARRE,
                        troughcolor=FOND, arrowcolor=ENCRE, bordercolor=BORDURE)

    def bouton(self, parent, texte, commande, genre="normal", police=None, **options):
        couleurs = {
            "normal": (BLANC, ENCRE, BLEU_CLAIR),
            "bleu": (BLEU, SUR_ACCENT, BLEU_FONCE),
            "vert": (VERT, SUR_ACCENT, VERT_FONCE),
            "danger": (BLANC, ROUGE, ROUGE_CLAIR),
            "contour_bleu": (BLANC, BLEU_TEXTE, BLEU_CLAIR),
        }[genre]
        b = tk.Button(parent, text=texte, command=commande, font=police or self.f_gras,
                      bg=couleurs[0], fg=couleurs[1], activebackground=couleurs[2],
                      activeforeground=couleurs[1] if genre != "bleu" and genre != "vert" else SUR_ACCENT,
                      relief="solid", bd=1, padx=14, pady=6, cursor="hand2",
                      highlightthickness=0, **options)
        return b

    def champ_texte(self, parent, variable, police=None):
        return tk.Entry(parent, textvariable=variable, font=police or self.f_base,
                        bg=BLANC, fg=ENCRE, relief="solid", bd=1, insertbackground=ENCRE,
                        highlightthickness=2, highlightcolor="#E08A1E",
                        highlightbackground=BORDURE, insertwidth=3)

    # ------------------------------------------------------------ construction
    def _construire(self):
        r = self.racine

        # --- Header
        # 1st line: title + text size; 2nd line: the tabs (which wrap
        # when the window is narrow or the text very large).
        entete = tk.Frame(r, bg=BLANC, padx=16, pady=8)
        entete.pack(fill="x")
        tk.Frame(r, bg=BORDURE, height=2).pack(fill="x")
        ligne_titre = tk.Frame(entete, bg=BLANC)
        ligne_titre.pack(fill="x")
        tk.Label(ligne_titre, text=NOM_APPLI, font=self.f_titre, bg=BLANC,
                 fg=ENCRE).pack(side="left")
        self.zone_onglets = tk.Frame(entete, bg=BLANC)
        self.zone_onglets.pack(fill="x", pady=(6, 0))
        self.onglets = {}
        for page, texte in (("compte", _("Mes mots de passe")), ("contact", _("Mes contacts")),
                            ("documents", _("Mes documents")), ("reglages", "⚙ " + _("Réglages"))):
            self.onglets[page] = self.bouton(self.zone_onglets, texte,
                                             lambda p=page: self.afficher_page(p))
        self.zone_onglets.bind("<Configure>", lambda e: self._placer_en_lignes(
            self.zone_onglets, list(self.onglets.values()), ecart=6))

        zone_taille = tk.Frame(ligne_titre, bg=BLANC)
        zone_taille.pack(side="right")
        tk.Label(zone_taille, text=_("Texte"), font=self.f_gras, bg=BLANC,
                 fg=GRIS).pack(side="left", padx=(0, 8))
        self.boutons_taille = []
        for i in range(len(TAILLES)):
            police = tkfont.Font(family=self.famille, size=11 + i * 4, weight="bold")
            b = tk.Button(zone_taille, text=_("A"), font=police, width=2,
                          command=lambda i=i: self.appliquer_taille(i),
                          relief="solid", bd=1, cursor="hand2", highlightthickness=0)
            b.pack(side="left", padx=3)
            self.boutons_taille.append(b)

        # --- Letter bar
        self.barre_lettres = tk.Frame(r, bg=BARRE, padx=12, pady=8)
        self.barre_lettres.pack(fill="x")
        self.sep_lettres = tk.Frame(r, bg=BORDURE, height=1)
        self.sep_lettres.pack(fill="x")
        self.boutons_lettres = {}
        for lettre in LETTRES:
            b = tk.Button(self.barre_lettres, text=_(lettre) if lettre == "Tout" else lettre, font=self.f_lettre,
                          relief="solid", bd=1, cursor="hand2", highlightthickness=0,
                          padx=8 if lettre == "Tout" else 0, width=0 if lettre == "Tout" else 2,
                          command=lambda l=lettre: self.choisir_lettre(l))
            self.boutons_lettres[lettre] = b
        self.barre_lettres.bind("<Configure>", lambda e: self._placer_lettres())

        # --- Footer (before the center so it stays visible)
        pied = tk.Frame(r, bg=BLANC, padx=16, pady=8)
        pied.pack(side="bottom", fill="x")
        tk.Frame(r, bg=BORDURE, height=2).pack(side="bottom", fill="x")
        # The button first: if the window is narrow, the sentence gets cut instead.
        self.bouton(pied, _("Enregistrer maintenant"), self.enregistrer_maintenant,
                    "vert").pack(side="right")
        self.etiquette_etat = tk.Label(pied, text="", font=self.f_gras, bg=BLANC, fg=VERT_TEXTE)
        self.etiquette_etat.pack(side="left")
        self.etiquette_synchro = tk.Label(pied, text="", font=self.f_petit, bg=BLANC, fg=GRIS)
        self.etiquette_synchro.pack(side="left", padx=(16, 0))

        # --- Center
        self.centre = tk.Frame(r, bg=FOND)
        self.centre.pack(fill="both", expand=True)
        self._page_fiches()
        self._page_documents()
        self._page_reglages()

    def _placer_lettres(self):
        """Lay the letters out on one or more lines depending on the width."""
        self._placer_en_lignes(self.barre_lettres, [self.boutons_lettres[l] for l in LETTRES],
                               marge=24, ecart=3)

    def _placer_en_lignes(self, cadre, boutons, marge=0, ecart=3):
        """Place buttons from left to right, wrapping to a new line if needed."""
        largeur_dispo = max(cadre.winfo_width() - marge, 200)
        ligne, colonne, x = 0, 0, 0
        for b in boutons:
            w = b.winfo_reqwidth() + 2 * ecart
            if x + w > largeur_dispo and colonne > 0:
                ligne, colonne, x = ligne + 1, 0, 0
            b.grid(row=ligne, column=colonne, padx=ecart, pady=3, sticky="nsew")
            colonne += 1
            x += w

    # ----------------------------------------------------------- cards page
    def _page_fiches(self):
        """A single page, showing either the passwords or the contacts."""
        p = self.page_fiches = tk.Frame(self.centre, bg=FOND, padx=16, pady=12)

        gauche = tk.Frame(p, bg=FOND)
        gauche.pack(side="left", fill="y", padx=(0, 16))
        self.titre_recherche = tk.Label(gauche, text="", font=self.f_gras, bg=FOND,
                                        fg=ENCRE, anchor="w")
        self.titre_recherche.pack(fill="x")
        self.var_recherche = tk.StringVar()
        self.var_recherche.trace_add("write", lambda *a: self._recherche_fiches_changee())
        self.champ_texte(gauche, self.var_recherche).pack(fill="x", ipady=4, pady=(2, 6))

        ligne_cat = tk.Frame(gauche, bg=FOND)
        ligne_cat.pack(fill="x", pady=(0, 4))
        tk.Label(ligne_cat, text=_("Catégorie :"), font=self.f_petit, bg=FOND,
                 fg=GRIS).pack(side="left")
        self.var_filtre_cat = tk.StringVar(value=toutes_categories())
        self.choix_filtre_cat = ttk.Combobox(ligne_cat, textvariable=self.var_filtre_cat,
                                             font=self.f_petit, state="readonly", width=16)
        self.choix_filtre_cat.pack(side="left", padx=(6, 0), fill="x", expand=True)
        self.choix_filtre_cat.bind("<<ComboboxSelected>>", lambda e: self.remplir_liste_fiches())

        self.etiquette_compte = tk.Label(gauche, text="", font=self.f_petit, bg=FOND,
                                         fg=GRIS, anchor="w")
        self.etiquette_compte.pack(fill="x")

        cadre_liste = tk.Frame(gauche, bg=FOND)
        cadre_liste.pack(fill="both", expand=True, pady=6)
        self.liste_fiches = tk.Listbox(
            cadre_liste, font=self.f_base, width=26, activestyle="none",
            bg=BLANC, fg=ENCRE, selectbackground=BLEU, selectforeground=SUR_ACCENT,
            relief="solid", bd=1, highlightthickness=0, exportselection=False)
        barre = ttk.Scrollbar(cadre_liste, orient="vertical",
                              command=self.liste_fiches.yview)
        self.liste_fiches.configure(yscrollcommand=barre.set)
        self.liste_fiches.pack(side="left", fill="both", expand=True)
        barre.pack(side="right", fill="y")
        self.liste_fiches.bind("<<ListboxSelect>>", lambda e: self._fiche_choisie())

        self.bouton_nouvelle = self.bouton(gauche, "", self.creer_fiche, "contour_bleu")
        self.bouton_nouvelle.pack(fill="x", pady=(4, 0))

        # Right side: the card, built from its fields
        self.droite = tk.Frame(p, bg=BLANC, padx=22, pady=16,
                               highlightthickness=2, highlightbackground=BORDURE)
        self.droite.pack(side="left", fill="both", expand=True)
        self.aucune_fiche = tk.Label(self.droite, text="", font=self.f_base, bg=BLANC,
                                     fg=GRIS, justify="left")
        self.zone_formulaire = tk.Frame(self.droite, bg=BLANC)
        self.vars_fiche = {}
        self.textes_fiche = {}
        self.widgets_fiche = {}
        self.champ_nom = None
        self._focus_apres = None

    # ------------------------------------------------------------- card form
    def _var_fiche(self, cle, valeur, index_perso=None):
        var = tk.StringVar(value=valeur)
        var.trace_add("write", lambda *a: self._valeur_changee(cle, var.get(), index_perso))
        self.vars_fiche[cle if index_perso is None else ("perso", index_perso)] = var
        return var

    def _zone_texte_fiche(self, parent, cle, valeur, hauteur):
        zone = tk.Text(parent, font=self.f_base, height=hauteur, wrap="word",
                       bg=BLANC, fg=ENCRE, relief="solid", bd=1, insertbackground=ENCRE,
                       highlightthickness=2, highlightcolor="#E08A1E",
                       highlightbackground=BORDURE, padx=8, pady=6,
                       insertwidth=3, undo=True)
        zone.insert("1.0", valeur)
        zone.edit_modified(False)
        zone.edit_reset()
        zone.bind("<<Modified>>", lambda e: self._texte_change(cle))
        self.textes_fiche[cle] = zone
        return zone

    def _bouton_retirer(self, parent, ligne, cle, index_perso=None):
        b = tk.Button(parent, text="✕", font=self.f_gras, width=2, command=lambda:
                      self.retirer_champ(cle, index_perso), bg=BLANC, fg=ROUGE,
                      activebackground=ROUGE_CLAIR, activeforeground=ROUGE,
                      relief="solid", bd=1, cursor="hand2", highlightthickness=0)
        b.grid(row=ligne, column=3, sticky="n", padx=(6, 0), pady=5)
        return b

    def _libelle(self, parent, ligne, texte, haut=False):
        tk.Label(parent, text=texte, font=self.f_gras, bg=BLANC, fg=GRIS, anchor="w",
                 justify="left", wraplength=220).grid(
            row=ligne, column=0, sticky="nw" if haut else "w", pady=5, padx=(0, 12))

    def _construire_formulaire(self, fiche):
        for w in self.zone_formulaire.winfo_children():
            w.destroy()
        self.vars_fiche, self.textes_fiche, self.widgets_fiche = {}, {}, {}
        genre = fiche.get("type", "compte")
        facultatifs = CHAMPS_FACULTATIFS.get(genre, [])
        self._chargement = True

        f = tk.Frame(self.zone_formulaire, bg=BLANC)
        f.pack(fill="both", expand=True)
        f.columnconfigure(1, weight=1)
        r = 0
        self._libelle(f, r, _("Nom"))
        self.champ_nom = self.champ_texte(f, self._var_fiche("nom", fiche.get("nom", "")),
                                          self.f_titre)
        self.champ_nom.grid(row=r, column=1, columnspan=3, sticky="ew", pady=5, ipady=2)
        r += 1

        for champ in ORDRE_CHAMPS.get(genre, []):
            if champ == "notes" or not champ_visible(fiche, champ):
                continue
            libelle = _(LIBELLES_CHAMPS[champ])
            valeur = fiche.get(champ, "")
            if champ == "mdp":
                self._cadre_mot_de_passe(f, r, valeur)
            elif champ == "categorie":
                self._libelle(f, r, libelle)
                cadre = tk.Frame(f, bg=BLANC)
                cadre.grid(row=r, column=1, columnspan=2, sticky="w", pady=5)
                valeurs = [sans_categorie()] + self.carnet.noms_categories()
                choix = ttk.Combobox(cadre, textvariable=self._var_fiche(
                    "categorie", valeur or sans_categorie()), values=valeurs,
                    font=self.f_base, state="readonly", width=18)
                choix.pack(side="left")
                self.pastille_categorie = tk.Label(cadre, text="   ", font=self.f_base,
                                                   bg=self.carnet.couleur_categorie(valeur) or BLANC,
                                                   relief="solid", bd=1 if valeur else 0)
                self.pastille_categorie.pack(side="left", padx=(8, 0), ipadx=4)
                self.widgets_fiche[champ] = choix
                self._bouton_retirer(f, r, champ)
            elif champ == "adresse":
                self._libelle(f, r, libelle, haut=True)
                zone = self._zone_texte_fiche(f, champ, valeur, 3)
                zone.grid(row=r, column=1, sticky="ew", pady=5)
                b = self.bouton(f, _("Copier"), None)
                b.configure(command=lambda b=b: self.copier(
                    self.textes_fiche["adresse"].get("1.0", "end-1c"), b))
                b.grid(row=r, column=2, sticky="new", padx=(10, 0), pady=5)
                self.widgets_fiche[champ] = zone
                if champ in facultatifs:
                    self._bouton_retirer(f, r, champ)
            else:
                self._libelle(f, r, libelle)
                champ_saisie = self.champ_texte(f, self._var_fiche(champ, valeur))
                champ_saisie.grid(row=r, column=1, sticky="ew", pady=5, ipady=4)
                self.widgets_fiche[champ] = champ_saisie
                if champ == "site":
                    b = self.bouton(f, _("Ouvrir"), self.ouvrir_site)
                elif champ == "anniversaire":
                    b = None
                else:
                    b = self.bouton(f, _("Copier"), None)
                    b.configure(command=lambda b=b, c=champ: self.copier(
                        self.vars_fiche[c].get(), b))
                if b is not None:
                    b.grid(row=r, column=2, sticky="ew", padx=(10, 0), pady=5)
                if champ in facultatifs:
                    self._bouton_retirer(f, r, champ)
            r += 1

        # Fields added by hand (customer no., secret question…)
        for i, perso in enumerate(fiche.get("perso", [])):
            self._libelle(f, r, perso.get("libelle", "") or _("Champ"))
            champ_saisie = self.champ_texte(f, self._var_fiche("perso", perso.get("valeur", ""), i))
            champ_saisie.grid(row=r, column=1, sticky="ew", pady=5, ipady=4)
            self.widgets_fiche[("perso", i)] = champ_saisie
            b = self.bouton(f, _("Copier"), None)
            b.configure(command=lambda b=b, i=i: self.copier(self.vars_fiche[("perso", i)].get(), b))
            b.grid(row=r, column=2, sticky="ew", padx=(10, 0), pady=5)
            self._bouton_retirer(f, r, "perso", i)
            r += 1

        self.bouton(f, _("＋  Ajouter un champ"), self.ajouter_champ, "contour_bleu",
                    police=self.f_petit).grid(row=r, column=1, sticky="w", pady=(4, 6))
        r += 1

        self._libelle(f, r, _("Notes"), haut=True)
        notes = self._zone_texte_fiche(f, "notes", fiche.get("notes", ""), 4)
        notes.grid(row=r, column=1, columnspan=3, sticky="nsew", pady=5)
        f.rowconfigure(r, weight=1)
        r += 1

        source = fiche.get("source", "")
        tk.Label(f, text=(_("Venu du document : ") + Path(source).name) if source else "",
                 font=self.f_petit, bg=BLANC, fg=GRIS, anchor="w").grid(
            row=r, column=0, columnspan=4, sticky="w", pady=(4, 0))
        r += 1
        ouvrir = tk.Frame(f, bg=BLANC)
        ouvrir.grid(row=r, column=0, columnspan=4, sticky="w", pady=(4, 0))
        tk.Label(ouvrir, text=_("Ouvrir sur l'ordinateur :"), font=self.f_petit, bg=BLANC,
                 fg=GRIS).pack(side="left", padx=(0, 8))
        self.bouton(ouvrir, _("La copie .txt"), lambda: self.ouvrir_fichier_fiche("txt"),
                    police=self.f_petit).pack(side="left")
        if source:
            self.bouton(ouvrir, _("Le document d'origine"), lambda: self.ouvrir_fichier_fiche("source"),
                        police=self.f_petit).pack(side="left", padx=(8, 0))
        self.bouton(ouvrir, _("Le dossier"), lambda: self.ouvrir_fichier_fiche("dossier"),
                    police=self.f_petit).pack(side="left", padx=(8, 0))
        r += 1
        self.bouton(f, _("Supprimer ce contact") if genre == "contact" else _("Supprimer cette fiche"),
                    self.supprimer_fiche, "danger").grid(row=r, column=1, columnspan=3,
                                                         sticky="e", pady=(10, 0))
        self._chargement = False

        if self._focus_apres is not None:
            widget = self.widgets_fiche.get(self._focus_apres)
            self._focus_apres = None
            if widget is not None:
                widget.focus_set()

    def _cadre_mot_de_passe(self, f, r, valeur):
        cadre = tk.Frame(f, bg=JAUNE_FOND, padx=14, pady=10,
                         highlightthickness=2, highlightbackground=JAUNE_BORD)
        cadre.grid(row=r, column=0, columnspan=4, sticky="ew", pady=(12, 8))
        cadre.columnconfigure(0, weight=1)
        tk.Label(cadre, text=_("Mot de passe"), font=self.f_gras, bg=JAUNE_FOND,
                 fg=JAUNE_TEXTE, anchor="w").grid(row=0, column=0, sticky="w")
        # Password already saved: locked (avoids erasing it by mistake)
        verrouille = bool(valeur)
        saisie = tk.Entry(cadre, textvariable=self._var_fiche("mdp", valeur), font=self.f_mdp,
                          bg=BLANC, fg=ENCRE, relief="solid", bd=1, highlightthickness=2,
                          insertbackground=ENCRE, highlightcolor="#E08A1E",
                          highlightbackground=JAUNE_BORD, insertwidth=3,
                          readonlybackground=BLANC, state="readonly" if verrouille else "normal")
        saisie.grid(row=1, column=0, sticky="ew", pady=(6, 8), ipady=4)
        self.widgets_fiche["mdp"] = saisie
        boutons = tk.Frame(cadre, bg=JAUNE_FOND)
        boutons.grid(row=2, column=0, sticky="w")
        b = self.bouton(boutons, _("Copier"), None)
        b.configure(command=lambda: self.copier(self.vars_fiche["mdp"].get(), b))
        b.pack(side="left", padx=(0, 10))
        bouton_modifier = self.bouton(boutons, _("✎  Modifier à la main"), None)

        def basculer():
            if saisie.cget("state") == "readonly":
                saisie.configure(state="normal")
                saisie.focus_set()
                saisie.icursor("end")
                bouton_modifier.configure(text=_("✔  Terminé"))
            else:
                saisie.configure(state="readonly")
                bouton_modifier.configure(text=_("✎  Modifier à la main"))

        bouton_modifier.configure(command=basculer)
        if verrouille:
            bouton_modifier.pack(side="left", padx=(0, 10))
        self.bouton(boutons, _("↻  Créer un nouveau mot de passe"),
                    self.ouvrir_generateur, "bleu").pack(side="left")

    # ------------------------------------------------------ changes in the card
    def _valeur_changee(self, cle, valeur, index_perso=None):
        if self._chargement:
            return
        fiche = self.carnet.trouver(self.id_courant)
        if fiche is None:
            return
        if index_perso is not None:
            persos = fiche.get("perso", [])
            if index_perso < len(persos):
                persos[index_perso]["valeur"] = valeur
        else:
            if cle == "categorie" and valeur == sans_categorie():
                valeur = ""
            fiche[cle] = valeur
            if cle in ("nom", "categorie"):
                self._maj_ligne_liste(fiche)
            if cle == "categorie" and hasattr(self, "pastille_categorie"):
                couleur = self.carnet.couleur_categorie(valeur)
                self.pastille_categorie.configure(bg=couleur or BLANC, bd=1 if couleur else 0)
        fiche["modifie_le"] = datetime.now().isoformat(timespec="seconds")
        fiche["modifiee_a_la_main"] = True   # synchronization will not overwrite it
        self.programmer_enregistrement()

    def _texte_change(self, cle):
        zone = self.textes_fiche.get(cle)
        if zone is None or not zone.edit_modified():
            return
        zone.edit_modified(False)
        self._valeur_changee(cle, zone.get("1.0", "end-1c"))

    def _maj_ligne_liste(self, fiche):
        if fiche["id"] not in self.ids_affiches:
            return
        i = self.ids_affiches.index(fiche["id"])
        self.liste_fiches.delete(i)
        self.liste_fiches.insert(i, "  " + (fiche["nom"] or _("Sans nom")))
        self._colorer_ligne(i, fiche)
        self.liste_fiches.selection_set(i)

    def _colorer_ligne(self, i, fiche):
        couleur = self.carnet.couleur_categorie(fiche.get("categorie", ""))
        if couleur:
            self.liste_fiches.itemconfig(i, background=couleur, foreground=TEXTE_SUR_PASTEL)
        else:
            self.liste_fiches.itemconfig(i, background=BLANC, foreground=ENCRE)

    def ajouter_champ(self):
        fiche = self.carnet.trouver(self.id_courant)
        if fiche is None:
            return
        genre = fiche.get("type", "compte")
        manquants = [c for c in CHAMPS_FACULTATIFS.get(genre, []) if not champ_visible(fiche, c)]

        f = tk.Toplevel(self.racine)
        f.title(_("Ajouter un champ"))
        f.configure(bg=BLANC, padx=24, pady=18)
        f.transient(self.racine)
        f.resizable(False, False)
        tk.Label(f, text=_("Quel champ ajouter à cette fiche ?"), font=self.f_gras,
                 bg=BLANC, fg=ENCRE).pack(anchor="w", pady=(0, 10))

        def ajouter_standard(champ):
            fiche.setdefault("champs_ajoutes", []).append(champ)
            self._focus_apres = champ
            f.destroy()
            self.montrer_fiche(fiche)
            self.programmer_enregistrement()

        if manquants:
            ligne = tk.Frame(f, bg=BLANC)
            ligne.pack(anchor="w", pady=(0, 12))
            for champ in manquants:
                self.bouton(ligne, _(LIBELLES_CHAMPS[champ]),
                            lambda c=champ: ajouter_standard(c)).pack(side="left", padx=(0, 8))

        tk.Label(f, text=_("Ou un autre champ, à nommer (ex. : Numéro client, Question secrète) :"),
                 font=self.f_petit, bg=BLANC, fg=GRIS).pack(anchor="w")
        var_nom = tk.StringVar()
        saisie = self.champ_texte(f, var_nom)
        saisie.pack(fill="x", ipady=4, pady=(4, 12))

        def ajouter_perso(_evenement=None):
            nom = var_nom.get().strip()
            if not nom:
                saisie.focus_set()
                return
            fiche.setdefault("perso", []).append({"libelle": nom, "valeur": ""})
            self._focus_apres = ("perso", len(fiche["perso"]) - 1)
            f.destroy()
            self.montrer_fiche(fiche)
            self.programmer_enregistrement()

        saisie.bind("<Return>", ajouter_perso)
        boutons = tk.Frame(f, bg=BLANC)
        boutons.pack(fill="x")
        self.bouton(boutons, _("Annuler"), f.destroy).pack(side="right")
        self.bouton(boutons, _("＋  Ajouter ce champ"), ajouter_perso, "bleu").pack(side="right", padx=10)
        f.grab_set()
        saisie.focus_set()

    def retirer_champ(self, cle, index_perso=None):
        fiche = self.carnet.trouver(self.id_courant)
        if fiche is None:
            return
        if index_perso is not None:
            persos = fiche.get("perso", [])
            if index_perso >= len(persos):
                return
            libelle, valeur = persos[index_perso].get("libelle", ""), persos[index_perso].get("valeur", "")
        else:
            libelle, valeur = _(LIBELLES_CHAMPS.get(cle, cle)), fiche.get(cle, "")
        if valeur and not messagebox.askyesno(
                _("Retirer le champ ?"),
                _("Retirer « {champ} » de cette fiche ?\n\nCe qui est écrit dedans sera effacé :",
                  champ=libelle) + "\n" + valeur,
                icon="warning", default="no"):
            return
        if index_perso is not None:
            del fiche["perso"][index_perso]
        else:
            fiche[cle] = ""
            if cle in fiche.get("champs_ajoutes", []):
                fiche["champs_ajoutes"].remove(cle)
            if cle == "categorie":
                self._maj_ligne_liste(fiche)
        fiche["modifie_le"] = datetime.now().isoformat(timespec="seconds")
        fiche["modifiee_a_la_main"] = True   # synchronization will not overwrite it
        self.montrer_fiche(fiche)
        self.programmer_enregistrement()

    # ---------------------------------------------------------- settings page
    def _carte(self, parent, titre, explication=""):
        carte = tk.Frame(parent, bg=BLANC, padx=20, pady=16,
                         highlightthickness=2, highlightbackground=BORDURE)
        tk.Label(carte, text=titre, font=self.f_titre, bg=BLANC, fg=ENCRE,
                 anchor="w").pack(fill="x")
        if explication:
            tk.Label(carte, text=explication, font=self.f_petit, bg=BLANC, fg=GRIS,
                     anchor="w", justify="left", wraplength=520).pack(fill="x", pady=(2, 10))
        return carte

    def _page_reglages(self):
        p = self.page_reglages = tk.Frame(self.centre, bg=FOND, padx=16, pady=12)

        colonne_gauche = tk.Frame(p, bg=FOND)
        colonne_gauche.pack(side="left", fill="both", expand=True, padx=(0, 16))

        # --- About (bottom left)
        apropos = self._carte(colonne_gauche, _("À propos"),
                              _("Pocket Book {version} — fonctionne entièrement sans internet : "
                                "rien ne quitte cet ordinateur.", version=VERSION))
        apropos.pack(side="bottom", fill="x", pady=(16, 0))
        tk.Label(apropos, text=_("Vos données sont ici :") + f"\n{DOSSIER_DONNEES}", font=self.f_petit,
                 bg=BLANC, fg=ENCRE, anchor="w", justify="left", wraplength=520).pack(fill="x")
        ligne_apropos = tk.Frame(apropos, bg=BLANC)
        ligne_apropos.pack(fill="x", pady=(10, 0))
        self.bouton(ligne_apropos, _("Ouvrir le dossier des données"),
                    lambda: ouvrir_avec_systeme(DOSSIER_DONNEES)).pack(side="left")
        if installation_possible() and meme_fichier(sys.executable, chemins_installation()["exe"]):
            self.bouton(ligne_apropos, _("Désinstaller…"), self.desinstaller_depuis_reglages,
                        "danger").pack(side="right")

        # --- Categories
        cat = self._carte(colonne_gauche, _("Catégories"),
                          _("Les catégories servent à trier les fiches. Chacune a sa couleur, "
                          "qui apparaît dans la liste des fiches."))
        cat.pack(side="top", fill="both", expand=True)
        cadre = tk.Frame(cat, bg=BLANC)
        cadre.pack(fill="both", expand=True)
        self.liste_categories = tk.Listbox(
            cadre, font=self.f_base, activestyle="none", height=10,
            bg=BLANC, fg=ENCRE, selectbackground=BLEU, selectforeground=SUR_ACCENT,
            relief="solid", bd=1, highlightthickness=0, exportselection=False)
        barre = ttk.Scrollbar(cadre, orient="vertical", command=self.liste_categories.yview)
        self.liste_categories.configure(yscrollcommand=barre.set)
        self.liste_categories.pack(side="left", fill="both", expand=True)
        barre.pack(side="right", fill="y")
        boutons = tk.Frame(cat, bg=BLANC)
        boutons.pack(fill="x", pady=(10, 0))
        self.bouton(boutons, _("＋  Nouvelle"), self.nouvelle_categorie, "bleu").pack(side="left")
        self.bouton(boutons, _("Renommer"), self.renommer_categorie).pack(side="left", padx=(8, 0))
        self.bouton(boutons, _("Couleur…"), self.couleur_categorie).pack(side="left", padx=(8, 0))
        self.bouton(boutons, _("Supprimer"), self.supprimer_categorie, "danger").pack(side="right")

        droite = tk.Frame(p, bg=FOND)
        droite.pack(side="left", fill="both", expand=True)

        # --- Language
        langue = self._carte(droite, _("Langue"))
        langue.pack(fill="x", pady=(0, 16))
        ligne_langues = tk.Frame(langue, bg=BLANC)
        ligne_langues.pack(fill="x")
        for code, nom in LANGUES.items():
            actif = code == langue_actuelle()
            tk.Button(ligne_langues, text=("✔ " if actif else "") + nom, font=self.f_gras,
                      bg=BLEU if actif else BLANC, fg=SUR_ACCENT if actif else ENCRE,
                      activebackground=BLEU_FONCE if actif else BLEU_CLAIR,
                      activeforeground=SUR_ACCENT if actif else ENCRE, relief="solid", bd=1,
                      padx=10, pady=6, cursor="hand2", highlightthickness=0,
                      command=lambda c=code: self.choisir_langue_interface(c)).pack(
                side="left", padx=(0, 6), pady=2)

        # --- Themes
        theme = self._carte(droite, _("Couleurs de l'écran"),
                            _("Choisissez ce qui est le plus agréable à lire."))
        theme.pack(fill="x")
        grille = tk.Frame(theme, bg=BLANC)
        grille.pack(fill="x")
        actuel = self.carnet.reglages.get("theme", "clair")
        for i, (cle, t) in enumerate(THEMES.items()):
            actif = cle == actuel
            b = tk.Button(grille, text=("✔  " if actif else "") + _(t["nom"]), font=self.f_gras,
                          bg=t["FOND"], fg=t["ENCRE"], activebackground=t["BLANC"],
                          activeforeground=t["ENCRE"], relief="solid", bd=4 if actif else 1,
                          padx=14, pady=12, cursor="hand2", highlightthickness=0,
                          command=lambda c=cle: self.choisir_theme(c))
            b.grid(row=i // 2, column=i % 2, sticky="ew", padx=4, pady=4)
        grille.columnconfigure(0, weight=1)
        grille.columnconfigure(1, weight=1)

        # --- .txt copy
        txt = self._carte(droite, _("Copie des fiches en .txt"),
                          _("Chaque fiche est recopiée dans un fichier .txt, mis à jour tout seul. "
                          "Les changements se font dans le carnet, pas dans les .txt."))
        txt.pack(fill="x", pady=(16, 0))
        self.etiquette_txt = tk.Label(txt, text="", font=self.f_petit, bg=BLANC, fg=ENCRE,
                                      anchor="w", justify="left", wraplength=520)
        self.etiquette_txt.pack(fill="x")
        ligne = tk.Frame(txt, bg=BLANC)
        ligne.pack(fill="x", pady=(10, 0))
        self.bouton(ligne, _("Changer de dossier…"), self.choisir_dossier_txt).pack(side="left")
        self.bouton(ligne, _("Ouvrir le dossier"), self.ouvrir_dossier_txt).pack(side="left", padx=8)

    def desinstaller_depuis_reglages(self):
        self.enregistrer()
        if fenetre_desinstallation(self.racine):
            self.racine.destroy()

    def remplir_categories(self, choisir=None):
        self.liste_categories.delete(0, "end")
        for i, c in enumerate(self.carnet.categories()):
            n = self.carnet.nb_fiches_categorie(c["nom"])
            self.liste_categories.insert("end", f"  {c['nom']}   (" + n_(n, "{n} fiche", "{n} fiches") + ")")
            self.liste_categories.itemconfig(i, background=c.get("couleur") or BLANC,
                                             foreground=TEXTE_SUR_PASTEL if c.get("couleur") else ENCRE)
            if c["nom"] == choisir:
                self.liste_categories.selection_set(i)
                self.liste_categories.see(i)

    def _categorie_choisie(self):
        choix = self.liste_categories.curselection()
        if not choix:
            messagebox.showinfo(NOM_APPLI, _("Cliquez d'abord sur une catégorie dans la liste."))
            return None
        return self.carnet.categories()[choix[0]]["nom"]

    def _categories_changees(self, choisir=None):
        self.remplir_categories(choisir)
        self.programmer_enregistrement()

    def nouvelle_categorie(self):
        nom = demander_texte(self, _("Nouvelle catégorie"), _("Nom de la nouvelle catégorie :"))
        if nom is None:
            return
        if not self.carnet.ajouter_categorie(nom):
            messagebox.showinfo(NOM_APPLI, _("La catégorie « {nom} » existe déjà.", nom=nom.strip()))
            return
        self._categories_changees(nom.strip())

    def renommer_categorie(self):
        ancien = self._categorie_choisie()
        if ancien is None:
            return
        nouveau = demander_texte(self, _("Renommer la catégorie"), _("Nouveau nom :"), ancien)
        if nouveau is None or nouveau.strip() == ancien:
            return
        if not self.carnet.renommer_categorie(ancien, nouveau):
            messagebox.showinfo(NOM_APPLI, _("La catégorie « {nom} » existe déjà.", nom=nouveau.strip()))
            return
        self._categories_changees(nouveau.strip())

    def couleur_categorie(self):
        nom = self._categorie_choisie()
        if nom is None:
            return
        couleur = choisir_couleur(self, nom)
        if couleur is None:
            return
        for c in self.carnet.categories():
            if c["nom"] == nom:
                c["couleur"] = couleur
        self._categories_changees(nom)

    def supprimer_categorie(self):
        nom = self._categorie_choisie()
        if nom is None:
            return
        n = self.carnet.nb_fiches_categorie(nom)
        texte = _("Supprimer la catégorie « {nom} » ?", nom=nom)
        if n:
            texte += "\n\n" + n_(n, "{n} fiche n'aura plus de catégorie (la fiche elle-même n'est pas supprimée).",
                                 "{n} fiches n'auront plus de catégorie (les fiches elles-mêmes ne sont pas supprimées).")
        if not messagebox.askyesno(_("Supprimer la catégorie ?"), texte, icon="warning", default="no"):
            return
        self.carnet.supprimer_categorie(nom)
        self._categories_changees()

    def choisir_langue_interface(self, code):
        if code == langue_actuelle():
            return
        choisir_langue(code)
        self.carnet.reglages["langue"] = code
        self._reconstruire()
        self.programmer_enregistrement()  # the .txt copies are rewritten in the new language

    def choisir_theme(self, cle):
        if cle == self.carnet.reglages.get("theme", "clair"):
            return
        self.carnet.reglages["theme"] = cle
        appliquer_theme_couleurs(cle)
        self._reconstruire()
        self.programmer_enregistrement()

    def _reconstruire(self):
        """Redraw the whole window (after a theme change)."""
        page = self.page
        for w in self.racine.winfo_children():
            w.destroy()
        self.racine.configure(bg=FOND)
        self._style()
        self._construire()
        self.appliquer_taille(self.carnet.reglages.get("taille_texte", 1), enregistrer=False)
        self._afficher_dossier()
        self.afficher_page(page)

    # --------------------------------------------------------- documents page
    def _page_documents(self):
        p = self.page_documents = tk.Frame(self.centre, bg=FOND, padx=16, pady=12)

        haut = tk.Frame(p, bg=FOND)
        haut.pack(fill="x", pady=(0, 8))
        self.etiquette_dossier = tk.Label(haut, text="", font=self.f_base, bg=FOND,
                                          fg=ENCRE, anchor="w", justify="left")
        self.etiquette_dossier.pack(fill="x")
        self.zone_boutons_docs = tk.Frame(p, bg=FOND)
        self.zone_boutons_docs.pack(fill="x", pady=(0, 4))
        boutons_docs = [
            self.bouton(self.zone_boutons_docs, _("↻  Synchroniser maintenant"),
                        self.synchroniser_maintenant, "vert"),
            self.bouton(self.zone_boutons_docs, _("Choisir le dossier…"), self.choisir_dossier),
            self.bouton(self.zone_boutons_docs, _("Importer des fichiers…"),
                        self.choisir_fichiers_a_importer),
        ]
        self.zone_boutons_docs.bind("<Configure>", lambda e: self._placer_en_lignes(
            self.zone_boutons_docs, boutons_docs, ecart=4))
        self.var_synchro = tk.BooleanVar(value=bool(self.carnet.reglages.get("synchro_auto", True)))
        tk.Checkbutton(p, text=_("Ranger tout seul les documents de ce dossier "
                               "(nouveaux et modifiés), à chaque ouverture et toutes les minutes"),
                       variable=self.var_synchro, command=self._synchro_auto_changee,
                       font=self.f_petit, bg=FOND, fg=ENCRE, activebackground=FOND,
                       activeforeground=ENCRE, selectcolor=BLANC, anchor="w",
                       justify="left").pack(fill="x", pady=(0, 8))

        filtres = tk.Frame(p, bg=FOND)
        filtres.pack(fill="x", pady=(0, 8))
        tk.Label(filtres, text=_("Montrer :"), font=self.f_gras, bg=FOND, fg=GRIS).pack(
            side="left", anchor="n", pady=(8, 0))
        zone_filtres = tk.Frame(filtres, bg=FOND)
        zone_filtres.pack(side="left", fill="x", expand=True, padx=(4, 0))
        # By default: only what is left to file (the rest is already in the book)
        self.filtre_genre = getattr(self, "filtre_genre", "a_ranger")
        self.boutons_filtre = {}
        for genre, texte in (("a_ranger", _("À ranger")), ("tous", _("Tout")),
                             ("compte", _("Mots de passe")), ("contact", _("Contacts")),
                             ("autre", _("Non reconnus"))):
            self.boutons_filtre[genre] = self.bouton(zone_filtres, texte,
                                                     lambda g=genre: self.choisir_filtre(g))
        zone_filtres.bind("<Configure>", lambda e: self._placer_en_lignes(
            zone_filtres, list(self.boutons_filtre.values()), ecart=4))

        corps = tk.Frame(p, bg=FOND)
        corps.pack(fill="both", expand=True)

        gauche = tk.Frame(corps, bg=FOND)
        gauche.pack(side="left", fill="y", padx=(0, 16))
        tk.Label(gauche, text=_("Chercher dans les documents"), font=self.f_gras,
                 bg=FOND, fg=ENCRE, anchor="w").pack(fill="x")
        self.var_recherche_docs = tk.StringVar()
        self.var_recherche_docs.trace_add("write", lambda *a: self._recherche_docs_changee())
        self.champ_texte(gauche, self.var_recherche_docs).pack(fill="x", ipady=4, pady=(2, 6))
        self.etiquette_compte_docs = tk.Label(gauche, text="", font=self.f_petit,
                                              bg=FOND, fg=GRIS, anchor="w", justify="left")
        self.etiquette_compte_docs.pack(fill="x")
        cadre_liste = tk.Frame(gauche, bg=FOND)
        cadre_liste.pack(fill="both", expand=True, pady=6)
        self.liste_docs = tk.Listbox(
            cadre_liste, font=self.f_base, width=32, activestyle="none",
            bg=BLANC, fg=ENCRE, selectbackground=BLEU, selectforeground=SUR_ACCENT,
            relief="solid", bd=1, highlightthickness=0, exportselection=False)
        barre = ttk.Scrollbar(cadre_liste, orient="vertical", command=self.liste_docs.yview)
        self.liste_docs.configure(yscrollcommand=barre.set)
        self.liste_docs.pack(side="left", fill="both", expand=True)
        barre.pack(side="right", fill="y")
        self.liste_docs.bind("<<ListboxSelect>>", lambda e: self._document_choisi())

        droite = tk.Frame(corps, bg=BLANC, padx=22, pady=16,
                          highlightthickness=2, highlightbackground=BORDURE)
        droite.pack(side="left", fill="both", expand=True)
        self.titre_doc = tk.Label(droite, text=_("Choisissez un document dans la liste."),
                                  font=self.f_titre, bg=BLANC, fg=ENCRE, anchor="w",
                                  justify="left")
        self.titre_doc.pack(fill="x")
        self.genre_doc = tk.Label(droite, text=_("Ce document n'est jamais modifié par le carnet."),
                                  font=self.f_petit, bg=BLANC, fg=GRIS, anchor="w")
        self.genre_doc.pack(fill="x", pady=(2, 8))
        boutons = tk.Frame(droite, bg=BLANC)
        boutons.pack(side="bottom", fill="x", pady=(10, 0))
        self.bouton_fiche_doc = self.bouton(boutons, _("＋  Créer une fiche avec ce document"),
                                            self.fiche_depuis_document, "bleu")
        self.bouton_fiche_doc.pack(side="left")
        self.bouton(boutons, _("Ouvrir dans Word"), self.ouvrir_document).pack(side="left", padx=10)

        # "What the book understood": the document reformatted, field by field
        self.cadre_compris = tk.Frame(droite, bg=JAUNE_FOND, padx=14, pady=10,
                                      highlightthickness=2, highlightbackground=JAUNE_BORD)
        self.cadre_compris.pack(fill="x", pady=(0, 10))
        tk.Label(droite, text=_("Texte du document :"), font=self.f_petit, bg=BLANC, fg=GRIS,
                 anchor="w").pack(fill="x")

        cadre_texte = tk.Frame(droite, bg=BLANC)
        cadre_texte.pack(fill="both", expand=True)
        self.texte_doc = tk.Text(cadre_texte, font=self.f_base, wrap="word", bg=FOND_TEXTE,
                                 fg=ENCRE, relief="solid", bd=1, padx=12, pady=10,
                                 highlightthickness=0, state="disabled")
        barre_t = ttk.Scrollbar(cadre_texte, orient="vertical", command=self.texte_doc.yview)
        self.texte_doc.configure(yscrollcommand=barre_t.set)
        self.texte_doc.pack(side="left", fill="both", expand=True)
        barre_t.pack(side="right", fill="y")
        self.texte_doc.tag_configure("trouve", background="#FFE08A", foreground=TEXTE_SUR_PASTEL)

    # ------------------------------------------------------------ navigation
    def afficher_page(self, page):
        self.page = page
        self.page_fiches.pack_forget()
        self.page_documents.pack_forget()
        self.page_reglages.pack_forget()
        # The letter bar is not used in the settings
        if page == "reglages":
            self.barre_lettres.pack_forget()
            self.sep_lettres.pack_forget()
        elif not self.barre_lettres.winfo_ismapped():
            self.barre_lettres.pack(fill="x", before=self.centre)
            self.sep_lettres.pack(fill="x", before=self.centre)
        if page == "documents":
            self.page_documents.pack(fill="both", expand=True)
        elif page == "reglages":
            self.page_reglages.pack(fill="both", expand=True)
        else:
            self.page_fiches.pack(fill="both", expand=True)
            contact = page == "contact"
            self.titre_recherche.configure(text=_("Chercher un contact") if contact
                                           else _("Chercher une fiche"))
            self.bouton_nouvelle.configure(text=_("＋  Nouveau contact") if contact
                                           else _("＋  Nouvelle fiche"))
            self.aucune_fiche.configure(
                text=(_("Aucun contact n'est choisi.\n\n") if contact else
                      _("Aucune fiche n'est choisie.\n\n"))
                + _("• Cliquez sur un nom dans la liste à gauche,\n")
                + (_("• ou sur « Nouveau contact » pour en créer un.") if contact else
                   _("• ou sur « Nouvelle fiche » pour en créer une."))
                + _("\n\nAstuce : glissez des fichiers .docx ou .txt (ou tout un dossier)\n"
                  "depuis l'Explorateur sur cette fenêtre pour les ranger d'un coup."))
            if self.var_recherche.get():
                self.var_recherche.set("")
            if self.var_filtre_cat.get() != toutes_categories():
                self.var_filtre_cat.set(toutes_categories())
        for nom, b in self.onglets.items():
            actif = nom == page
            b.configure(bg=BLEU if actif else BLANC, fg=SUR_ACCENT if actif else ENCRE,
                        activebackground=BLEU_FONCE if actif else BLEU_CLAIR,
                        activeforeground=SUR_ACCENT if actif else ENCRE)
        self.lettre = "Tout"
        self.rafraichir()

    def rafraichir(self):
        if self.page == "documents":
            self.remplir_liste_docs()
        elif self.page == "reglages":
            self.remplir_categories()
            self._afficher_dossier_txt()
        else:
            self.remplir_liste_fiches()

    def choisir_lettre(self, lettre):
        # A letter clears the search, so the two don't mix.
        var = self.var_recherche_docs if self.page == "documents" else self.var_recherche
        if var.get():
            var.set("")
        self.lettre = lettre
        self.rafraichir()

    def _colorer_lettres(self, lettres_presentes):
        for lettre, b in self.boutons_lettres.items():
            actif = lettre == self.lettre
            present = lettre == "Tout" or lettre in lettres_presentes
            if actif:
                b.configure(bg=BLEU, fg=SUR_ACCENT, activebackground=BLEU_FONCE,
                            activeforeground=SUR_ACCENT, state="normal", cursor="hand2")
            elif present:
                b.configure(bg=BLANC, fg=ENCRE, activebackground=BLEU_CLAIR,
                            activeforeground=ENCRE, state="normal", cursor="hand2")
            else:
                b.configure(bg=BARRE, fg=LETTRE_ETEINTE, state="disabled",
                            disabledforeground=LETTRE_ETEINTE, cursor="arrow")

    # --------------------------------------------------------------- text size
    def appliquer_taille(self, niveau, enregistrer=True):
        niveau = max(0, min(len(TAILLES) - 1, int(niveau)))
        t = TAILLES[niveau]
        self.f_base.configure(size=t)
        self.f_gras.configure(size=t)
        self.f_petit.configure(size=max(t - 2, 11))
        self.f_titre.configure(size=t + 6)
        self.f_mdp.configure(size=t + 6)
        self.f_lettre.configure(size=t - 1)
        for i, b in enumerate(self.boutons_taille):
            actif = i == niveau
            b.configure(bg=BLEU if actif else BLANC, fg=SUR_ACCENT if actif else ENCRE,
                        activebackground=BLEU_FONCE if actif else BLEU_CLAIR,
                        activeforeground=SUR_ACCENT if actif else ENCRE)
        self.racine.after(20, self._placer_lettres)
        self.racine.after(20, lambda: self._placer_en_lignes(
            self.zone_onglets, list(self.onglets.values()), ecart=6))
        if enregistrer and self.carnet.reglages.get("taille_texte") != niveau:
            self.carnet.reglages["taille_texte"] = niveau
            self.programmer_enregistrement()

    # -------------------------------------------------------------- card list
    def _recherche_fiches_changee(self):
        if self.var_recherche.get():
            self.lettre = "Tout"
        if self.page in ("compte", "contact"):
            self.remplir_liste_fiches()

    def remplir_liste_fiches(self):
        genre = self.page
        recherche = normaliser(self.var_recherche.get().strip())
        toutes = sorted((f for f in self.carnet.fiches if f.get("type", "compte") == genre),
                        key=lambda f: cle_tri(f["nom"]))
        trouvees = [f for f in toutes if fiche_correspond(f, recherche)]
        noms_cat = self.carnet.noms_categories()
        self.choix_filtre_cat.configure(values=[toutes_categories()] + noms_cat + [sans_categorie()])
        filtre = self.var_filtre_cat.get()
        if filtre not in [toutes_categories(), sans_categorie()] + noms_cat:
            filtre = toutes_categories()
            self.var_filtre_cat.set(filtre)
        if filtre == sans_categorie():
            trouvees = [f for f in trouvees if not f.get("categorie")]
        elif filtre != toutes_categories():
            trouvees = [f for f in trouvees if f.get("categorie") == filtre]
        self._colorer_lettres({premiere_lettre(f["nom"]) for f in trouvees})
        if self.lettre != "Tout":
            trouvees = [f for f in trouvees if premiere_lettre(f["nom"]) == self.lettre]

        self.liste_fiches.delete(0, "end")
        self.ids_affiches = []
        for i, fiche in enumerate(trouvees):
            self.liste_fiches.insert("end", "  " + (fiche["nom"] or _("Sans nom")))
            self._colorer_ligne(i, fiche)
            self.ids_affiches.append(fiche["id"])
        if self.id_courant in self.ids_affiches:
            i = self.ids_affiches.index(self.id_courant)
            self.liste_fiches.selection_set(i)
            self.liste_fiches.see(i)

        n = len(trouvees)
        if genre == "contact":
            texte = n_(n, "{n} contact", "{n} contacts")
            if recherche:
                texte = n_(n, "{n} contact trouvé", "{n} contacts trouvés")
        else:
            texte = n_(n, "{n} fiche", "{n} fiches")
            if recherche:
                texte = n_(n, "{n} fiche trouvée", "{n} fiches trouvées")
        if not recherche:
            texte += _(", de A à Z") if self.lettre == "Tout" else _(" à la lettre {lettre}", lettre=self.lettre)
        if filtre != toutes_categories():
            texte += f" — {filtre}"
        self.etiquette_compte.configure(text=texte)
        self.montrer_fiche(self.carnet.trouver(self.id_courant))

    def _fiche_choisie(self):
        choix = self.liste_fiches.curselection()
        if not choix:
            return
        self.id_courant = self.ids_affiches[choix[0]]
        self.montrer_fiche(self.carnet.trouver(self.id_courant))

    def montrer_fiche(self, fiche):
        if fiche is None or fiche.get("type", "compte") != self.page:
            self.zone_formulaire.pack_forget()
            self.aucune_fiche.pack(anchor="nw")
            return
        self.aucune_fiche.pack_forget()
        self.zone_formulaire.pack(fill="both", expand=True)
        self._construire_formulaire(fiche)

    def creer_fiche(self):
        genre = self.page if self.page in ("compte", "contact") else "compte"
        fiche = self.carnet.nouvelle_fiche(type=genre)
        self.id_courant = fiche["id"]
        if self.var_recherche.get():
            self.var_recherche.set("")
        self.lettre = "Tout"
        self.remplir_liste_fiches()
        self.programmer_enregistrement()
        # Offer to type the name right away.
        if self.champ_nom is not None:
            self.champ_nom.focus_set()
            self.champ_nom.select_range(0, "end")

    def supprimer_fiche(self):
        fiche = self.carnet.trouver(self.id_courant)
        if fiche is None:
            return
        if fiche.get("type") == "contact":
            question = _("Voulez-vous vraiment supprimer le contact « {nom} » ?", nom=fiche["nom"])
        else:
            question = _("Voulez-vous vraiment supprimer la fiche « {nom} » ?", nom=fiche["nom"])
        if not messagebox.askyesno(
                _("Supprimer ?"),
                question + "\n\n" + _("Une copie reste dans les sauvegardes du jour."),
                icon="warning", default="no"):
            return
        self.carnet.supprimer(fiche["id"])
        self.id_courant = None
        self.remplir_liste_fiches()
        self.programmer_enregistrement()

    # ------------------------------------------------------------ small helpers
    def copier(self, texte, bouton=None):
        if not texte:
            return
        self.racine.clipboard_clear()
        self.racine.clipboard_append(texte)
        self.racine.update()
        if bouton is not None:
            ancien = bouton.cget("text")
            if not ancien.startswith("✔"):
                bouton.configure(text=_("✔ Copié"))
                self.racine.after(1500, lambda: bouton.configure(text=ancien))

    def ouvrir_site(self):
        adresse = self.vars_fiche["site"].get().strip() if "site" in self.vars_fiche else ""
        if not adresse:
            messagebox.showinfo(_("Site internet"), _("Aucune adresse de site n'est notée sur cette fiche."))
            return
        if not re.match(r"^https?://", adresse, re.IGNORECASE):
            adresse = "https://" + adresse
        webbrowser.open(adresse)

    # ---------------------------------------------------------------- generator
    def ouvrir_generateur(self):
        fiche = self.carnet.trouver(self.id_courant)
        if fiche is None:
            return
        if fiche.get("mdp") and not messagebox.askyesno(
                _("Changer le mot de passe ?"),
                _("Voulez-vous vraiment changer le mot de passe de « {nom} » ?\n\n"
                  "Attention : cela change seulement le carnet. Il faudra aussi le changer "
                  "sur le site lui-même, sinon vous ne pourrez plus vous connecter.\n\n"
                  "(L'ancien mot de passe sera gardé dans les notes.)", nom=fiche.get("nom", "")),
                icon="warning", default="no"):
            return
        FenetreGenerateur(self)

    def remplacer_mot_de_passe(self, nouveau):
        fiche = self.carnet.trouver(self.id_courant)
        if fiche is None:
            return
        ancien = fiche.get("mdp", "")
        if ancien and ancien != nouveau:
            date = datetime.now().strftime(_("%d/%m/%Y"))
            note = _("Ancien mot de passe (remplacé le {date}) : {ancien}", date=date, ancien=ancien)
            notes = fiche.get("notes", "").rstrip()
            fiche["notes"] = (notes + "\n" + note).strip()
        fiche["mdp"] = nouveau
        fiche["modifie_le"] = datetime.now().isoformat(timespec="seconds")
        fiche["modifiee_a_la_main"] = True   # synchronization will not overwrite it
        self.montrer_fiche(fiche)
        self.programmer_enregistrement()

    # --------------------------------------------------------------------- save
    def programmer_enregistrement(self):
        self.etiquette_etat.configure(text=_("✎ Modification en cours…"), fg=GRIS)
        if self._minuterie is not None:
            self.racine.after_cancel(self._minuterie)
        self._minuterie = self.racine.after(800, self.enregistrer)

    def enregistrer(self):
        self._minuterie = None
        copie_ok = self.carnet.synchroniser_txt()  # the .txt files first (updates their list)
        try:
            self.carnet.enregistrer()
        except Exception as exc:
            self.etiquette_etat.configure(text=_("⚠ Impossible d'enregistrer !"), fg=ROUGE)
            messagebox.showerror(
                _("Problème d'enregistrement"),
                _("Le carnet n'a pas pu être enregistré.\n\n") + str(exc))
            return False
        heure = datetime.now().strftime("%H:%M")
        if copie_ok:
            self.etiquette_etat.configure(text=_("✔ Tout est enregistré (à {heure})", heure=heure), fg=VERT_TEXTE)
            self._alerte_txt_montree = False
        else:
            # The book is saved; only the .txt copy failed (USB stick removed…).
            self.etiquette_etat.configure(
                text=_("✔ Enregistré (à {heure}) — ⚠ copie .txt impossible", heure=heure), fg=ROUGE)
            if not self._alerte_txt_montree:
                self._alerte_txt_montree = True
                messagebox.showwarning(
                    NOM_APPLI, _("Le carnet est bien enregistré, mais la copie des fiches en "
                               ".txt n'a pas pu être faite.\n\nLe dossier est peut-être "
                               "débranché (clé USB, disque réseau).\n\n") + self.carnet.message_txt)
        return True

    def enregistrer_maintenant(self):
        if self._minuterie is not None:
            self.racine.after_cancel(self._minuterie)
            self._minuterie = None
        if self.enregistrer():
            try:
                self.carnet.sauvegarde_du_jour()
            except OSError:
                pass

    def quitter(self):
        if self._minuterie is not None:
            self.racine.after_cancel(self._minuterie)
        if not self.enregistrer():
            if not messagebox.askyesno(_("Fermer quand même ?"),
                                       _("Le carnet n'a pas pu être enregistré.\n"
                                       "Fermer quand même ?"), default="no"):
                return
        self.racine.destroy()

    # ---------------------------------------------------------------- documents
    def _apres_ouverture(self):
        if self.carnet.message_recuperation:
            messagebox.showwarning(NOM_APPLI, self.carnet.message_recuperation)
        if FICHIER_CARNET.exists():
            self.etiquette_etat.configure(text=_("✔ Tout est enregistré"), fg=VERT_TEXTE)
        dossier = self.carnet.reglages.get("dossier_documents", "")
        self._afficher_dossier()
        if self.carnet.fiches:
            self.enregistrer()  # create any missing .txt files
        if dossier and os.path.isdir(dossier):
            self.lancer_lecture()

    def _afficher_dossier_txt(self):
        dossier = self.carnet.reglages.get("dossier_txt", "")
        self.etiquette_txt.configure(
            text=(_("Copie de chaque fiche en .txt, mise à jour toute seule, dans :\n") + dossier)
            if dossier else _("Copie des fiches en .txt : désactivée."))

    def choisir_dossier_txt(self):
        dossier = filedialog.askdirectory(
            title=_("Dans quel dossier ranger la copie .txt des fiches ?"),
            initialdir=self.carnet.reglages.get("dossier_txt") or str(DOSSIER_DONNEES))
        if not dossier:
            return
        dossier = os.path.normpath(dossier)
        docs = self.carnet.reglages.get("dossier_documents", "")
        if docs and os.path.normcase(dossier) == os.path.normcase(os.path.normpath(docs)):
            messagebox.showwarning(
                NOM_APPLI, _("Choisissez un autre dossier que celui des documents d'origine\n"
                           "(par exemple un sous-dossier « Fiches en texte »)."))
            return
        self.carnet.changer_dossier_txt(dossier)
        self._afficher_dossier_txt()
        self.enregistrer()
        messagebox.showinfo(NOM_APPLI, _("La copie .txt des fiches est maintenant dans :\n") + dossier
                            + _("\n\nL'ancien dossier n'a pas été modifié."))

    def ouvrir_fichier_fiche(self, quoi):
        """Open the card's .txt copy, its source document, or the folder (file selected)."""
        fiche = self.carnet.trouver(self.id_courant)
        if fiche is None:
            return
        if quoi == "source":
            chemin = fiche.get("source", "")
        else:
            self.enregistrer()  # the .txt copy must be up to date before opening it
            rel = fiche.get("fichier_txt", "")
            chemin = str(Path(self.carnet.reglages.get("dossier_txt", "")) / rel) if rel else ""
        if not chemin or not os.path.exists(chemin):
            messagebox.showinfo(NOM_APPLI, _("Ce fichier n'existe pas (ou plus) sur l'ordinateur."))
            return
        try:
            if quoi == "dossier":
                montrer_dans_dossier(chemin)
            else:
                ouvrir_avec_systeme(chemin)
        except OSError as exc:
            messagebox.showerror(NOM_APPLI, _("Le fichier n'a pas pu être ouvert.\n\n") + str(exc))

    def ouvrir_dossier_txt(self):
        dossier = self.carnet.reglages.get("dossier_txt", "")
        if not dossier:
            return
        Path(dossier).mkdir(parents=True, exist_ok=True)
        try:
            ouvrir_avec_systeme(dossier)
        except OSError as exc:
            messagebox.showerror(NOM_APPLI, _("Le dossier n'a pas pu être ouvert.\n\n") + str(exc))

    def _afficher_dossier(self):
        self._afficher_dossier_txt()
        dossier = self.carnet.reglages.get("dossier_documents", "")
        if dossier:
            self.etiquette_dossier.configure(text=_("Dossier des documents :\n") + dossier)
        else:
            self.etiquette_dossier.configure(
                text=_("Aucun dossier choisi. Cliquez sur « Choisir le dossier… »."))

    def choisir_dossier(self):
        dossier = filedialog.askdirectory(
            title=_("Où sont rangés vos documents ?"),
            initialdir=self.carnet.reglages.get("dossier_documents") or str(Path.home()))
        if not dossier:
            return
        self.carnet.reglages["dossier_documents"] = os.path.normpath(dossier)
        self.programmer_enregistrement()
        self._afficher_dossier()
        self.lancer_lecture()

    def lancer_lecture(self):
        dossier = self.carnet.reglages.get("dossier_documents", "")
        if not dossier or not os.path.isdir(dossier):
            messagebox.showinfo(NOM_APPLI, _("Choisissez d'abord le dossier où sont rangés vos documents."))
            return
        if self.lecture_en_cours:
            return
        self.lecture_en_cours = True
        self.etiquette_compte_docs.configure(text=_("Lecture des documents…"))
        ancien = self.index

        def travail():
            try:
                resultat = indexer(dossier, ancien,
                                   lambda i, n: self.file_messages.put(("progres", i, n)),
                                   exclure=[self.carnet.reglages.get("dossier_txt", "")])
                try:
                    ecrire_json_sur(FICHIER_INDEX, resultat)
                except OSError:
                    pass
                self.file_messages.put(("fini", resultat))
            except Exception as exc:
                self.file_messages.put(("erreur", str(exc)))

        threading.Thread(target=travail, daemon=True).start()
        self.racine.after(100, self._suivre_lecture)

    def _suivre_lecture(self):
        try:
            while True:
                message = self.file_messages.get_nowait()
                if message[0] == "progres":
                    _type, i, n = message
                    self.etiquette_compte_docs.configure(
                        text=_("Lecture des documents : {i} sur {n}…", i=i, n=n))
                elif message[0] == "fini":
                    self.index = message[1]
                    self.lecture_en_cours = False
                    demande = self._synchro_demandee
                    self._synchro_demandee = False
                    if demande or self.carnet.reglages.get("synchro_auto", True):
                        self._appliquer_synchro(afficher_resume=demande)
                    if self.page == "documents":
                        self.remplir_liste_docs()
                    else:
                        self._compte_docs()
                    return
                elif message[0] == "erreur":
                    self.lecture_en_cours = False
                    self.etiquette_compte_docs.configure(text=_("La lecture a échoué."))
                    messagebox.showerror(NOM_APPLI, _("Les documents n'ont pas pu être lus.\n\n") + message[1])
                    return
        except queue.Empty:
            pass
        self.racine.after(100, self._suivre_lecture)

    # ------------------------------------------------------- synchronization
    def _appliquer_synchro(self, afficher_resume=False):
        documents = self._documents()
        if not documents:
            return
        resume = self.carnet.synchroniser_documents(documents, self._garder_categories)
        total = resume["crees"] + resume["mises_a_jour"] + resume["a_verifier"]
        if total:
            self.enregistrer()
            if self.page in ("compte", "contact"):
                self.remplir_liste_fiches()
        morceaux = []
        if resume["crees"]:
            morceaux.append(n_(resume["crees"], "{n} fiche créée", "{n} fiches créées"))
        if resume["mises_a_jour"]:
            morceaux.append(n_(resume["mises_a_jour"], "{n} mise à jour", "{n} mises à jour"))
        if resume["a_verifier"]:
            morceaux.append(n_(resume["a_verifier"], "{n} à vérifier (⚠ dans les notes)",
                               "{n} à vérifier (⚠ dans les notes)"))
        if morceaux:
            heure = datetime.now().strftime("%H:%M")
            self.etiquette_synchro.configure(
                text=_("↻ Documents synchronisés à {heure} : ", heure=heure) + ", ".join(morceaux))
        if afficher_resume:
            messagebox.showinfo(
                _("Synchronisation"),
                (_("Depuis les documents :\n\n   • ") + "\n   • ".join(morceaux)) if morceaux
                else _("Tout est déjà à jour : aucune fiche à créer ou à modifier."))

    def synchroniser_maintenant(self):
        dossier = self.carnet.reglages.get("dossier_documents", "")
        if not dossier or not os.path.isdir(dossier):
            messagebox.showinfo(NOM_APPLI, _("Choisissez d'abord le dossier où sont rangés vos documents."))
            return
        self._synchro_demandee = True
        self.lancer_lecture()

    def _synchro_auto_changee(self):
        self.carnet.reglages["synchro_auto"] = bool(self.var_synchro.get())
        self.programmer_enregistrement()
        if self.var_synchro.get():
            self.synchroniser_maintenant()

    def _synchro_periodique(self):
        """Every minute: rescan the folder (only changed files are read again)."""
        dossier = self.carnet.reglages.get("dossier_documents", "")
        if (self.carnet.reglages.get("synchro_auto", True) and dossier
                and os.path.isdir(dossier) and not self.lecture_en_cours):
            self.lancer_lecture()
        self.racine.after(60000, self._synchro_periodique)

    def _documents(self):
        return self.index.get("documents", {}) if self.index.get(
            "dossier") == self.carnet.reglages.get("dossier_documents") else {}

    def _compte_docs(self):
        n = len(self._documents())
        self.etiquette_compte_docs.configure(text=n_(n, "{n} document", "{n} documents"))

    def _recherche_docs_changee(self):
        if self.var_recherche_docs.get():
            self.lettre = "Tout"
        if self._minuterie_recherche is not None:
            self.racine.after_cancel(self._minuterie_recherche)
        self._minuterie_recherche = self.racine.after(250, self.remplir_liste_docs)

    def choisir_filtre(self, genre):
        self.filtre_genre = genre
        self.remplir_liste_docs()

    def remplir_liste_docs(self):
        self._minuterie_recherche = None
        for genre, b in self.boutons_filtre.items():
            actif = genre == self.filtre_genre
            b.configure(bg=BLEU if actif else BLANC, fg=SUR_ACCENT if actif else ENCRE,
                        activebackground=BLEU_FONCE if actif else BLEU_CLAIR,
                        activeforeground=SUR_ACCENT if actif else ENCRE)
        documents = self._documents()
        recherche = normaliser(self.var_recherche_docs.get().strip())
        elements = sorted(documents.items(), key=lambda kv: cle_tri(kv[1]["nom"]))
        deja = self.carnet.sources_connues()
        tous_les_documents = len(elements)
        if self.filtre_genre == "a_ranger":
            elements = [(c, d) for c, d in elements if os.path.normcase(c) not in deja]
        elif self.filtre_genre != "tous":
            elements = [(c, d) for c, d in elements if d.get("genre", "autre") == self.filtre_genre]
        if recherche:
            elements = [(c, d) for c, d in elements if recherche in self._texte_cherchable(c, d)]
        self._colorer_lettres({premiere_lettre(d["nom"]) for _c, d in elements})
        if self.lettre != "Tout":
            elements = [(c, d) for c, d in elements if premiere_lettre(d["nom"]) == self.lettre]

        self.liste_docs.delete(0, "end")
        self.chemins_affiches = []
        for chemin, doc in elements:
            genre = doc.get("genre", "autre")
            marque = "✔ " if os.path.normcase(chemin) in deja else "   "
            self.liste_docs.insert("end", f" {marque}{_(ETIQUETTES_GENRE[genre])} · {doc['nom']}")
            self.liste_docs.itemconfig("end", foreground=couleur_genre(genre))
            self.chemins_affiches.append(chemin)

        n = len(elements)
        if self.lecture_en_cours:
            return
        if not self.carnet.reglages.get("dossier_documents"):
            texte = _("Aucun dossier choisi.")
        else:
            if self.filtre_genre == "a_ranger":
                texte = (n_(n, "{n} document à ranger (sur {total})", "{n} documents à ranger (sur {total})",
                            total=tous_les_documents) if n else
                         _("✔ Tout est rangé ({total} documents).\nCliquez sur « Tout » pour les revoir.",
                           total=tous_les_documents))
            elif recherche:
                texte = n_(n, "{n} document trouvé", "{n} documents trouvés")
            else:
                texte = n_(n, "{n} document", "{n} documents")
            if not recherche and self.lettre != "Tout" and n:
                texte += _(" à la lettre {lettre}", lettre=self.lettre)
            texte += "\n" + _("✔ = déjà rangé dans le carnet")
            anciens = self.index.get("anciens_doc", 0)
            if anciens:
                texte += "\n" + n_(anciens, "⚠ {n} ancien fichier .doc non lu\n   (à enregistrer en .docx avec Word)",
                                   "⚠ {n} anciens fichiers .doc non lus\n   (à enregistrer en .docx avec Word)")
        self.etiquette_compte_docs.configure(text=texte)

    def _texte_cherchable(self, chemin, doc):
        """Name + text without accents, cached for fast searching."""
        cle = (chemin, doc.get("mtime"))
        if cle not in self._cache_recherche:
            self._cache_recherche[cle] = normaliser(doc["nom"] + "\n" + doc.get("texte", ""))
        return self._cache_recherche[cle]

    def _document_courant(self):
        choix = self.liste_docs.curselection()
        if not choix:
            return None, None
        chemin = self.chemins_affiches[choix[0]]
        return chemin, self._documents().get(chemin)

    def _document_choisi(self):
        chemin, doc = self._document_courant()
        if doc is None:
            return
        self.titre_doc.configure(text=doc["nom"])
        genre = doc.get("genre", "autre")
        self.genre_doc.configure(
            text=_("Reconnu comme : {genre}   —   ce document n'est jamais modifié.",
                   genre=_(NOMS_GENRE[genre])),
            fg=couleur_genre(genre))
        self._montrer_compris(chemin, doc)
        self.texte_doc.configure(state="normal")
        self.texte_doc.delete("1.0", "end")
        self.texte_doc.insert("1.0", doc["erreur"] or doc["texte"] or _("(Document vide)"))
        recherche = self.var_recherche_docs.get().strip()
        if recherche:
            debut = "1.0"
            while True:
                pos = self.texte_doc.search(recherche, debut, stopindex="end", nocase=True)
                if not pos:
                    break
                fin = f"{pos}+{len(recherche)}c"
                self.texte_doc.tag_add("trouve", pos, fin)
                debut = fin
            premier = self.texte_doc.tag_nextrange("trouve", "1.0")
            if premier:
                self.texte_doc.see(premier[0])
        self.texte_doc.configure(state="disabled")

    def _fiches_du_document(self, chemin):
        return [f for f in self.carnet.fiches
                if os.path.normcase(f.get("source", "")) == os.path.normcase(chemin)]

    def _montrer_compris(self, chemin, doc):
        """Show the reformatted document (or the card it was already filed into)."""
        for w in self.cadre_compris.winfo_children():
            w.destroy()
        rangees = self._fiches_du_document(chemin)
        genre = doc.get("genre", "autre")
        if rangees:
            fiches, titre = rangees, _("Déjà rangé dans le carnet :")
            self.bouton_fiche_doc.configure(text=_("→  Voir la fiche"), command=lambda: self.voir_fiche(rangees[0]))
        elif genre in ("compte", "contact") and not doc.get("erreur"):
            fiches = self._garder_categories(deviner(doc["nom"], doc["texte"], genre))
            titre = _("Ce que le carnet a compris :")
            self.bouton_fiche_doc.configure(text=_("＋  Créer une fiche avec ce document"),
                                            command=self.fiche_depuis_document)
        else:
            self.bouton_fiche_doc.configure(text=_("＋  Créer une fiche avec ce document"),
                                            command=self.fiche_depuis_document)
            tk.Label(self.cadre_compris, text=_("Le carnet n'a pas reconnu ce document. Vous pouvez "
                     "quand même créer une fiche : il vous demandera s'il s'agit d'un mot de passe "
                     "ou d'un contact."), font=self.f_petit, bg=JAUNE_FOND, fg=JAUNE_TEXTE,
                     anchor="w", justify="left", wraplength=700).pack(fill="x")
            return
        tk.Label(self.cadre_compris, text=titre, font=self.f_gras, bg=JAUNE_FOND,
                 fg=JAUNE_TEXTE, anchor="w").pack(fill="x")
        grille = tk.Frame(self.cadre_compris, bg=JAUNE_FOND)
        grille.pack(fill="x", pady=(4, 0))
        r = 0
        for fiche in fiches[:6]:
            lignes = [(_("Nom"), fiche.get("nom", ""))]
            for champ in ORDRE_CHAMPS.get(fiche.get("type", "compte"), []):
                valeur = fiche.get(champ, "")
                if valeur and champ != "notes":
                    lignes.append((_(LIBELLES_CHAMPS[champ]), valeur.replace("\n", ", ")))
            lignes += [(p.get("libelle", ""), p.get("valeur", "")) for p in fiche.get("perso", [])]
            if fiche.get("notes"):
                lignes.append((_("Notes"), fiche["notes"].replace("\n", " · ")[:120]))
            for libelle, valeur in lignes:
                tk.Label(grille, text=deux_points(libelle), font=self.f_petit, bg=JAUNE_FOND,
                         fg=JAUNE_TEXTE, anchor="w").grid(row=r, column=0, sticky="nw", padx=(0, 12))
                tk.Label(grille, text=valeur, font=self.f_mdp if libelle == _("Mot de passe")
                         else self.f_gras, bg=JAUNE_FOND, fg=ENCRE, anchor="w", justify="left",
                         wraplength=650).grid(row=r, column=1, sticky="w")
                r += 1
            r += 1
        if len(fiches) > 6:
            tk.Label(grille, text=_("… et {n} autres contacts", n=len(fiches) - 6), font=self.f_petit,
                     bg=JAUNE_FOND, fg=JAUNE_TEXTE).grid(row=r, column=0, columnspan=2, sticky="w")

    def voir_fiche(self, fiche):
        """Switch to the card's tab and select it."""
        self.id_courant = fiche["id"]
        self.afficher_page(fiche.get("type", "compte"))

    def ouvrir_document(self):
        chemin, doc = self._document_courant()
        if not chemin:
            messagebox.showinfo(NOM_APPLI, _("Choisissez d'abord un document dans la liste."))
            return
        try:
            ouvrir_avec_systeme(chemin)
        except OSError as exc:
            messagebox.showerror(NOM_APPLI, _("Le document n'a pas pu être ouvert.\n\n") + str(exc))

    def fiche_depuis_document(self):
        chemin, doc = self._document_courant()
        if doc is None:
            messagebox.showinfo(NOM_APPLI, _("Choisissez d'abord un document dans la liste."))
            return
        if os.path.normcase(chemin) in self.carnet.sources_connues():
            if not messagebox.askyesno(
                    NOM_APPLI, _("« {nom} » est déjà rangé dans le carnet.\n"
                                 "En créer une autre fiche quand même ?", nom=doc["nom"]), default="no"):
                return
        genre = doc.get("genre", "autre")
        if genre == "autre":
            genre = demander_genre(self, doc["nom"])
            if genre is None:
                return
        propositions = self._garder_categories(deviner(doc["nom"], doc["texte"], genre))
        self.carnet.reprendre_source(chemin)
        maintenant = datetime.now().isoformat(timespec="seconds")
        fiches = [self.carnet.nouvelle_fiche(source=chemin, source_mtime=doc.get("mtime"),
                                             importe_le=maintenant, **champs)
                  for champs in propositions]
        self.id_courant = fiches[0]["id"]
        self.programmer_enregistrement()
        self.afficher_page(genre)
        if len(fiches) > 1:
            texte = _("Ce document contenait {n} contacts : ils ont tous été créés.", n=len(fiches))
        else:
            texte = _("La fiche a été remplie à partir du document.")
        texte += "\n\n" + _("Vérifiez que chaque information est au bon endroit.")
        messagebox.showinfo(_("Fiche créée"), texte)

    # -------------------------------------------------- drag and drop / import
    def _activer_glisser_deposer(self):
        """Accept files dragged from Windows Explorer onto the window."""
        self.depots = queue.Queue()
        if not sys.platform.startswith("win"):
            return
        try:
            import ctypes
            from ctypes import wintypes
            user32, shell32 = ctypes.windll.user32, ctypes.windll.shell32
            WM_DROPFILES, GWLP_WNDPROC = 0x0233, -4
            LRESULT = ctypes.c_ssize_t
            WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT,
                                         wintypes.WPARAM, wintypes.LPARAM)
            definir = (user32.SetWindowLongPtrW if ctypes.sizeof(ctypes.c_void_p) == 8
                       else user32.SetWindowLongW)
            definir.restype = ctypes.c_void_p
            definir.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_void_p]
            user32.CallWindowProcW.restype = LRESULT
            user32.CallWindowProcW.argtypes = [ctypes.c_void_p, wintypes.HWND, wintypes.UINT,
                                               wintypes.WPARAM, wintypes.LPARAM]
            shell32.DragQueryFileW.restype = wintypes.UINT
            shell32.DragQueryFileW.argtypes = [ctypes.c_void_p, wintypes.UINT,
                                               wintypes.LPWSTR, wintypes.UINT]
            shell32.DragFinish.argtypes = [ctypes.c_void_p]
            shell32.DragAcceptFiles.argtypes = [wintypes.HWND, wintypes.BOOL]

            hwnd = int(self.racine.wm_frame(), 16)
            ancienne = {}

            def procedure(h, message, wparam, lparam):
                if message == WM_DROPFILES:
                    try:
                        n = shell32.DragQueryFileW(wparam, 0xFFFFFFFF, None, 0)
                        chemins = []
                        for i in range(n):
                            tampon = ctypes.create_unicode_buffer(32768)
                            shell32.DragQueryFileW(wparam, i, tampon, 32768)
                            chemins.append(tampon.value)
                        self.depots.put(chemins)
                    finally:
                        shell32.DragFinish(wparam)
                    return 0
                return user32.CallWindowProcW(ancienne["proc"], h, message, wparam, lparam)

            self._procedure_depot = WNDPROC(procedure)   # kept in memory (important)
            ancienne["proc"] = definir(hwnd, GWLP_WNDPROC,
                                       ctypes.cast(self._procedure_depot, ctypes.c_void_p))
            shell32.DragAcceptFiles(hwnd, True)
        except Exception:
            return  # no drag and drop: the "Import files…" button is still there
        self.racine.after(300, self._surveiller_depots)

    def _surveiller_depots(self):
        try:
            while True:
                self.importer_chemins(self.depots.get_nowait())
        except queue.Empty:
            pass
        self.racine.after(300, self._surveiller_depots)

    def choisir_fichiers_a_importer(self):
        chemins = filedialog.askopenfilenames(
            title=_("Choisissez les documents à ranger (plusieurs à la fois possible)"),
            filetypes=[(_("Documents Word et texte"), "*.docx *.txt"), (_("Tous les fichiers"), "*.*")])
        if chemins:
            self.importer_chemins(list(chemins))

    def importer_chemins(self, chemins):
        """File away files (or whole folders) dragged in or chosen."""
        dossier_txt = self.carnet.reglages.get("dossier_txt", "")
        fichiers, anciens_doc, ignores = [], 0, 0
        for chemin in chemins:
            if os.path.isdir(chemin):
                trouves, anciens = lister_documents(chemin, [dossier_txt])
                fichiers += trouves
                anciens_doc += anciens
            elif os.path.basename(chemin).startswith("~$"):
                continue
            elif chemin.lower().endswith(EXTENSIONS_LUES):
                fichiers.append(chemin)
            elif chemin.lower().endswith(".doc"):
                anciens_doc += 1
            else:
                ignores += 1

        deja = self.carnet.sources_connues()
        a_ranger, non_reconnus, nb_deja = [], [], 0
        for chemin in sorted(set(fichiers), key=lambda c: cle_tri(Path(c).stem)):
            if os.path.normcase(chemin) in deja:
                nb_deja += 1
                continue
            try:
                texte = lire_document(chemin)
            except Exception:
                non_reconnus.append((chemin, ""))
                continue
            genre = classer_document(texte)
            if genre == "autre":
                non_reconnus.append((chemin, texte))
            else:
                a_ranger.append((chemin, self._garder_categories(
                    deviner(Path(chemin).stem, texte, genre))))

        nb_comptes = sum(1 for _c, fs in a_ranger for f in fs if f["type"] == "compte")
        nb_contacts = sum(1 for _c, fs in a_ranger for f in fs if f["type"] == "contact")
        remarques = []
        if nb_deja:
            remarques.append(n_(nb_deja, "{n} document déjà rangé : ignoré.",
                                "{n} documents déjà rangés : ignorés."))
        if anciens_doc:
            remarques.append(n_(anciens_doc, "{n} ancien fichier .doc non lu (à enregistrer en .docx avec Word).",
                                "{n} anciens fichiers .doc non lus (à enregistrer en .docx avec Word)."))
        if ignores:
            remarques.append(n_(ignores, "{n} fichier d'un autre type ignoré.",
                                "{n} fichiers d'un autre type ignorés."))
        if non_reconnus:
            noms = ", ".join(Path(c).stem for c, _t in non_reconnus[:6])
            noms += "…" if len(non_reconnus) > 6 else ""
            remarques.append(n_(len(non_reconnus), "{n} document non reconnu : {noms}",
                                "{n} documents non reconnus : {noms}", noms=noms))

        if not a_ranger and not non_reconnus:
            messagebox.showinfo(NOM_APPLI, _("Rien de nouveau à ranger.\n\n") + "\n".join(remarques))
            return
        if a_ranger and not messagebox.askyesno(
                _("Ranger ces documents ?"),
                _("Le carnet va ranger :") + "\n\n   • "
                + n_(nb_comptes, "{n} mot de passe  →  « Mes mots de passe »",
                     "{n} mots de passe  →  « Mes mots de passe »") + "\n   • "
                + n_(nb_contacts, "{n} contact  →  « Mes contacts »",
                     "{n} contacts  →  « Mes contacts »") + "\n\n"
                + ("\n".join(remarques) + "\n\n" if remarques else "")
                + _("Les documents eux-mêmes ne sont pas modifiés. Continuer ?")):
            return
        forcer = False
        if non_reconnus:
            forcer = messagebox.askyesno(
                _("Documents non reconnus"),
                n_(len(non_reconnus), "{n} document ne ressemble ni à un mot de passe ni à un contact.",
                   "{n} documents ne ressemblent ni à un mot de passe ni à un contact.")
                + "\n\n" + _("Les ranger quand même dans « Mes mots de passe » ?\n"
                               "(leur texte ira dans les Notes de la fiche)"), default="no")
        try:
            self.carnet.enregistrer()
            self.carnet.sauvegarde_du_jour(force=True)
        except OSError:
            pass
        premiere = None
        maintenant = datetime.now().isoformat(timespec="seconds")
        for chemin, propositions in a_ranger:
            for champs in propositions:
                self.carnet.reprendre_source(chemin)
                fiche = self.carnet.nouvelle_fiche(source=chemin, importe_le=maintenant,
                                                   source_mtime=self._mtime(chemin), **champs)
                premiere = premiere or fiche
        if forcer:
            for chemin, texte in non_reconnus:
                champs = self._garder_categories([deviner_fiche(Path(chemin).stem, texte)])[0]
                self.carnet.reprendre_source(chemin)
                fiche = self.carnet.nouvelle_fiche(source=chemin, importe_le=maintenant,
                                                   source_mtime=self._mtime(chemin), **champs)
                premiere = premiere or fiche
        if premiere is None:
            return
        self.enregistrer()
        self.id_courant = premiere["id"]
        total = nb_comptes + nb_contacts + (len(non_reconnus) if forcer else 0)
        self.afficher_page("contact" if nb_contacts > nb_comptes + (len(non_reconnus) if forcer else 0)
                           else "compte")
        messagebox.showinfo(_("C'est rangé !"), n_(total, "{n} fiche créée.", "{n} fiches créées."))

    @staticmethod
    def _mtime(chemin):
        try:
            return os.stat(chemin).st_mtime
        except OSError:
            return None

    def _garder_categories(self, propositions):
        """A guessed category is only kept if it exists in the settings."""
        for champs in propositions:
            if "categorie" in champs:
                champs["categorie"] = self.carnet.categorie_existante(champs["categorie"])
        return propositions

    def importer_tout(self):
        """Former "File everything" button: it is now the synchronization."""
        self.synchroniser_maintenant()


def demander_texte(appli, titre, question, valeur=""):
    """Small window to type some text (in large print). None if cancelled."""
    reponse = {"texte": None}
    f = tk.Toplevel(appli.racine)
    f.title(titre)
    f.configure(bg=BLANC, padx=24, pady=18)
    f.transient(appli.racine)
    f.resizable(False, False)
    tk.Label(f, text=question, font=appli.f_gras, bg=BLANC, fg=ENCRE).pack(anchor="w")
    var = tk.StringVar(value=valeur)
    saisie = appli.champ_texte(f, var)
    saisie.pack(fill="x", ipady=4, pady=(6, 14))

    def valider(_evenement=None):
        if var.get().strip():
            reponse["texte"] = var.get()
            f.destroy()

    saisie.bind("<Return>", valider)
    boutons = tk.Frame(f, bg=BLANC)
    boutons.pack(fill="x")
    appli.bouton(boutons, _("Annuler"), f.destroy).pack(side="right")
    appli.bouton(boutons, _("✔  Valider"), valider, "vert").pack(side="right", padx=10)
    f.grab_set()
    saisie.focus_set()
    saisie.select_range(0, "end")
    appli.racine.wait_window(f)
    return reponse["texte"]


def choisir_couleur(appli, nom):
    """Grid of soft colors (all readable with dark text)."""
    reponse = {"couleur": None}
    f = tk.Toplevel(appli.racine)
    f.title(_("Couleur de la catégorie"))
    f.configure(bg=BLANC, padx=24, pady=18)
    f.transient(appli.racine)
    f.resizable(False, False)
    tk.Label(f, text=_("Couleur pour « {nom} » :", nom=nom), font=appli.f_gras, bg=BLANC,
             fg=ENCRE).pack(anchor="w", pady=(0, 10))
    grille = tk.Frame(f, bg=BLANC)
    grille.pack()

    def choisir(couleur):
        reponse["couleur"] = couleur
        f.destroy()

    for i, (libelle, couleur) in enumerate(PALETTE_CATEGORIES):
        tk.Button(grille, text=_(libelle), font=appli.f_gras, bg=couleur, fg=TEXTE_SUR_PASTEL,
                  activebackground=couleur, activeforeground=TEXTE_SUR_PASTEL, width=10,
                  relief="solid", bd=1, pady=10, cursor="hand2", highlightthickness=0,
                  command=lambda c=couleur: choisir(c)).grid(row=i // 5, column=i % 5,
                                                              padx=4, pady=4)
    appli.bouton(f, _("Annuler"), f.destroy).pack(anchor="e", pady=(12, 0))
    f.grab_set()
    appli.racine.wait_window(f)
    return reponse["couleur"]


def demander_genre(appli, nom):
    """Small window asking: is it a password or a contact?"""
    reponse = {"genre": None}
    f = tk.Toplevel(appli.racine)
    f.title(_("Quel genre de document ?"))
    f.configure(bg=BLANC, padx=24, pady=18)
    f.transient(appli.racine)
    f.resizable(False, False)
    tk.Label(f, text=f"« {nom} »\n\n" + _("Que contient ce document ?"), font=appli.f_gras,
             bg=BLANC, fg=ENCRE, justify="left").pack(anchor="w", pady=(0, 14))

    def choisir(genre):
        reponse["genre"] = genre
        f.destroy()

    boutons = tk.Frame(f, bg=BLANC)
    boutons.pack(fill="x")
    appli.bouton(boutons, _("Un mot de passe"), lambda: choisir("compte"), "bleu").pack(side="left")
    appli.bouton(boutons, _("Un contact"), lambda: choisir("contact"), "bleu").pack(side="left", padx=10)
    appli.bouton(boutons, _("Annuler"), f.destroy).pack(side="right")
    f.grab_set()
    f.focus_set()
    appli.racine.wait_window(f)
    return reponse["genre"]


class FenetreGenerateur:
    """Small window to create a password."""

    def __init__(self, appli):
        self.appli = appli
        f = self.fenetre = tk.Toplevel(appli.racine)
        f.title(_("Créer un nouveau mot de passe"))
        f.configure(bg=BLANC, padx=24, pady=18)
        f.transient(appli.racine)
        f.resizable(False, False)

        tk.Label(f, text=_("Créer un nouveau mot de passe"), font=appli.f_titre,
                 bg=BLANC, fg=ENCRE).pack(anchor="w")

        self.var_genre = tk.StringVar(value="facile")
        choix = tk.Frame(f, bg=BLANC)
        choix.pack(anchor="w", pady=(12, 6))
        for valeur, texte in (("facile", _("Facile à lire (des mots)")),
                              ("solide", _("Très solide (lettres et signes)"))):
            tk.Radiobutton(choix, text=texte, value=valeur, variable=self.var_genre,
                           command=self.nouveau, font=appli.f_base, bg=BLANC,
                           fg=ENCRE, activebackground=BLANC, selectcolor=BLEU_CLAIR,
                           anchor="w").pack(anchor="w", pady=2)

        ligne = tk.Frame(f, bg=BLANC)
        ligne.pack(anchor="w", pady=6)
        tk.Label(ligne, text=_("Longueur :"), font=appli.f_gras, bg=BLANC, fg=GRIS).pack(side="left")
        self.var_longueur = tk.IntVar(value=4)
        self.reglette = tk.Scale(ligne, from_=3, to=6, orient="horizontal",
                                 variable=self.var_longueur, length=260,
                                 command=lambda v: self.nouveau(), font=appli.f_base,
                                 bg=BLANC, highlightthickness=0, sliderlength=36, width=22)
        self.reglette.pack(side="left", padx=10)
        self.etiquette_unite = tk.Label(ligne, text=_("mots"), font=appli.f_base, bg=BLANC, fg=GRIS)
        self.etiquette_unite.pack(side="left")

        self.var_mdp = tk.StringVar()
        tk.Entry(f, textvariable=self.var_mdp, font=appli.f_mdp, bg=JAUNE_FOND, fg=ENCRE,
                 relief="solid", bd=1, justify="center", width=28,
                 highlightthickness=2, highlightbackground=JAUNE_BORD,
                 readonlybackground=JAUNE_FOND, state="readonly").pack(fill="x", pady=12, ipady=8)

        boutons = tk.Frame(f, bg=BLANC)
        boutons.pack(fill="x", pady=(4, 0))
        appli.bouton(boutons, _("↻  Un autre"), self.nouveau).pack(side="left")
        self.bouton_copier = appli.bouton(boutons, _("Copier"), None)
        self.bouton_copier.configure(command=lambda: appli.copier(self.var_mdp.get(), self.bouton_copier))
        self.bouton_copier.pack(side="left", padx=10)
        appli.bouton(boutons, _("Annuler"), f.destroy).pack(side="right")
        appli.bouton(boutons, _("✔  Utiliser ce mot de passe"), self.utiliser, "vert").pack(side="right", padx=10)

        tk.Label(f, text=_("L'ancien mot de passe sera gardé dans les notes de la fiche."),
                 font=appli.f_petit, bg=BLANC, fg=GRIS).pack(anchor="w", pady=(12, 0))

        self._genre_precedent = None
        self.nouveau()
        f.grab_set()
        f.focus_set()

    def nouveau(self):
        genre = self.var_genre.get()
        if genre != self._genre_precedent:
            self._genre_precedent = genre
            if genre == "facile":
                self.reglette.configure(from_=3, to=6)
                self.var_longueur.set(4)
                self.etiquette_unite.configure(text=_("mots"))
            else:
                self.reglette.configure(from_=12, to=32)
                self.var_longueur.set(16)
                self.etiquette_unite.configure(text=_("caractères"))
        n = self.var_longueur.get()
        if genre == "facile":
            self.var_mdp.set(generer_phrase(n))
        else:
            self.var_mdp.set(generer_mot_de_passe(n))

    def utiliser(self):
        self.appli.remplacer_mot_de_passe(self.var_mdp.get())
        self.fenetre.destroy()


# ---------------------------------------------------------------------------
# Installation / uninstallation (built program: Windows and Linux;
# on Mac, the app is simply dragged into "Applications")
# ---------------------------------------------------------------------------

EDITEUR = "Louis"
CLE_DESINSTALLATION = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\PocketBook"


def dossier_special(numero, secours):
    """Windows folder (Desktop = 0x10, Start menu Programs = 0x02)."""
    try:
        import ctypes
        from ctypes import wintypes
        tampon = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        if ctypes.windll.shell32.SHGetFolderPathW(None, numero, None, 0, tampon) == 0:
            return Path(tampon.value)
    except Exception:
        pass
    return secours


def dossier_bureau_linux():
    try:
        import subprocess
        chemin = subprocess.run(["xdg-user-dir", "DESKTOP"], capture_output=True,
                                text=True, timeout=5).stdout.strip()
        if chemin and os.path.isdir(chemin):
            return Path(chemin)
    except Exception:
        pass
    return Path.home() / "Desktop"


def installation_possible():
    """Only the built program (.exe, Linux binary) installs itself."""
    return getattr(sys, "frozen", False) and (EST_WINDOWS or EST_LINUX)


def chemins_installation():
    if EST_WINDOWS:
        base = Path(os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local"))
        return {
            "dossier": base / "Pocket Book",
            "exe": base / "Pocket Book" / "Pocket Book.exe",
            "bureau": dossier_special(0x10, Path.home() / "Desktop") / "Pocket Book.lnk",
            "menu": dossier_special(0x02, Path.home()) / "Pocket Book.lnk",
        }
    donnees = Path(os.environ.get("XDG_DATA_HOME") or (Path.home() / ".local" / "share"))
    return {
        "dossier": donnees / "pocket-book",
        "exe": donnees / "pocket-book" / "pocket-book",
        "icone": donnees / "pocket-book" / "pocketbook.png",
        "bureau": dossier_bureau_linux() / "pocket-book.desktop",
        "menu": donnees / "applications" / "pocket-book.desktop",
        "commande": Path.home() / ".local" / "bin" / "pocket-book",
        "options": donnees / "pocket-book" / "installation.json",
    }


def creer_raccourci(lien, cible):
    """Windows: .lnk shortcut (built-in Windows tool). Linux: .desktop launcher."""
    import subprocess
    lien = Path(lien)
    lien.parent.mkdir(parents=True, exist_ok=True)
    if EST_WINDOWS:
        script = ("$r = (New-Object -ComObject WScript.Shell).CreateShortcut($env:MC_LIEN);"
                  "$r.TargetPath = $env:MC_CIBLE;"
                  "$r.WorkingDirectory = Split-Path $env:MC_CIBLE;"
                  "$r.IconLocation = $env:MC_CIBLE + ',0';"
                  "$r.Description = 'Pocket Book';"
                  "$r.Save()")
        env = dict(os.environ, MC_LIEN=str(lien), MC_CIBLE=str(cible))
        subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                        "-Command", script], env=env, check=True, timeout=30,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return
    icone = chemins_installation()["icone"]
    lien.write_text(
        "[Desktop Entry]\n"
        "Type=Application\n"
        f"Name={NOM_APPLI}\n"
        f"Comment={_('Mots de passe et contacts, sans internet')}\n"
        f'Exec="{cible}"\n'
        f"Icon={icone}\n"
        "Terminal=false\n"
        "Categories=Utility;Office;\n", encoding="utf-8")
    os.chmod(lien, 0o755)
    try:  # GNOME: allow launching from the Desktop
        subprocess.run(["gio", "set", str(lien), "metadata::trusted", "true"],
                       capture_output=True, timeout=5)
    except Exception:
        pass


def meme_fichier(a, b):
    try:
        return os.path.normcase(str(Path(a).resolve())) == os.path.normcase(str(Path(b).resolve()))
    except OSError:
        return False


def lire_registre(nom, defaut=None):
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, CLE_DESINSTALLATION) as cle:
            return winreg.QueryValueEx(cle, nom)[0]
    except (OSError, ImportError):
        return defaut


def option_bureau():
    """Had the user chosen a Desktop icon?"""
    if EST_WINDOWS:
        return bool(lire_registre("RaccourciBureau", 1))
    try:
        with open(chemins_installation()["options"], encoding="utf-8") as f:
            return bool(json.load(f).get("bureau", True))
    except (OSError, ValueError):
        return True


def deja_installe():
    return chemins_installation()["exe"].exists()


def inscrire_dans_windows(exe, avec_bureau):
    """Make "Pocket Book" appear in Settings > Apps (so it can be uninstalled)."""
    import winreg
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, CLE_DESINSTALLATION) as cle:
        valeurs = {
            "DisplayName": NOM_APPLI,
            "DisplayVersion": VERSION,
            "Publisher": EDITEUR,
            "DisplayIcon": f"{exe},0",
            "InstallLocation": str(Path(exe).parent),
            "UninstallString": f'"{exe}" --desinstaller',
            "InstallDate": datetime.now().strftime("%Y%m%d"),
        }
        for nom, valeur in valeurs.items():
            winreg.SetValueEx(cle, nom, 0, winreg.REG_SZ, valeur)
        for nom, valeur in (("NoModify", 1), ("NoRepair", 1),
                            ("EstimatedSize", max(1, os.path.getsize(exe) // 1024)),
                            ("RaccourciBureau", 1 if avec_bureau else 0)):
            winreg.SetValueEx(cle, nom, 0, winreg.REG_DWORD, valeur)


def installer(exe_source, avec_bureau):
    """Copy the program, create the shortcuts, register it with the system.

    Returns (success, error message).
    """
    chemins = chemins_installation()
    exe = chemins["exe"]
    try:
        exe.parent.mkdir(parents=True, exist_ok=True)
        if not meme_fichier(exe_source, exe):
            if EST_LINUX and exe.exists():
                exe.unlink()  # Linux: a program can be replaced even while it is running
            shutil.copy2(exe_source, exe)
        if EST_LINUX:
            os.chmod(exe, 0o755)
            shutil.copy2(ressource("pocketbook.png"), chemins["icone"])
    except PermissionError:
        return False, _("Pocket Book est sans doute encore ouvert.\n"
                        "Fermez-le, puis cliquez à nouveau sur « Installer ».")
    except OSError as exc:
        return False, _("La copie du programme a échoué.") + "\n\n" + str(exc)

    liens = [chemins["menu"]] + ([chemins["bureau"]] if avec_bureau else [])
    for lien in liens:
        try:
            creer_raccourci(lien, exe)
        except Exception:
            pass
    if not avec_bureau and chemins["bureau"].exists():
        try:
            chemins["bureau"].unlink()
        except OSError:
            pass
    try:
        if EST_WINDOWS:
            inscrire_dans_windows(exe, avec_bureau)
        else:
            ecrire_json_sur(chemins["options"], {"bureau": avec_bureau, "version": VERSION})
            commande = chemins["commande"]
            commande.parent.mkdir(parents=True, exist_ok=True)
            if commande.is_symlink() or commande.exists():
                commande.unlink()
            commande.symlink_to(exe)
    except Exception:
        pass
    return True, ""


def retirer_installation(supprimer_donnees):
    """Remove the program, shortcuts and registration. Returns a closing text."""
    import subprocess
    chemins = chemins_installation()
    for cle in ("bureau", "menu", "commande"):
        lien = chemins.get(cle)
        try:
            if lien and (lien.exists() or lien.is_symlink()):
                lien.unlink()
        except OSError:
            pass
    if EST_WINDOWS:
        try:
            import winreg
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, CLE_DESINSTALLATION)
        except OSError:
            pass
    if supprimer_donnees:
        shutil.rmtree(DOSSIER_DONNEES, ignore_errors=True)
    dossier = chemins["dossier"]
    if EST_WINDOWS:
        # The program is running: its folder is deleted right after it closes.
        subprocess.Popen(
            f'cmd /c ping 127.0.0.1 -n 4 > nul & rmdir /s /q "{dossier}"',
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0), cwd=str(Path.home()))
    else:
        shutil.rmtree(dossier, ignore_errors=True)
    texte = _("Pocket Book a été désinstallé.")
    if not supprimer_donnees:
        texte += "\n\n" + _("Vos fiches sont toujours dans :") + f"\n{DOSSIER_DONNEES}"
    return texte


def _fenetre_simple(titre, parent=None):
    """Small, clear and readable window for the installation."""
    appliquer_theme_couleurs("clair")
    racine = tk.Toplevel(parent) if parent is not None else tk.Tk()
    racine.title(titre)
    racine.configure(bg=BLANC, padx=34, pady=28)
    racine.resizable(False, False)
    mettre_icone(racine)
    famille = police_disponible(POLICES_TEXTE)
    polices = {
        "titre": tkfont.Font(family=famille, size=22, weight="bold"),
        "base": tkfont.Font(family=famille, size=14),
        "gras": tkfont.Font(family=famille, size=14, weight="bold"),
    }
    return racine, polices


def _gros_bouton(parent, texte, commande, polices, principal=False):
    return tk.Button(parent, text=texte, command=commande, font=polices["gras"],
                     bg=VERT if principal else BLANC, fg=SUR_ACCENT if principal else ENCRE,
                     activebackground=VERT_FONCE if principal else BLEU_CLAIR,
                     activeforeground=SUR_ACCENT if principal else ENCRE,
                     relief="solid", bd=1, padx=22, pady=10, cursor="hand2", highlightthickness=0)


def _choix_langue_installation(zone, polices, rafraichir):
    """Small row of languages at the top of the installation window."""
    ligne = tk.Frame(zone, bg=BLANC)
    ligne.pack(anchor="e", pady=(0, 10))
    for code, nom in LANGUES.items():
        actif = code == langue_actuelle()
        tk.Button(ligne, text=nom, font=polices["base"] if not actif else polices["gras"],
                  bg=BLEU if actif else BLANC, fg=SUR_ACCENT if actif else ENCRE,
                  activebackground=BLEU_CLAIR, relief="solid", bd=1, padx=8, pady=2,
                  cursor="hand2", highlightthickness=0,
                  command=lambda c=code: (choisir_langue(c), rafraichir())).pack(side="left", padx=2)


def fenetre_installation():
    """Launched from a download, a USB stick…: offer to install (or update)."""
    import subprocess
    chemins = chemins_installation()
    deja = deja_installe()
    racine, polices = _fenetre_simple(_("Installation de Pocket Book"))
    zone = tk.Frame(racine, bg=BLANC)
    zone.pack(fill="both", expand=True)
    var_bureau = tk.BooleanVar(value=option_bureau())

    def vider():
        for w in zone.winfo_children():
            w.destroy()

    def ecran_accueil():
        vider()
        racine.title(_("Installation de Pocket Book"))
        _choix_langue_installation(zone, polices, ecran_accueil)
        tk.Label(zone, text=_("Mettre à jour Pocket Book") if deja else _("Installer Pocket Book"),
                 font=polices["titre"], bg=BLANC, fg=ENCRE).pack(anchor="w")
        texte = (_("Une nouvelle version de Pocket Book va remplacer l'ancienne.\n"
                   "Vos fiches ne sont pas touchées.") if deja else
                 _("Pocket Book va être installé sur cet ordinateur.\n"
                   "Il fonctionne sans internet : rien ne quitte l'ordinateur.\n"
                   "Vos fiches seront rangées dans :") + f"\n{DOSSIER_DONNEES}")
        tk.Label(zone, text=texte, font=polices["base"], bg=BLANC, fg=GRIS,
                 justify="left").pack(anchor="w", pady=(10, 16))
        tk.Checkbutton(zone, text=_("Mettre une icône « Pocket Book » sur le Bureau"),
                       variable=var_bureau, font=polices["base"], bg=BLANC, fg=ENCRE,
                       activebackground=BLANC, selectcolor=BLANC).pack(anchor="w", pady=(0, 20))
        boutons = tk.Frame(zone, bg=BLANC)
        boutons.pack(fill="x")
        _gros_bouton(boutons, _("Annuler"), racine.destroy, polices).pack(side="right")
        _gros_bouton(boutons, _("Mettre à jour") if deja else _("Installer"), lancer, polices,
                     principal=True).pack(side="right", padx=(0, 12))

    def lancer():
        vider()
        tk.Label(zone, text=_("Installation en cours…"), font=polices["titre"], bg=BLANC,
                 fg=ENCRE).pack(anchor="w")
        racine.update()
        reussi, erreur = installer(Path(sys.executable), var_bureau.get())
        vider()
        if not reussi:
            tk.Label(zone, text=_("L'installation n'a pas pu se faire"), font=polices["titre"],
                     bg=BLANC, fg=ROUGE).pack(anchor="w")
            tk.Label(zone, text=erreur, font=polices["base"], bg=BLANC, fg=ENCRE,
                     justify="left").pack(anchor="w", pady=(10, 20))
            boutons = tk.Frame(zone, bg=BLANC)
            boutons.pack(fill="x")
            _gros_bouton(boutons, _("Fermer"), racine.destroy, polices).pack(side="right")
            _gros_bouton(boutons, _("Réessayer"), ecran_accueil, polices).pack(side="right", padx=(0, 12))
            return
        tk.Label(zone, text="✔  " + _("Pocket Book est installé"), font=polices["titre"], bg=BLANC,
                 fg=VERT_TEXTE).pack(anchor="w")
        if var_bureau.get():
            ou = _("Pour l'ouvrir, double-cliquez sur l'icône « Pocket Book » du Bureau\n"
                   "(ou cherchez « Pocket Book » dans le menu des applications).")
        else:
            ou = _("Pour l'ouvrir, cherchez « Pocket Book » dans le menu des applications.")
        tk.Label(zone, text=ou + "\n\n" + _("Ce fichier d'installation peut maintenant être rangé ou supprimé."),
                 font=polices["base"], bg=BLANC, fg=GRIS, justify="left").pack(anchor="w", pady=(10, 20))
        boutons = tk.Frame(zone, bg=BLANC)
        boutons.pack(fill="x")

        def ouvrir():
            subprocess.Popen([str(chemins["exe"]), "--langue", langue_actuelle()],
                             cwd=str(chemins["exe"].parent))
            racine.destroy()

        _gros_bouton(boutons, _("Fermer"), racine.destroy, polices).pack(side="right")
        _gros_bouton(boutons, _("Ouvrir Pocket Book"), ouvrir, polices,
                     principal=True).pack(side="right", padx=(0, 12))

    ecran_accueil()
    racine.mainloop()


def fenetre_desinstallation(parent=None):
    """Windows: Settings > Apps > Uninstall. Linux: button in the Settings.

    Returns True if the program was uninstalled.
    """
    racine, polices = _fenetre_simple(_("Désinstaller Pocket Book"), parent)
    resultat = {"fait": False}
    tk.Label(racine, text=_("Désinstaller Pocket Book ?"), font=polices["titre"], bg=BLANC,
             fg=ENCRE).pack(anchor="w")
    tk.Label(racine, text=_("Le programme et ses icônes vont être retirés de cet ordinateur.\n"
                            "Vos fiches sont gardées, dans :") + f"\n{DOSSIER_DONNEES}",
             font=polices["base"], bg=BLANC, fg=GRIS, justify="left").pack(anchor="w", pady=(10, 14))
    var_donnees = tk.BooleanVar(value=False)
    tk.Checkbutton(racine, text=_("Supprimer aussi toutes mes fiches et leurs sauvegardes"),
                   variable=var_donnees, font=polices["base"], bg=BLANC, fg=ROUGE,
                   activebackground=BLANC, selectcolor=BLANC).pack(anchor="w", pady=(0, 20))

    def confirmer():
        if var_donnees.get() and not messagebox.askyesno(
                _("Supprimer les fiches ?"),
                _("Toutes les fiches, les sauvegardes et les copies .txt de ce dossier seront "
                  "effacées définitivement :") + f"\n{DOSSIER_DONNEES}\n\n" + _("Continuer ?"),
                icon="warning", default="no", parent=racine):
            return
        texte = retirer_installation(var_donnees.get())
        messagebox.showinfo(NOM_APPLI, texte, parent=racine)
        resultat["fait"] = True
        racine.destroy()

    boutons = tk.Frame(racine, bg=BLANC)
    boutons.pack(fill="x")
    _gros_bouton(boutons, _("Annuler"), racine.destroy, polices).pack(side="right")
    tk.Button(boutons, text=_("Désinstaller"), command=confirmer, font=polices["gras"], bg=ROUGE,
              fg=SUR_ACCENT, activebackground="#7E2617", activeforeground=SUR_ACCENT,
              relief="solid", bd=1, padx=22, pady=10, cursor="hand2",
              highlightthickness=0).pack(side="right", padx=(0, 12))
    if parent is None:
        racine.mainloop()
    else:
        racine.transient(parent)
        racine.grab_set()
        parent.wait_window(racine)
    return resultat["fait"]


def installer_si_besoin():
    """Return True if the program must stop here (installation or uninstallation)."""
    if not installation_possible():
        return False
    if "--desinstaller" in sys.argv:
        fenetre_desinstallation()
        return True
    chemins = chemins_installation()
    if not meme_fichier(sys.executable, chemins["exe"]):
        fenetre_installation()
        return True
    # Launched from the installed copy: repair whatever is missing.
    if EST_WINDOWS and lire_registre("DisplayName") is None:
        try:
            inscrire_dans_windows(chemins["exe"], True)
        except Exception:
            pass
    if option_bureau() and not chemins["bureau"].exists():
        try:
            creer_raccourci(chemins["bureau"], chemins["exe"])
        except Exception:
            pass
    return False


def main():
    if "--langue" in sys.argv:  # language chosen in the installation window
        i = sys.argv.index("--langue")
        if i + 1 < len(sys.argv):
            choisir_langue(sys.argv[i + 1])
            LANGUE_IMPOSEE[0] = sys.argv[i + 1]
    else:
        choisir_langue(langue_du_systeme())
    if EST_WINDOWS:
        try:  # sharp text on high-DPI screens
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    if installer_si_besoin():
        return
    migrer_ancien_dossier()
    DOSSIER_DONNEES.mkdir(parents=True, exist_ok=True)
    racine = tk.Tk()
    Application(racine)
    racine.mainloop()


if __name__ == "__main__":
    main()
