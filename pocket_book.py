# -*- coding: utf-8 -*-
"""
Pocket Book — a very simple, offline password and contact keeper,
designed for people who are not at ease with computers.

- Password and contact cards, saved automatically.
- Password generator (easy to read or very strong).
- Reads old documents (.docx and .txt) WITHOUT EVER CHANGING THEM:
  each recognized document becomes a card, updated when it changes.
- .txt copy of each card, A to Z sorting, categories, themes, text size.
- Interface in English, French, Spanish, German and Italian (translations.py).
- Windows, macOS and Linux. Python standard library only.

Data is stored in "Documents/Pocket Book":
    pocketbook.json        cards and settings (not encrypted: see README)
    documents_index.json   document reading cache (can be deleted)
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

from translations import LANGUAGES, TRANSLATIONS, EASY_WORDS  # noqa: E402

# ---------------------------------------------------------------------------
# Interface language
# ---------------------------------------------------------------------------
# The program's text is written in English; _("text") returns its translation
# in the chosen language (translations.py). To add a language: see translations.py.

_LANGUAGE = ["en"]
FORCED_LANGUAGE = [None]   # language passed by the installation window


def _(text, **values):
    translated = TRANSLATIONS.get(_LANGUAGE[0], {}).get(text, text)
    return translated.format(**values) if values else translated


def n_(number, singular, plural, **values):
    """Singular or plural sentence depending on the number (in French, 0 and 1 are singular)."""
    one = number <= 1 if _LANGUAGE[0] == "fr" else number == 1
    return _(singular if one else plural, n=number, **values)


def with_colon(label):
    """"Libellé :" in French, "Label:" in the other languages."""
    return f"{label} :" if _LANGUAGE[0] == "fr" else f"{label}:"


def set_language(code):
    if code in LANGUAGES:
        _LANGUAGE[0] = code


def current_language():
    return _LANGUAGE[0]


def system_language():
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
    names = {"french": "fr", "english": "en", "spanish": "es", "german": "de", "italian": "it"}
    for code in codes:
        bottom = (code or "").lower()
        for name, short in names.items():
            if bottom.startswith(name):
                return short
        bottom = bottom.strip(' ("\n')
        if bottom[:2] in LANGUAGES:
            return bottom[:2]
    return "en"


APP_NAME = "Pocket Book"
VERSION = "1.1.0"
IS_WINDOWS = sys.platform.startswith("win")
IS_MAC = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")


def my_documents_folder():
    """The user's "Documents" folder (Windows: even when moved to OneDrive)."""
    if IS_LINUX:
        try:  # localized folder name (Documents, Dokumente, Documenti…)
            import subprocess
            path = subprocess.run(["xdg-user-dir", "DOCUMENTS"], capture_output=True,
                                  text=True, timeout=5).stdout.strip()
            if path and os.path.isdir(path) and os.path.normpath(path) != str(Path.home()):
                return Path(path)
        except Exception:
            pass
    if IS_WINDOWS:
        try:
            import ctypes
            from ctypes import wintypes
            buffer = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            if ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buffer) == 0:
                return Path(buffer.value)
        except Exception:
            pass
    return Path.home() / "Documents"


DATA_FOLDER = my_documents_folder() / "Pocket Book"
OLD_DATA_FOLDER = my_documents_folder() / "Mon carnet"   # name used by the first versions


def migrate_old_folder():
    """The first versions were called "Mon carnet": their cards are carried over.

    The old folder is copied (never deleted) to "Pocket Book".
    """
    old = OLD_DATA_FOLDER / "carnet.json"
    if DATA_FOLDER.exists() or not old.exists():
        return False
    try:
        shutil.copytree(OLD_DATA_FOLDER, DATA_FOLDER)
        os.replace(DATA_FOLDER / "carnet.json", DATA_FOLDER / "pocketbook.json")
        old_ones = DATA_FOLDER / "sauvegardes"
        if old_ones.exists():
            os.replace(old_ones, DATA_FOLDER / "backups")
            for f in (DATA_FOLDER / "backups").glob("carnet_*.json"):
                os.replace(f, f.with_name(f.name.replace("carnet_", "pocketbook_", 1)))
        # the settings pointed to the old folder (.txt copy…)
        path = DATA_FOLDER / "pocketbook.json"
        data = upgrade_data(json.loads(path.read_text(encoding="utf-8")))
        settings = data.get("settings", {})
        old_txt = settings.get("txt_folder", "")
        if old_txt.startswith(str(OLD_DATA_FOLDER)):
            settings["txt_folder"] = str(DATA_FOLDER) + old_txt[len(str(OLD_DATA_FOLDER)):]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except (OSError, ValueError):
        return False


def resource(name):
    """File shipped with the program (also works inside the .exe / app)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    for candidate in (os.path.join(base, name), os.path.join(base, "assets", name)):
        if os.path.exists(candidate):
            return candidate
    return os.path.join(base, name)


def open_with_system(path):
    """Open a file or folder with the system's usual program."""
    import subprocess
    if IS_WINDOWS:
        os.startfile(path)  # noqa: S606
    elif IS_MAC:
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])


def show_in_folder(path):
    """Open the folder containing the file, with the file selected if possible."""
    import subprocess
    if IS_WINDOWS:
        subprocess.Popen(["explorer", "/select,", os.path.normpath(path)])
    elif IS_MAC:
        subprocess.Popen(["open", "-R", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(Path(path).parent)])
BOOK_FILE = DATA_FOLDER / "pocketbook.json"
INDEX_FILE = DATA_FOLDER / "documents_index.json"
BACKUP_FOLDER = DATA_FOLDER / "backups"
BACKUPS_KEPT = 30

READ_EXTENSIONS = (".docx", ".txt")

FIELDS = {
    "account": ["name", "category", "site", "username", "email", "password", "notes", "source"],
    "contact": ["name", "mobile", "phone", "email", "address", "birthday", "notes", "source"],
}

def no_category():
    """Text for the "no category" choice (the category is optional)."""
    return _("(none)")


def all_categories():
    return _("All categories")

# Card fields: display order, and the ones that can be added / removed
FIELD_ORDER = {
    "account": ["category", "site", "username", "email", "password", "notes"],
    "contact": ["category", "mobile", "phone", "email", "address", "birthday", "notes"],
}
OPTIONAL_FIELDS = {
    "account": ["category", "site"],
    "contact": ["category", "phone", "address", "birthday"],
}
FIELD_LABELS = {
    "name": "Name", "category": "Category", "site": "Website",
    "username": "Username", "email": "Email address", "password": "Password",
    "notes": "Notes", "mobile": "Mobile", "phone": "Landline",
    "address": "Address", "birthday": "Birthday",
}

# Category colors: pale backgrounds, text always dark (easy to read)
CATEGORY_PALETTE = [
    ("Blue", "#D6E6FA"), ("Green", "#D6F0DC"), ("Yellow", "#FFF0B8"), ("Orange", "#FFDDC2"),
    ("Red", "#F8D3D3"), ("Purple", "#E6DAF5"), ("Pink", "#F8D6E8"),
    ("Turquoise", "#CDEFEA"), ("Grey", "#E4E2DC"), ("Brown", "#E8D9C7"),
]
TEXT_ON_PASTEL = "#1B1A17"
DEFAULT_CATEGORIES = [
    {"name": "Bank", "color": "#D6E6FA"}, {"name": "Administration", "color": "#E4E2DC"},
    {"name": "Health", "color": "#D6F0DC"}, {"name": "Email", "color": "#CDEFEA"},
    {"name": "Shopping", "color": "#FFDDC2"}, {"name": "Bills", "color": "#FFF0B8"},
    {"name": "Leisure", "color": "#E6DAF5"}, {"name": "Family", "color": "#F8D6E8"},
    {"name": "Work", "color": "#E8D9C7"},
]

# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------


def normalize(text_value):
    """Lowercase without accents, so "impot" finds "Impôts"."""
    text_value = unicodedata.normalize("NFD", text_value or "")
    text_value = "".join(c for c in text_value if unicodedata.category(c) != "Mn")
    return text_value.casefold()


def first_letter(name):
    """Sorting letter: A to Z, or "#" for a digit or a symbol."""
    for c in normalize(name).upper():
        if c.isalpha() and "A" <= c <= "Z":
            return c
        if c.isalnum():
            return "#"
    return "#"


def sort_key(name):
    return normalize(name).strip()


# ---------------------------------------------------------------------------
# Reading documents (never writing)
# ---------------------------------------------------------------------------

_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def docx_text(path):
    """Text of a .docx, paragraph by paragraph (tables included)."""
    with zipfile.ZipFile(path, "r") as z:
        xml = z.read("word/document.xml")
    root = ElementTree.fromstring(xml)
    lines = []

    def paragraph_text(p):
        parts = []
        for el in p.iter():
            if el.tag == _W + "t" and el.text:
                parts.append(el.text)
            elif el.tag == _W + "tab":
                parts.append("\t")
            elif el.tag in (_W + "br", _W + "cr"):
                parts.append("\n")
        return "".join(parts)

    def walk_tree(element):
        for child in element:
            if child.tag == _W + "p":
                lines.append(paragraph_text(child))
            elif child.tag == _W + "tbl":
                # A table: one line per row, cells separated by a tab
                for row in child.iter(_W + "tr"):
                    cells = [" ".join(paragraph_text(p) for p in cell.iter(_W + "p")).strip()
                             for cell in row.findall(_W + "tc")]
                    lines.append("\t".join(cells))
            else:
                walk_tree(child)

    walk_tree(root)
    return "\n".join(lines)


def txt_text(path):
    raw = Path(path).read_bytes()
    for encoding_name in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding_name)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def read_document(path):
    ext = Path(path).suffix.lower()
    if ext == ".docx":
        return docx_text(path)
    if ext == ".txt":
        return txt_text(path)
    raise ValueError(_("File type not supported"))


def list_documents(folder, exclude=()):
    """Every .docx / .txt in the folder and its subfolders.

    Also returns the number of old .doc files (Word 97-2003), which are not read.
    """
    results, old_entries = [], 0
    for root, subfolders, files in os.walk(folder):
        excluded = {os.path.normcase(os.path.abspath(e)) for e in exclude if e}
        subfolders[:] = [d for d in subfolders if not d.startswith(".")
                         and os.path.normcase(os.path.abspath(os.path.join(root, d))) not in excluded]
        for f in files:
            if f.startswith("~$") or f.startswith("."):
                continue  # Word temporary files
            if f.lower().endswith(READ_EXTENSIONS):
                results.append(os.path.join(root, f))
            elif f.lower().endswith(".doc"):
                old_entries += 1
    return results, old_entries


# ---------------------------------------------------------------------------
# Guessing a card from a document
# ---------------------------------------------------------------------------

# Labels recognized in documents (French, English, Spanish, German, Italian)
_LABELS = {
    "password": ["mot de passe", "mdp", "password", "pass", "pwd", "code secret",
                 "code", "mot passe", "passcode", "pin",
                 "contrasena", "clave", "clave de acceso",
                 "passwort", "kennwort", "pw",
                 "parola d'ordine", "parola chiave", "chiave"],
    "email": ["e-mail", "email", "mail", "adresse mail", "adresse e-mail",
              "courriel", "gmail", "hotmail", "outlook", "orange", "laposte",
              "yahoo", "free", "email address", "e-mail address",
              "correo", "correo electronico", "e-mail-adresse", "posta", "posta elettronica"],
    "username": ["identifiant", "id", "login", "utilisateur",
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
_RE_LABEL = re.compile(r"^\s*([^:=\t]{1,30}?)\s*(?:[:=]|\t+)\s*(.*)$")


def _which_label(label):
    lib = normalize(label).strip(" .-_*:=")
    for field, words in _LABELS.items():
        for word in words:
            if lib == normalize(word):
                return field
    return None


def guess_category(name):
    n = normalize(name)
    rules = [
        ("Bank", ["banque", "bnp", "credit", "caisse d", "societe generale",
                  "lcl", "boursorama", "cofidis", "cetelem", "cep", "paypal",
                  "bank", "banco", "banca", "sparkasse", "revolut", "n26"]),
        ("Administration", ["impot", "caf", "urssaf", "gouv", "retraite",
                            "ants", "france connect", "franceconnect", "inpi",
                            "pole emploi", "france travail", "tax", "hacienda",
                            "finanzamt", "agenzia entrate", "gov"]),
        ("Health", ["ameli", "doctolib", "mutuelle", "pharma", "sante",
                    "health", "salud", "gesundheit", "salute", "krankenkasse"]),
        ("Email", ["mail", "gmail", "outlook", "hotmail", "laposte.net",
                   "orange", "yahoo"]),
        ("Bills", ["edf", "engie", "free", "sfr", "bouygues", "veolia",
                   "eau", "gaz", "assurance"]),
        ("Shopping", ["amazon", "cdiscount", "fnac", "leboncoin", "dominos",
                      "mcdonald", "carrefour", "leclerc"]),
        ("Leisure", ["netflix", "deezer", "spotify", "disney", "canal",
                     "battlenet", "ea", "nvidia"]),
    ]
    for category, words in rules:
        for word in words:
            if re.search(r"(^|[^a-z])" + re.escape(word), n):
                return _(category)
    return ""  # nothing certain: no category rather than a wrong one


def guess_card(name, text_value):
    """Suggest a card (dictionary) from a document's text.

    Recognized formats, for example:
        adresse@mail.fr            Identifiant : 12345      1234567890
        (empty line)               MDP : xxxxx
        MotDePasse
    """
    card = {"username": "", "email": "", "password": "", "site": ""}
    emails, urls, tokens, texts = [], [], [], []
    pending_field = None

    for line in (text_value or "").splitlines():
        line = line.strip()
        if not line:
            continue

        if pending_field:
            if not card[pending_field]:
                card[pending_field] = line
                pending_field = None
                continue
            pending_field = None

        # A label on its own ("Mot de passe"): the value is on the next line.
        lone_field = _which_label(line)
        if lone_field:
            pending_field = lone_field
            continue

        m = _RE_LABEL.match(line)
        if m and not _RE_URL.match(line):
            field = _which_label(m.group(1))
            if field:
                value = m.group(2).strip()
                if field == "email" and value and not _RE_EMAIL.match(value):
                    field = "username"
                if not value:
                    pending_field = field
                elif not card[field]:
                    card[field] = value
                else:
                    texts.append(line)
                continue

        if _RE_EMAIL.match(line):
            emails.append(line)
        elif _RE_URL.match(line):
            urls.append(line)
        elif " " not in line and "\t" not in line:
            tokens.append(line)
        else:
            texts.append(line)

    for e in emails:
        if not card["email"]:
            card["email"] = e
        else:
            texts.append(e)
    for u in urls:
        if not card["site"]:
            card["site"] = u
        else:
            texts.append(u)

    if tokens:
        if not card["password"]:
            if len(tokens) >= 2:
                card["password"] = tokens[-1]
                rest = tokens[:-1]
                if not card["username"]:
                    card["username"] = rest.pop(0)
                texts.extend(rest)
            else:
                lone = tokens[0]
                already_account = card["email"] or card["username"]
                if not already_account and lone.isdigit() and len(lone) >= 8:
                    card["username"] = lone
                else:
                    card["password"] = lone
        else:
            if not card["username"]:
                card["username"] = tokens.pop(0)
            texts.extend(tokens)

    if not card["site"] and re.search(r"\.[a-z]{2,4}$", normalize(name)):
        card["site"] = name.strip()

    return {
        "type": "account",
        "name": name.strip() or _("Untitled"),
        "category": guess_category(name),
        "site": card["site"],
        "username": card["username"],
        "email": card["email"],
        "password": card["password"],
        "notes": "\n".join(texts),
    }


# ---------------------------------------------------------------------------
# Contacts: recognize and fill in
# ---------------------------------------------------------------------------

_RE_PHONE = re.compile(
    # France: 06 12 34 56 78, +33 6 12 34 56 78
    r"(?<!\d)(?:(?:\+|00)33\s?\(?0?\)?\s?[1-9]|0[1-9])(?:[\s.\-]?\d{2}){4}(?!\d)"
    # International: +44 20 7946 0958, +49 30 1234567, +56 9 1234 5678…
    r"|(?<![\d+])\+(?!33)\d{1,3}(?:[\s.\-]?\(?\d{1,4}\)?){2,5}(?!\d)"
    # North America: (555) 123-4567, 555-123-4567
    r"|(?<!\d)\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?!\d)")
_RE_POSTCODE = re.compile(r"(?<!\d)\d{5}(?!\d)\s+[A-Za-zÀ-ÿ]")
_STREET_WORDS = re.compile(
    r"(?:^|\s)(?:\d+\s*(?:bis|ter)?\s*,?\s*)?(?:rue|avenue|av\.|boulevard|bd|chemin|allee|"
    r"impasse|place|route|residence|batiment|bat\.|lieu-dit|cedex|quai|square|"
    r"cours|faubourg|hameau|lotissement|appartement|appt|bp|"
    r"street|st\.|road|rd\.|lane|drive|dr\.|ave\.?|way|court|ct\.|apt\.?|suite|terrace|blvd\.?|"
    r"calle|avenida|pasaje|camino|plaza|paseo|piso|"
    r"strasse|str\.|weg|platz|gasse|allee|"
    r"via|viale|piazza|corso|vicolo|largo)(?=[\s,])"
    # number after the street name (Hauptstraße 12, Via Roma 5, Calle Mayor 3)
    r"|[a-z]+(?:strasse|str\.|weg|platz|gasse)\s+\d")


_RE_ADDRESS_NUMBER_THEN_POSTCODE = re.compile(r"^\s*\d+[a-z]?\s+[^\d@]+[\s,]+\d{5}(?:-\d{4})?\s*$", re.IGNORECASE)


def address_line(line):
    """A postal address line: postcode + city, "12 rue …", "742 Main St, City 49007"."""
    if " " not in line.strip():
        return False
    if _RE_POSTCODE.search(line) or _RE_ADDRESS_NUMBER_THEN_POSTCODE.match(line):
        return True
    return bool(_STREET_WORDS.search(normalize(line) + " ") and re.search(r"\d", line))
_RE_DATE = re.compile(r"(?<!\d)(\d{1,2})[/.\-](\d{1,2})(?:[/.\-](\d{2,4}))?(?!\d)")
_BIRTHDAY_WORDS = re.compile(r"(anniv|ne le|nee le|naissance|ne\(e\)|birthday|born|date of birth|"
                             r"cumpleanos|nacimiento|nacio|geburtstag|geboren|compleanno|nato|nata|nascita)")
_ACCOUNT_WORDS = re.compile(r"(mot de passe|mdp|password|identifiant|login|code secret|pseudo|"
                            r"username|contrasena|usuario|passwort|kennwort|benutzername|"
                            r"nome utente|parola d'ordine)")


def _could_be_password(line):
    """A single "word" that is neither an e-mail, nor a phone number, nor a website."""
    return (" " not in line and "\t" not in line and not _RE_EMAIL.match(line)
            and not _RE_URL.match(line) and not _RE_PHONE.search(line))


def classify_document(text_value):
    """"compte", "contact" or "autre".

    Simple, predictable rules; when in doubt: "autre".
    """
    lines = [l.strip() for l in (text_value or "").splitlines() if l.strip()]
    if not lines:
        return "other"
    everything = normalize("\n".join(lines))

    account_signs = bool(_ACCOUNT_WORDS.search(everything))
    phone = bool(_RE_PHONE.search("\n".join(lines)))
    address = any(address_line(l) for l in lines)
    birthday = bool(_BIRTHDAY_WORDS.search(everything) and _RE_DATE.search(everything))
    contact_signs = phone or address or birthday

    if account_signs:
        return "account"
    emails = [l for l in lines if _RE_EMAIL.match(l)]
    lone_words = [l for l in lines if _could_be_password(l)]
    if contact_signs:
        return "contact"
    if emails and lone_words:
        return "account"
    if len(lines) <= 3 and lone_words:
        return "account"
    return "other"


def guess_contact(name, text_value):
    lines = [l.strip() for l in (text_value or "").splitlines() if l.strip()]
    mobiles, landlines, emails, address, notes = [], [], [], [], []
    birthday = ""
    for line in lines:
        n = normalize(line)
        rest = line
        for phone_number in [m.group(0) for m in _RE_PHONE.finditer(line)]:
            digits_on = re.sub(r"\D", "", phone_number)
            french = (re.match(r"^0[1-9]\d{8}$", digits_on) or re.match(r"^\s*(\+|00)33", phone_number))
            if french:  # French number: written "06 12 34 56 78"
                if digits_on.startswith("0033"):
                    digits_on = digits_on[2:]
                if digits_on.startswith("33"):
                    digits_on = "0" + digits_on[2:].lstrip("0")
                pretty = " ".join(digits_on[i:i + 2] for i in range(0, len(digits_on), 2))
                is_mobile = digits_on[:2] in ("06", "07")
            else:  # other country: kept as is
                pretty = re.sub(r"\s+", " ", phone_number.strip())
                is_mobile = False
            (mobiles if is_mobile else landlines).append(pretty)
            rest = rest.replace(phone_number, " ")
        for word in rest.split():
            if _RE_EMAIL.match(word.strip(",;()<>")):
                emails.append(word.strip(",;()<>"))
                rest = rest.replace(word, " ")
        rest_clean = re.sub(r"^[\s:;,\-–]*(tel|tél|telephone|téléphone|portable|fixe|mobile|"
                            r"e-mail|email|mail|courriel)?\s*[:.]?\s*", "", rest,
                            flags=re.IGNORECASE).strip(" :;,-–")
        if not rest_clean:
            continue
        if not birthday and _BIRTHDAY_WORDS.search(n) and _RE_DATE.search(line):
            birthday = _RE_DATE.search(line).group(0)
            continue
        if address_line(rest_clean):
            address.append(re.sub(r"^(adresse)\s*[:.]?\s*", "", rest_clean, flags=re.IGNORECASE))
            continue
        if normalize(rest_clean) == normalize(name):
            continue
        notes.append(rest_clean)
    return {
        "type": "contact",
        "name": name.strip() or _("Untitled"),
        "mobile": " / ".join(dict.fromkeys(mobiles)),
        "phone": " / ".join(dict.fromkeys(landlines)),
        "email": emails[0] if emails else "",
        "address": "\n".join(address),
        "birthday": birthday,
        "notes": "\n".join(notes + emails[1:]),
    }


def _possible_title(line):
    return not (_RE_PHONE.search(line) or address_line(line) or _RE_EMAIL.match(line)
                or _RE_URL.match(line))


def split_contacts(name, text_value):
    """A document may hold several contacts (a small address book).

    - blocks separated by an empty line, each starting with a name;
    - or a Word table: one row per person (name | phone | address…).
    Otherwise: a single contact, named after the file.
    """
    text_value = (text_value or "").strip()
    blocks = [b for b in re.split(r"\n\s*\n", text_value) if b.strip()]
    found = []
    for block in blocks:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if classify_document(block) == "contact" and _possible_title(lines[0]):
            found.append((lines[0], block))
    if len(found) >= 2 and len(found) >= len(blocks) - 1:
        return [guess_contact(title_text, block) for title_text, block in found]

    rows = [l for l in text_value.splitlines() if "\t" in l and _RE_PHONE.search(l)]
    if len(rows) >= 2:
        cards = []
        for row in rows:
            cells = [c.strip() for c in row.split("\t") if c.strip()]
            if cells and _possible_title(cells[0]):
                cards.append(guess_contact(cells[0], "\n".join(cells)))
        if len(cards) >= 2:
            return cards
    return [guess_contact(name, text_value)]


def guess(name, text_value, kind=None):
    """Card(s) suggested for a document, according to its kind (guessed if missing)."""
    kind = kind or classify_document(text_value)
    if kind == "contact":
        return split_contacts(name, text_value)
    return [guess_card(name, text_value)]


# ---------------------------------------------------------------------------
# Password generator
# ---------------------------------------------------------------------------

EASY_WORDS_FR = """
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

AMBIGUOUS = set("0O1lI|")
SYMBOLS = "!?@#$%&*+-=_"


def generate_password(length=16, uppercase=True, digits_on=True,
                      symbols=True, no_ambiguous=True):
    groups = [string.ascii_lowercase]
    if uppercase:
        groups.append(string.ascii_uppercase)
    if digits_on:
        groups.append(string.digits)
    if symbols:
        groups.append(SYMBOLS)
    if no_ambiguous:
        groups = ["".join(c for c in g if c not in AMBIGUOUS) for g in groups]
    length = max(length, len(groups))
    # at least one character from each chosen group
    characters = [secrets.choice(g) for g in groups]
    all_items = "".join(groups)
    characters += [secrets.choice(all_items) for _i in range(length - len(characters))]
    for i in range(len(characters) - 1, 0, -1):  # secure shuffle
        j = secrets.randbelow(i + 1)
        characters[i], characters[j] = characters[j], characters[i]
    return "".join(characters)


def generate_passphrase(word_count=4):
    listbox = EASY_WORDS.get(current_language(), EASY_WORDS_FR)  # words in the chosen language
    words = [secrets.choice(listbox).capitalize() for _i in range(word_count)]
    return "-".join(words) + "-" + str(secrets.randbelow(90) + 10)


# ---------------------------------------------------------------------------
# The book on disk
# ---------------------------------------------------------------------------


def write_json_safely(path, data):
    """Write to a temporary file then replace: never a half-written file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp_path, path)


# Files saved before version 1.1 used French names: they are converted when read.
_OLD_CARD_KEYS = {
    "nom": "name", "categorie": "category", "identifiant": "username", "mdp": "password",
    "telephone": "phone", "portable": "mobile", "adresse": "address", "anniversaire": "birthday",
    "cree_le": "created_at", "modifie_le": "modified_at", "importe_le": "imported_at",
    "modifiee_a_la_main": "edited_by_hand", "fichier_txt": "txt_file", "perso": "custom",
    "champs_ajoutes": "added_fields",
}
_OLD_SETTING_KEYS = {
    "taille_texte": "text_size", "dossier_documents": "documents_folder",
    "synchro_auto": "auto_sync", "dossier_txt": "txt_folder", "txt_connus": "known_txt",
    "sources_ecartees": "dismissed_sources", "langue": "language",
}
_OLD_VALUES = {"compte": "account", "autre": "other",
               "clair": "light", "sombre": "dark", "contraste": "contrast"}


def _renamed(old, keys):
    return {keys.get(k, k): v for k, v in old.items()}


def upgrade_data(data):
    """Convert a book saved by an older version (French names) to the current format."""
    if "fiches" not in data and "reglages" not in data:
        return data
    cards = []
    for old_card in data.get("fiches", []):
        card = _renamed(old_card, _OLD_CARD_KEYS)
        card["type"] = _OLD_VALUES.get(card.get("type"), card.get("type"))
        card["custom"] = [{"label": c.get("libelle", ""), "value": c.get("valeur", "")}
                          for c in card.get("custom", [])]
        card["added_fields"] = [_OLD_CARD_KEYS.get(f, f) for f in card.get("added_fields", [])]
        if not card["custom"]:
            del card["custom"]
        if not card["added_fields"]:
            del card["added_fields"]
        cards.append(card)
    settings = _renamed(data.get("reglages", {}), _OLD_SETTING_KEYS)
    if "theme" in settings:
        settings["theme"] = _OLD_VALUES.get(settings["theme"], settings["theme"])
    if "categories" in settings:
        settings["categories"] = [{"name": c.get("nom", ""), "color": c.get("couleur", "")}
                                  for c in settings["categories"]]
    return {"version": 2, "saved_at": data.get("enregistre_le", ""),
            "settings": settings, "cards": cards}


class Book:
    def __init__(self, file_path=BOOK_FILE, backups=BACKUP_FOLDER):
        self.file_path = Path(file_path)
        self.backups = Path(backups)
        self.cards = []
        self.settings = {"text_size": 1, "documents_folder": "", "theme": "light",
                         "auto_sync": True,
                         "txt_folder": str(DATA_FOLDER / _("Cards as text")),
                         "known_txt": [],
                         "categories": [{"name": _(c["name"]), "color": c["color"]}
                                        for c in DEFAULT_CATEGORIES]}
        self._txt_cache = {}
        self.txt_message = ""
        self.recovery_message = ""

    # -- loading -------------------------------------------------------------
    def load(self):
        if not self.file_path.exists():
            return
        try:
            self._load_from(self.file_path)
        except Exception:
            # Damaged file: set it aside and fall back to the latest backup.
            date = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            damaged = self.file_path.with_name("pocketbook_unreadable_" + date + ".json")
            try:
                shutil.copy2(self.file_path, damaged)
            except OSError:
                pass
            for backup in self.list_backups():
                try:
                    self._load_from(backup)
                    self.recovery_message = _(
                        "The notebook was damaged. The backup from {date} has been restored.",
                        date=backup.stem.replace("pocketbook_", ""))
                    return
                except Exception:
                    continue
            self.recovery_message = _(
                "The notebook was damaged and no backup could be read. A copy was kept: {file_path}", file_path=damaged.name)

    def _load_from(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = upgrade_data(json.load(f))
        cards = data.get("cards", [])
        for card in cards:
            card.setdefault("id", uuid.uuid4().hex)
            card.setdefault("type", "account")
            for field in FIELDS[card["type"] if card["type"] in FIELDS else "account"]:
                card.setdefault(field, "")
        self.cards = cards
        self.settings.update(data.get("settings", {}))
        self.ensure_categories()

    # -- saving --------------------------------------------------------------
    def save(self):
        write_json_safely(self.file_path, {
            "version": 2,
            "saved_at": datetime.now().isoformat(timespec="seconds"),
            "settings": self.settings,
            "cards": self.cards,
        })

    def list_backups(self):
        if not self.backups.exists():
            return []
        return sorted(self.backups.glob("pocketbook_*.json"), reverse=True)

    def daily_backup(self, force=False):
        """One copy per day (or on demand, e.g. before an import)."""
        if not self.file_path.exists():
            return
        self.backups.mkdir(parents=True, exist_ok=True)
        if force:
            name = "pocketbook_" + datetime.now().strftime("%Y-%m-%d_%Hh%M") + ".json"
        else:
            name = "pocketbook_" + datetime.now().strftime("%Y-%m-%d") + ".json"
        target_path = self.backups / name
        if force or not target_path.exists():
            shutil.copy2(self.file_path, target_path)
        for old_backup in self.list_backups()[BACKUPS_KEPT:]:
            try:
                old_backup.unlink()
            except OSError:
                pass

    # -- cards ---------------------------------------------------------------
    def new_card(self, type="account", **fields):
        card = {"id": uuid.uuid4().hex, "type": type}
        card.update({c: "" for c in FIELDS[type]})
        card["name"] = _("New contact") if type == "contact" else _("New card")
        card["created_at"] = datetime.now().isoformat(timespec="seconds")
        card.update({k: v for k, v in fields.items() if v is not None})
        self.cards.append(card)
        return card

    def find(self, card_id):
        for card in self.cards:
            if card["id"] == card_id:
                return card
        return None

    def delete(self, card_id):
        card = self.find(card_id)
        self.cards = [f for f in self.cards if f["id"] != card_id]
        source = (card or {}).get("source", "")
        if source and os.path.normcase(source) not in self.known_sources():
            # Deleted on purpose: synchronization must not recreate it.
            dismissed = self.settings.setdefault("dismissed_sources", [])
            if os.path.normcase(source) not in dismissed:
                dismissed.append(os.path.normcase(source))

    def restore_source(self, path):
        """Filing requested by hand: the document is no longer set aside."""
        dismissed = self.settings.get("dismissed_sources", [])
        if os.path.normcase(path) in dismissed:
            dismissed.remove(os.path.normcase(path))

    # -- categories ------------------------------------------------------------
    def categories(self):
        return self.settings.setdefault("categories", [])

    def category_names(self):
        return [c["name"] for c in self.categories()]

    def category_color(self, name):
        for c in self.categories():
            if c["name"] == name:
                return c.get("color", "")
        return ""

    def ensure_categories(self):
        """Every category used by a card exists in the list."""
        known_names = {normalize(n) for n in self.category_names()}
        for card in self.cards:
            name = card.get("category", "")
            if name and normalize(name) not in known_names:
                self.categories().append({"name": name, "color": "#E4E2DC"})
                known_names.add(normalize(name))

    def add_category(self, name):
        name = name.strip()
        if not name or normalize(name) in {normalize(n) for n in self.category_names()}:
            return False
        used = {c.get("color") for c in self.categories()}
        free_colors = [hex_color for _name, hex_color in CATEGORY_PALETTE if hex_color not in used]
        color = (free_colors or [CATEGORY_PALETTE[len(self.categories()) % len(CATEGORY_PALETTE)][1]])[0]
        self.categories().append({"name": name, "color": color})
        return True

    def rename_category(self, old, new):
        new = new.strip()
        if not new:
            return False
        if normalize(new) != normalize(old) and normalize(new) in {
                normalize(n) for n in self.category_names()}:
            return False
        for c in self.categories():
            if c["name"] == old:
                c["name"] = new
        for card in self.cards:
            if card.get("category") == old:
                card["category"] = new
        return True

    def delete_category(self, name):
        self.settings["categories"] = [c for c in self.categories() if c["name"] != name]
        for card in self.cards:
            if card.get("category") == name:
                card["category"] = ""

    def category_card_count(self, name):
        return sum(1 for f in self.cards if f.get("category") == name)

    def existing_category(self, name):
        """Keep a guessed category only if it still exists."""
        for n in self.category_names():
            if normalize(n) == normalize(name or ""):
                return n
        return ""

    # -- synchronization with the documents folder -----------------------------
    def sync_documents(self, documents, category_filter=None):
        """Create cards for new documents, update those of changed documents.

        - A card edited by hand in the book is never overwritten: it only gets
          a "the document has changed" note.
        - A deleted document does not delete its card.
        - Unrecognized documents create nothing.
        Returns a summary {"created", "updated", "to_check"}.
        """
        filter_fn = category_filter or (lambda p: p)
        now_str = datetime.now().isoformat(timespec="seconds")
        by_source = {}
        for card in self.cards:
            if card.get("source"):
                by_source.setdefault(os.path.normcase(card["source"]), []).append(card)
        summary = {"created": 0, "updated": 0, "to_check": 0}
        dismissed = set(self.settings.get("dismissed_sources", []))

        for path, doc in sorted(documents.items(), key=lambda kv: sort_key(kv[1]["name"])):
            kind = doc.get("kind", "other")
            existing = by_source.get(os.path.normcase(path), [])
            if not existing:
                if os.path.normcase(path) in dismissed:
                    continue  # card deleted on purpose: do not recreate it
                if kind in ("account", "contact") and not doc.get("error"):
                    for fields in filter_fn(guess(doc["name"], doc["text"], kind)):
                        self.new_card(source=path, source_mtime=doc["mtime"],
                                      imported_at=now_str, **fields)
                        summary["created"] += 1
                continue
            if all(f.get("source_mtime") == doc["mtime"] for f in existing):
                continue  # nothing new
            if any(f.get("source_mtime") is None for f in existing):
                for f in existing:   # card from before synchronization existed: just record the date
                    f["source_mtime"] = doc["mtime"]
                continue
            modified = [f for f in existing if f.get("edited_by_hand")
                        or f.get("modified_at", "") > f.get("imported_at", "")]
            if modified:
                date = datetime.now().strftime(_("%m/%d/%Y"))
                for f in existing:
                    f["source_mtime"] = doc["mtime"]
                    note = _("⚠ The document “{name}” changed on {date}: check this card (it was "
                             "not replaced).",
                             name=doc["name"], date=date)
                    f["notes"] = (f.get("notes", "").rstrip() + "\n" + note).strip()
                summary["to_check"] += 1
                continue
            # Card never edited by hand: rebuild it from the document
            card_kind = kind if kind in ("account", "contact") else existing[0].get("type", "account")
            suggestions = filter_fn(guess(doc["name"], doc["text"], card_kind))
            if len(suggestions) == 1 and len(existing) == 1:
                card = existing[0]
                for key in FIELDS.get(card.get("type", "account"), []):
                    if key != "source":
                        card[key] = ""
                card.update(suggestions[0])
                card.update(source_mtime=doc["mtime"], imported_at=now_str,
                            modified_at=now_str)
            else:
                ids = {f["id"] for f in existing}
                self.cards = [f for f in self.cards if f["id"] not in ids]
                for fields in suggestions:
                    self.new_card(source=path, source_mtime=doc["mtime"],
                                  imported_at=now_str, **fields)
            summary["updated"] += 1
        return summary

    def known_sources(self):
        return {os.path.normcase(f.get("source", "")) for f in self.cards if f.get("source")}

    # -- .txt copy of each card ------------------------------------------------
    def sync_txt(self):
        """One .txt per card in the chosen folder; only writes what changed.

        Returns True if all is well (otherwise the problem is in self.message_txt).
        """
        folder = self.settings.get("txt_folder", "")
        if not folder:
            return True
        folder = Path(folder)
        self.txt_message = ""
        wanted = {}   # relative path -> content
        taken = set()

        renames = {}   # new relative path -> old one (renamed card)
        known = {os.path.normcase(r) for r in self.settings.get("known_txt", [])}

        def place(card, rel):
            taken.add(os.path.normcase(rel))
            wanted[rel] = card_text(card)
            old = card.get("txt_file", "")
            if old and os.path.normcase(old) != os.path.normcase(rel):
                renames[rel] = old
            card["txt_file"] = rel

        # 1) each card keeps its file if it still matches its name
        to_place = []
        for card in sorted(self.cards, key=lambda f: f.get("created_at", "")):
            subfolder = _(TXT_SUBFOLDERS.get(card.get("type", "account"), "Other"))
            base = file_name(card.get("name", ""))
            old = card.get("txt_file", "")
            old_in_right_folder = old and Path(old).parent.name == subfolder
            stem = Path(old).stem if old else ""
            kept = (old_in_right_folder and os.path.normcase(old) not in taken
                    and (stem == base or re.fullmatch(re.escape(base) + r" \(\d+\)", stem)))
            if kept:
                place(card, old)
            else:
                to_place.append((card, subfolder, base))
        # 2) new (or renamed) cards get a free name
        for card, subfolder, base in to_place:
            n = 1
            while True:
                rel = os.path.join(subfolder, (base if n == 1 else f"{base} ({n})") + ".txt")
                free = os.path.normcase(rel) not in taken and (
                    os.path.normcase(rel) in known or not (folder / rel).exists())
                if free:  # never overwrite a file that was not created by the book
                    break
                n += 1
            place(card, rel)

        try:
            wanted_norm = {os.path.normcase(r) for r in wanted}
            # Renamed card: rename its file (instead of creating a new one)
            for rel, old in renames.items():
                source, target_path = folder / old, folder / rel
                if (os.path.normcase(old) not in wanted_norm and source.exists()
                        and not target_path.exists()):
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(source, target_path)
                    self._txt_cache.pop(str(source), None)
            for rel, content in wanted.items():
                path = folder / rel
                if self._txt_cache.get(str(path)) == content:
                    continue
                try:
                    current = path.read_text(encoding="utf-8-sig")
                except OSError:
                    current = None
                if current != content:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    temp_path = path.with_name(path.name + ".tmp")
                    with open(temp_path, "w", encoding="utf-8-sig", newline="\r\n") as f:
                        f.write(content)
                    os.replace(temp_path, path)
                self._txt_cache[str(path)] = content
            # 3) files of deleted cards: moved aside, never erased
            for rel in self.settings.get("known_txt", []):
                if os.path.normcase(rel) in wanted_norm:
                    continue
                path = folder / rel
                if path.exists():
                    if not any(os.path.normcase(r) == os.path.normcase(rel) for r in wanted):
                        trash = folder / _("Deleted cards")
                        trash.mkdir(parents=True, exist_ok=True)
                        target_path = trash / path.name
                        n = 2
                        while target_path.exists():
                            target_path = trash / f"{path.stem} ({n}){path.suffix}"
                            n += 1
                        os.replace(path, target_path)
                self._txt_cache.pop(str(path), None)
            self.settings["known_txt"] = sorted(wanted)
            return True
        except OSError as exc:
            self.txt_message = str(exc)
            return False

    def change_txt_folder(self, new):
        """New folder: everything is rewritten there (the old one is left as is)."""
        self.settings["txt_folder"] = str(new)
        self.settings["known_txt"] = []
        self._txt_cache = {}
        for card in self.cards:
            card.pop("txt_file", None)


TXT_SUBFOLDERS = {"account": "Passwords", "contact": "Contacts"}   # translated when used
_FORBIDDEN = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_RESERVED = {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}


def file_name(name):
    """Valid Windows file name built from the card's name."""
    clean = _FORBIDDEN.sub("-", name or "").strip().strip(".").strip()
    clean = re.sub(r"\s+", " ", clean)[:80].strip()
    if not clean or clean.upper() in _RESERVED:
        clean = (clean + " (" + _("card") + ")").strip() if clean else _("Untitled")
    return clean


def _readable_date(iso):
    try:
        return datetime.fromisoformat(iso).strftime(_("%m/%d/%Y at %H:%M"))
    except (TypeError, ValueError):
        return ""


def field_visible(card, field):
    """An optional field only appears if it is filled in or added on purpose."""
    kind = card.get("type", "account")
    return (field not in OPTIONAL_FIELDS.get(kind, []) or bool(card.get(field))
            or field in card.get("added_fields", []))


def card_text(card):
    """Content of a card's .txt file (readable in Notepad)."""
    kind = card.get("type", "account")
    lines = [card.get("name", "") or _("Untitled"), "=" * max(len(card.get("name", "")), 8), ""]
    blocks = []
    for field in FIELD_ORDER.get(kind, []):
        if field == "notes" or not field_visible(card, field):
            continue
        value = card.get(field, "")
        if field == "address":
            blocks += ["", with_colon(_("Address")), value or "-"]
        else:
            lines.append(f"{with_colon(_(FIELD_LABELS[field]))} {value}")
    for custom in card.get("custom", []):
        lines.append(f"{with_colon(custom.get('label', ''))} {custom.get('value', '')}")
    lines += blocks
    lines += ["", with_colon(_("Notes")), card.get("notes", "") or "-", ""]
    date = _readable_date(card.get("modified_at") or card.get("created_at"))
    lines.append("-" * 60)
    lines.append(_("Automatic copy made by Pocket Book (card changed on {date}).", date=date)
                 if date else _("Automatic copy made by Pocket Book."))
    lines.append(_("This file is rewritten after every change: edit the card in the notebook."))
    return "\n".join(lines) + "\n"


def card_matches(card, search):
    if not search:
        return True
    everything = " ".join(str(v) for k, v in card.items()
                          if k not in ("id", "type", "source", "password", "created_at", "modified_at",
                                       "custom", "added_fields", "txt_file"))
    everything += " " + " ".join(f"{p.get('label', '')} {p.get('value', '')}"
                                 for p in card.get("custom", []))
    return search in normalize(everything)


# ---------------------------------------------------------------------------
# Document index (background reading, with a cache)
# ---------------------------------------------------------------------------


def load_index():
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"folder": "", "documents": {}}


def index_documents(folder, old_index, progress=None, exclude=()):
    """Read new or changed documents; reuse the cache for the others."""
    old_entries = old_index.get("documents", {}) if old_index.get("folder") == folder else {}
    paths, old_doc_count = list_documents(folder, exclude)
    total = len(paths)
    new_entries = {}
    for i, path in enumerate(paths, 1):
        try:
            st = os.stat(path)
        except OSError:
            continue
        old = old_entries.get(path)
        if old and old.get("mtime") == st.st_mtime and old.get("size") == st.st_size:
            old.setdefault("kind", classify_document(old.get("text", "")))
            new_entries[path] = old
        else:
            try:
                text_value = read_document(path)
                error = ""
            except Exception as exc:  # damaged or protected document, renamed old .doc…
                text_value = ""
                error = _("Could not read this document ({error}).", error=type(exc).__name__)
            new_entries[path] = {"name": Path(path).stem, "mtime": st.st_mtime,
                                 "size": st.st_size, "text": text_value, "error": error,
                                 "kind": classify_document(text_value)}
        if progress and (i % 25 == 0 or i == total):
            progress(i, total)
    return {"folder": folder, "documents": new_entries, "old_doc_count": old_doc_count}


# ===========================================================================
# Interface
# ===========================================================================

import tkinter as tk  # noqa: E402  (after the logic, so it can be tested on its own)
from tkinter import filedialog, messagebox, ttk  # noqa: E402
import tkinter.font as tkfont  # noqa: E402

# Readable fonts available on each system (the first one found is used)
TEXT_FONTS = ["Verdana", "Segoe UI", "DejaVu Sans", "Noto Sans", "Helvetica"]
MONO_FONTS = ["Consolas", "Menlo", "DejaVu Sans Mono", "Noto Sans Mono", "Courier New"]


def available_font(candidates):
    try:
        present_fonts = {f.lower() for f in tkfont.families()}
    except Exception:
        return candidates[0]
    for name in candidates:
        if name.lower() in present_fonts:
            return name
    return candidates[-1]


def set_icon(window):
    """Window icon: .ico on Windows, .png elsewhere."""
    try:
        if IS_WINDOWS:
            window.iconbitmap(default=resource("pocketbook.ico"))
        else:
            image = tk.PhotoImage(file=resource("pocketbook.png"))
            window.iconphoto(True, image)
            window._icon = image  # keep the image in memory
    except Exception:
        pass

# Color themes (all checked for good text contrast)
THEMES = {
    "light": {"name": "Light", "BLUE_TEXT": "#1E4F91", "GREEN_TEXT": "#1F6B3A", "BG": "#F6F4EF", "WHITE": "#FFFFFF", "INK": "#1B1A17",
              "GREY": "#4A4740", "BORDER": "#CFC9BC", "BORDER_STRONG": "#8C8578",
              "BLUE": "#1E4F91", "BLUE_LIGHT": "#E3ECF8", "BLUE_DARK": "#163B6D",
              "GREEN": "#1F6B3A", "GREEN_DARK": "#174F2B", "RED": "#A4321F",
              "RED_LIGHT": "#F6E3DF", "YELLOW_BG": "#FFF6E5", "YELLOW_BORDER": "#E0B867",
              "YELLOW_TEXT": "#6B4A0C", "BAR": "#EDE9E0", "LETTER_OFF": "#A8A296",
              "TEXT_BG": "#FBFAF7"},
    "dark": {"name": "Dark", "BLUE_TEXT": "#8DB8F0", "GREEN_TEXT": "#7FD09E", "BG": "#1C1D20", "WHITE": "#2A2C30", "INK": "#F1F0EC",
             "GREY": "#C8C5BE", "BORDER": "#4A4D53", "BORDER_STRONG": "#8B8E94",
             "BLUE": "#2F6DBA", "BLUE_LIGHT": "#2F3B4E", "BLUE_DARK": "#24578F",
             "GREEN": "#23784A", "GREEN_DARK": "#1A5C38", "RED": "#FF9C8A",
             "RED_LIGHT": "#4A2C28", "YELLOW_BG": "#3A3020", "YELLOW_BORDER": "#B48B35",
             "YELLOW_TEXT": "#F3D58E", "BAR": "#25262A", "LETTER_OFF": "#6E7076",
             "TEXT_BG": "#232528"},
    "contrast": {"name": "High contrast", "BLUE_TEXT": "#0033A0", "GREEN_TEXT": "#00591F", "BG": "#FFFFFF", "WHITE": "#FFFFFF",
                 "INK": "#000000", "GREY": "#000000", "BORDER": "#000000",
                 "BORDER_STRONG": "#000000", "BLUE": "#0033A0", "BLUE_LIGHT": "#D6E4FF",
                 "BLUE_DARK": "#00226B", "GREEN": "#00591F", "GREEN_DARK": "#003D15",
                 "RED": "#B00000", "RED_LIGHT": "#FFE0E0", "YELLOW_BG": "#FFF4B3",
                 "YELLOW_BORDER": "#000000", "YELLOW_TEXT": "#000000", "BAR": "#F0F0F0",
                 "LETTER_OFF": "#8A8A8A", "TEXT_BG": "#FFFFFF"},
    "sepia": {"name": "Soft sepia", "BLUE_TEXT": "#7A4416", "GREEN_TEXT": "#3D6B29", "BG": "#F2E8D5", "WHITE": "#FBF5E9", "INK": "#2B2116",
              "GREY": "#5B4A36", "BORDER": "#D5C3A1", "BORDER_STRONG": "#9C8768",
              "BLUE": "#7A4416", "BLUE_LIGHT": "#EEDCC0", "BLUE_DARK": "#5C3210",
              "GREEN": "#3D6B29", "GREEN_DARK": "#2C5020", "RED": "#9E2F1C",
              "RED_LIGHT": "#F3DCD3", "YELLOW_BG": "#FFF3D6", "YELLOW_BORDER": "#D2A852",
              "YELLOW_TEXT": "#5E410B", "BAR": "#EADCC2", "LETTER_OFF": "#B0A089",
              "TEXT_BG": "#FDF9F0"},
}
ON_ACCENT = "#FFFFFF"   # text on blue / green buttons, whatever the theme


def apply_theme_colors(name):
    """Change the colors used by the whole interface."""
    globals().update({k: v for k, v in THEMES.get(name, THEMES["light"]).items() if k != "name"})


apply_theme_colors("light")

SIZES = [12, 14, 17, 20]          # text sizes (points)
LETTERS = ["All"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["#"]
KIND_LABELS = {"account": "Password", "contact": "Contact", "other": "?"}
KIND_NAMES = {"account": "a password", "contact": "a contact", "other": "not recognised"}
def kind_color(kind):
    return {"account": BLUE_TEXT, "contact": GREEN_TEXT}.get(kind, GREY)


class Application:
    def __init__(self, root):
        self.root = root
        self.book = Book()
        self.book.load()
        try:
            self.book.daily_backup()
        except OSError:
            pass

        self.page = "account"
        self.letter = "All"
        self.current_id = None
        self._loading = False
        self._timer = None
        self._search_timer = None
        self.index = load_index()
        self.message_queue = queue.Queue()
        self.reading_in_progress = False
        self.shown_paths = []
        self.shown_ids = []
        self._search_cache = {}
        self._txt_alert_shown = False
        self._sync_requested = False

        # Language: the book's, otherwise the system's (or the one chosen at installation)
        if FORCED_LANGUAGE[0]:
            self.book.settings["language"] = FORCED_LANGUAGE[0]
        set_language(self.book.settings.get("language") or current_language())
        self.book.settings["language"] = current_language()
        apply_theme_colors(self.book.settings.get("theme", "light"))
        self._fonts()
        self._window()
        self._build()
        self.apply_size(self.book.settings.get("text_size", 1), save=False)
        self.show_page("account")
        self.root.after(50, self._after_opening)
        self.root.after(300, self._enable_drag_and_drop)
        self.root.after(60000, self._periodic_sync)

    # ------------------------------------------------------------------ base
    def _fonts(self):
        family_name = available_font(TEXT_FONTS)
        self.family_name = family_name
        self.f_base = tkfont.Font(family=family_name, size=14)
        self.f_bold = tkfont.Font(family=family_name, size=14, weight="bold")
        self.f_small = tkfont.Font(family=family_name, size=12)
        self.f_title = tkfont.Font(family=family_name, size=20, weight="bold")
        self.f_password = tkfont.Font(family=available_font(MONO_FONTS), size=20, weight="bold")
        self.f_letter = tkfont.Font(family=family_name, size=13, weight="bold")

    def _window(self):
        r = self.root
        r.title(APP_NAME)
        r.configure(bg=BG)
        r.minsize(900, 600)
        try:
            if IS_LINUX:
                r.attributes("-zoomed", True)
            else:
                r.state("zoomed")
        except tk.TclError:
            r.geometry("1280x860")
        r.protocol("WM_DELETE_WINDOW", self.quit_app)
        set_icon(r)
        r.option_add("*TCombobox*Listbox.font", self.f_base)
        self._style()

    def _style(self):
        """Colors of drop-down lists and scrollbars (according to the theme)."""
        r = self.root
        r.option_add("*TCombobox*Listbox.background", WHITE)
        r.option_add("*TCombobox*Listbox.foreground", INK)
        r.option_add("*TCombobox*Listbox.selectBackground", BLUE)
        r.option_add("*TCombobox*Listbox.selectForeground", ON_ACCENT)
        style = ttk.Style(r)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TCombobox", padding=6, fieldbackground=WHITE, background=WHITE,
                        foreground=INK, arrowcolor=INK, arrowsize=22,
                        bordercolor=BORDER_STRONG)
        style.map("TCombobox", fieldbackground=[("readonly", WHITE)],
                  foreground=[("readonly", INK)], selectbackground=[("readonly", WHITE)],
                  selectforeground=[("readonly", INK)])
        style.configure("Vertical.TScrollbar", arrowsize=22, width=22, background=BAR,
                        troughcolor=BG, arrowcolor=INK, bordercolor=BORDER)

    def button(self, parent, text_value, command, kind="normal", font=None, **options):
        colors = {
            "normal": (WHITE, INK, BLUE_LIGHT),
            "blue": (BLUE, ON_ACCENT, BLUE_DARK),
            "green": (GREEN, ON_ACCENT, GREEN_DARK),
            "danger": (WHITE, RED, RED_LIGHT),
            "blue_outline": (WHITE, BLUE_TEXT, BLUE_LIGHT),
        }[kind]
        b = tk.Button(parent, text=text_value, command=command, font=font or self.f_bold,
                      bg=colors[0], fg=colors[1], activebackground=colors[2],
                      activeforeground=colors[1] if kind != "blue" and kind != "green" else ON_ACCENT,
                      relief="solid", bd=1, padx=14, pady=6, cursor="hand2",
                      highlightthickness=0, **options)
        return b

    def text_entry(self, parent, variable, font=None):
        return tk.Entry(parent, textvariable=variable, font=font or self.f_base,
                        bg=WHITE, fg=INK, relief="solid", bd=1, insertbackground=INK,
                        highlightthickness=2, highlightcolor="#E08A1E",
                        highlightbackground=BORDER, insertwidth=3)

    # ------------------------------------------------------------ construction
    def _build(self):
        r = self.root

        # --- Header
        # 1st line: title + text size; 2nd line: the tabs (which wrap
        # when the window is narrow or the text very large).
        header = tk.Frame(r, bg=WHITE, padx=16, pady=8)
        header.pack(fill="x")
        tk.Frame(r, bg=BORDER, height=2).pack(fill="x")
        title_row = tk.Frame(header, bg=WHITE)
        title_row.pack(fill="x")
        tk.Label(title_row, text=APP_NAME, font=self.f_title, bg=WHITE,
                 fg=INK).pack(side="left")
        self.tabs_area = tk.Frame(header, bg=WHITE)
        self.tabs_area.pack(fill="x", pady=(6, 0))
        self.tabs = {}
        for page, text_value in (("account", _("My passwords")), ("contact", _("My contacts")),
                                 ("documents", _("My documents")), ("settings", "⚙ " + _("Settings"))):
            self.tabs[page] = self.button(self.tabs_area, text_value,
                                          lambda p=page: self.show_page(p))
        self.tabs_area.bind("<Configure>", lambda e: self._wrap_in_rows(
            self.tabs_area, list(self.tabs.values()), gap=6))

        size_area = tk.Frame(title_row, bg=WHITE)
        size_area.pack(side="right")
        tk.Label(size_area, text=_("Text"), font=self.f_bold, bg=WHITE,
                 fg=GREY).pack(side="left", padx=(0, 8))
        self.size_buttons = []
        for i in range(len(SIZES)):
            font = tkfont.Font(family=self.family_name, size=11 + i * 4, weight="bold")
            b = tk.Button(size_area, text=_("A"), font=font, width=2,
                          command=lambda i=i: self.apply_size(i),
                          relief="solid", bd=1, cursor="hand2", highlightthickness=0)
            b.pack(side="left", padx=3)
            self.size_buttons.append(b)

        # --- Letter bar
        self.letter_bar = tk.Frame(r, bg=BAR, padx=12, pady=8)
        self.letter_bar.pack(fill="x")
        self.letter_separator = tk.Frame(r, bg=BORDER, height=1)
        self.letter_separator.pack(fill="x")
        self.letter_buttons = {}
        for letter in LETTERS:
            b = tk.Button(self.letter_bar, text=_(letter) if letter == "All" else letter, font=self.f_letter,
                          relief="solid", bd=1, cursor="hand2", highlightthickness=0,
                          padx=8 if letter == "All" else 0, width=0 if letter == "All" else 2,
                          command=lambda l=letter: self.choose_letter(l))
            self.letter_buttons[letter] = b
        self.letter_bar.bind("<Configure>", lambda e: self._place_letters())

        # --- Footer (before the center so it stays visible)
        footer = tk.Frame(r, bg=WHITE, padx=16, pady=8)
        footer.pack(side="bottom", fill="x")
        tk.Frame(r, bg=BORDER, height=2).pack(side="bottom", fill="x")
        # The button first: if the window is narrow, the sentence gets cut instead.
        self.button(footer, _("Save now"), self.save_now,
                    "green").pack(side="right")
        self.status_label = tk.Label(footer, text="", font=self.f_bold, bg=WHITE, fg=GREEN_TEXT)
        self.status_label.pack(side="left")
        self.sync_label = tk.Label(footer, text="", font=self.f_small, bg=WHITE, fg=GREY)
        self.sync_label.pack(side="left", padx=(16, 0))

        # --- Center
        self.center = tk.Frame(r, bg=BG)
        self.center.pack(fill="both", expand=True)
        self._cards_page()
        self._documents_page()
        self._settings_page()

    def _place_letters(self):
        """Lay the letters out on one or more lines depending on the width."""
        self._wrap_in_rows(self.letter_bar, [self.letter_buttons[l] for l in LETTERS],
                           margin=24, gap=3)

    def _wrap_in_rows(self, frame, buttons, margin=0, gap=3):
        """Place buttons from left to right, wrapping to a new line if needed."""
        available_width = max(frame.winfo_width() - margin, 200)
        line, col, x = 0, 0, 0
        for b in buttons:
            w = b.winfo_reqwidth() + 2 * gap
            if x + w > available_width and col > 0:
                line, col, x = line + 1, 0, 0
            b.grid(row=line, column=col, padx=gap, pady=3, sticky="nsew")
            col += 1
            x += w

    # ----------------------------------------------------------- cards page
    def _cards_page(self):
        """A single page, showing either the passwords or the contacts."""
        p = self.cards_page = tk.Frame(self.center, bg=BG, padx=16, pady=12)

        left = tk.Frame(p, bg=BG)
        left.pack(side="left", fill="y", padx=(0, 16))
        self.search_title = tk.Label(left, text="", font=self.f_bold, bg=BG,
                                     fg=INK, anchor="w")
        self.search_title.pack(fill="x")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._cards_search_changed())
        self.text_entry(left, self.search_var).pack(fill="x", ipady=4, pady=(2, 6))

        category_row = tk.Frame(left, bg=BG)
        category_row.pack(fill="x", pady=(0, 4))
        tk.Label(category_row, text=_("Category:"), font=self.f_small, bg=BG,
                 fg=GREY).pack(side="left")
        self.category_filter_var = tk.StringVar(value=all_categories())
        self.category_filter_choice = ttk.Combobox(category_row, textvariable=self.category_filter_var,
                                                   font=self.f_small, state="readonly", width=16)
        self.category_filter_choice.pack(side="left", padx=(6, 0), fill="x", expand=True)
        self.category_filter_choice.bind("<<ComboboxSelected>>", lambda e: self.fill_cards_list())

        self.count_label = tk.Label(left, text="", font=self.f_small, bg=BG,
                                    fg=GREY, anchor="w")
        self.count_label.pack(fill="x")

        list_frame = tk.Frame(left, bg=BG)
        list_frame.pack(fill="both", expand=True, pady=6)
        self.cards_list = tk.Listbox(
            list_frame, font=self.f_base, width=26, activestyle="none",
            bg=WHITE, fg=INK, selectbackground=BLUE, selectforeground=ON_ACCENT,
            relief="solid", bd=1, highlightthickness=0, exportselection=False)
        bar = ttk.Scrollbar(list_frame, orient="vertical",
                            command=self.cards_list.yview)
        self.cards_list.configure(yscrollcommand=bar.set)
        self.cards_list.pack(side="left", fill="both", expand=True)
        bar.pack(side="right", fill="y")
        self.cards_list.bind("<<ListboxSelect>>", lambda e: self._card_selected())

        self.new_button = self.button(left, "", self.create_card, "blue_outline")
        self.new_button.pack(fill="x", pady=(4, 0))

        # Right side: the card, built from its fields
        self.right = tk.Frame(p, bg=WHITE, padx=22, pady=16,
                              highlightthickness=2, highlightbackground=BORDER)
        self.right.pack(side="left", fill="both", expand=True)
        self.no_card = tk.Label(self.right, text="", font=self.f_base, bg=WHITE,
                                fg=GREY, justify="left")
        self.form_area = tk.Frame(self.right, bg=WHITE)
        self.card_vars = {}
        self.card_texts = {}
        self.card_widgets = {}
        self.name_entry = None
        self._focus_after = None

    # ------------------------------------------------------------- card form
    def _card_var(self, key, value, custom_index=None):
        var = tk.StringVar(value=value)
        var.trace_add("write", lambda *a: self._value_changed(key, var.get(), custom_index))
        self.card_vars[key if custom_index is None else ("custom", custom_index)] = var
        return var

    def _card_text_area(self, parent, key, value, height):
        area = tk.Text(parent, font=self.f_base, height=height, wrap="word",
                       bg=WHITE, fg=INK, relief="solid", bd=1, insertbackground=INK,
                       highlightthickness=2, highlightcolor="#E08A1E",
                       highlightbackground=BORDER, padx=8, pady=6,
                       insertwidth=3, undo=True)
        area.insert("1.0", value)
        area.edit_modified(False)
        area.edit_reset()
        area.bind("<<Modified>>", lambda e: self._text_changed(key))
        self.card_texts[key] = area
        return area

    def _remove_button(self, parent, line, key, custom_index=None):
        b = tk.Button(parent, text="✕", font=self.f_bold, width=2, command=lambda:
                      self.remove_field(key, custom_index), bg=WHITE, fg=RED,
                      activebackground=RED_LIGHT, activeforeground=RED,
                      relief="solid", bd=1, cursor="hand2", highlightthickness=0)
        b.grid(row=line, column=3, sticky="n", padx=(6, 0), pady=5)
        return b

    def _label(self, parent, line, text_value, top=False):
        tk.Label(parent, text=text_value, font=self.f_bold, bg=WHITE, fg=GREY, anchor="w",
                 justify="left", wraplength=220).grid(
            row=line, column=0, sticky="nw" if top else "w", pady=5, padx=(0, 12))

    def _build_form(self, card):
        for w in self.form_area.winfo_children():
            w.destroy()
        self.card_vars, self.card_texts, self.card_widgets = {}, {}, {}
        kind = card.get("type", "account")
        optional = OPTIONAL_FIELDS.get(kind, [])
        self._loading = True

        f = tk.Frame(self.form_area, bg=WHITE)
        f.pack(fill="both", expand=True)
        f.columnconfigure(1, weight=1)
        r = 0
        self._label(f, r, _("Name"))
        self.name_entry = self.text_entry(f, self._card_var("name", card.get("name", "")),
                                          self.f_title)
        self.name_entry.grid(row=r, column=1, columnspan=3, sticky="ew", pady=5, ipady=2)
        r += 1

        for field in FIELD_ORDER.get(kind, []):
            if field == "notes" or not field_visible(card, field):
                continue
            label = _(FIELD_LABELS[field])
            value = card.get(field, "")
            if field == "password":
                self._password_frame(f, r, value)
            elif field == "category":
                self._label(f, r, label)
                frame = tk.Frame(f, bg=WHITE)
                frame.grid(row=r, column=1, columnspan=2, sticky="w", pady=5)
                value_list = [no_category()] + self.book.category_names()
                selection = ttk.Combobox(frame, textvariable=self._card_var(
                    "category", value or no_category()), values=value_list,
                    font=self.f_base, state="readonly", width=18)
                selection.pack(side="left")
                self.category_badge = tk.Label(frame, text="   ", font=self.f_base,
                                               bg=self.book.category_color(value) or WHITE,
                                               relief="solid", bd=1 if value else 0)
                self.category_badge.pack(side="left", padx=(8, 0), ipadx=4)
                self.card_widgets[field] = selection
                self._remove_button(f, r, field)
            elif field == "address":
                self._label(f, r, label, top=True)
                area = self._card_text_area(f, field, value, 3)
                area.grid(row=r, column=1, sticky="ew", pady=5)
                b = self.button(f, _("Copy"), None)
                b.configure(command=lambda b=b: self.copy(
                    self.card_texts["address"].get("1.0", "end-1c"), b))
                b.grid(row=r, column=2, sticky="new", padx=(10, 0), pady=5)
                self.card_widgets[field] = area
                if field in optional:
                    self._remove_button(f, r, field)
            else:
                self._label(f, r, label)
                entry = self.text_entry(f, self._card_var(field, value))
                entry.grid(row=r, column=1, sticky="ew", pady=5, ipady=4)
                self.card_widgets[field] = entry
                if field == "site":
                    b = self.button(f, _("Open"), self.open_site)
                elif field == "birthday":
                    b = None
                else:
                    b = self.button(f, _("Copy"), None)
                    b.configure(command=lambda b=b, c=field: self.copy(
                        self.card_vars[c].get(), b))
                if b is not None:
                    b.grid(row=r, column=2, sticky="ew", padx=(10, 0), pady=5)
                if field in optional:
                    self._remove_button(f, r, field)
            r += 1

        # Fields added by hand (customer no., secret question…)
        for i, custom in enumerate(card.get("custom", [])):
            self._label(f, r, custom.get("label", "") or _("Field"))
            entry = self.text_entry(f, self._card_var("custom", custom.get("value", ""), i))
            entry.grid(row=r, column=1, sticky="ew", pady=5, ipady=4)
            self.card_widgets[("custom", i)] = entry
            b = self.button(f, _("Copy"), None)
            b.configure(command=lambda b=b, i=i: self.copy(self.card_vars[("custom", i)].get(), b))
            b.grid(row=r, column=2, sticky="ew", padx=(10, 0), pady=5)
            self._remove_button(f, r, "custom", i)
            r += 1

        self.button(f, _("＋  Add a field"), self.add_field, "blue_outline",
                    font=self.f_small).grid(row=r, column=1, sticky="w", pady=(4, 6))
        r += 1

        self._label(f, r, _("Notes"), top=True)
        notes = self._card_text_area(f, "notes", card.get("notes", ""), 4)
        notes.grid(row=r, column=1, columnspan=3, sticky="nsew", pady=5)
        f.rowconfigure(r, weight=1)
        r += 1

        source = card.get("source", "")
        tk.Label(f, text=(_("From the document: ") + Path(source).name) if source else "",
                 font=self.f_small, bg=WHITE, fg=GREY, anchor="w").grid(
            row=r, column=0, columnspan=4, sticky="w", pady=(4, 0))
        r += 1
        open_row = tk.Frame(f, bg=WHITE)
        open_row.grid(row=r, column=0, columnspan=4, sticky="w", pady=(4, 0))
        tk.Label(open_row, text=_("Open on the computer:"), font=self.f_small, bg=WHITE,
                 fg=GREY).pack(side="left", padx=(0, 8))
        self.button(open_row, _("The .txt copy"), lambda: self.open_card_file("txt"),
                    font=self.f_small).pack(side="left")
        if source:
            self.button(open_row, _("The original document"), lambda: self.open_card_file("source"),
                        font=self.f_small).pack(side="left", padx=(8, 0))
        self.button(open_row, _("The folder"), lambda: self.open_card_file("folder"),
                    font=self.f_small).pack(side="left", padx=(8, 0))
        r += 1
        self.button(f, _("Delete this contact") if kind == "contact" else _("Delete this card"),
                    self.delete_card, "danger").grid(row=r, column=1, columnspan=3,
                                                     sticky="e", pady=(10, 0))
        self._loading = False

        if self._focus_after is not None:
            widget = self.card_widgets.get(self._focus_after)
            self._focus_after = None
            if widget is not None:
                widget.focus_set()

    def _password_frame(self, f, r, value):
        frame = tk.Frame(f, bg=YELLOW_BG, padx=14, pady=10,
                         highlightthickness=2, highlightbackground=YELLOW_BORDER)
        frame.grid(row=r, column=0, columnspan=4, sticky="ew", pady=(12, 8))
        frame.columnconfigure(0, weight=1)
        tk.Label(frame, text=_("Password"), font=self.f_bold, bg=YELLOW_BG,
                 fg=YELLOW_TEXT, anchor="w").grid(row=0, column=0, sticky="w")
        # Password already saved: locked (avoids erasing it by mistake)
        locked = bool(value)
        entry_widget = tk.Entry(frame, textvariable=self._card_var("password", value), font=self.f_password,
                                bg=WHITE, fg=INK, relief="solid", bd=1, highlightthickness=2,
                                insertbackground=INK, highlightcolor="#E08A1E",
                                highlightbackground=YELLOW_BORDER, insertwidth=3,
                                readonlybackground=WHITE, state="readonly" if locked else "normal")
        entry_widget.grid(row=1, column=0, sticky="ew", pady=(6, 8), ipady=4)
        self.card_widgets["password"] = entry_widget
        buttons = tk.Frame(frame, bg=YELLOW_BG)
        buttons.grid(row=2, column=0, sticky="w")
        b = self.button(buttons, _("Copy"), None)
        b.configure(command=lambda: self.copy(self.card_vars["password"].get(), b))
        b.pack(side="left", padx=(0, 10))
        edit_button = self.button(buttons, _("✎  Edit by hand"), None)

        def toggle():
            if entry_widget.cget("state") == "readonly":
                entry_widget.configure(state="normal")
                entry_widget.focus_set()
                entry_widget.icursor("end")
                edit_button.configure(text=_("✔  Done"))
            else:
                entry_widget.configure(state="readonly")
                edit_button.configure(text=_("✎  Edit by hand"))

        edit_button.configure(command=toggle)
        if locked:
            edit_button.pack(side="left", padx=(0, 10))
        self.button(buttons, _("↻  Create a new password"),
                    self.open_generator, "blue").pack(side="left")

    # ------------------------------------------------------ changes in the card
    def _value_changed(self, key, value, custom_index=None):
        if self._loading:
            return
        card = self.book.find(self.current_id)
        if card is None:
            return
        if custom_index is not None:
            customs = card.get("custom", [])
            if custom_index < len(customs):
                customs[custom_index]["value"] = value
        else:
            if key == "category" and value == no_category():
                value = ""
            card[key] = value
            if key in ("name", "category"):
                self._update_list_row(card)
            if key == "category" and hasattr(self, "category_badge"):
                color = self.book.category_color(value)
                self.category_badge.configure(bg=color or WHITE, bd=1 if color else 0)
        card["modified_at"] = datetime.now().isoformat(timespec="seconds")
        card["edited_by_hand"] = True   # synchronization will not overwrite it
        self.schedule_save()

    def _text_changed(self, key):
        area = self.card_texts.get(key)
        if area is None or not area.edit_modified():
            return
        area.edit_modified(False)
        self._value_changed(key, area.get("1.0", "end-1c"))

    def _update_list_row(self, card):
        if card["id"] not in self.shown_ids:
            return
        i = self.shown_ids.index(card["id"])
        self.cards_list.delete(i)
        self.cards_list.insert(i, "  " + (card["name"] or _("Untitled")))
        self._color_row(i, card)
        self.cards_list.selection_set(i)

    def _color_row(self, i, card):
        color = self.book.category_color(card.get("category", ""))
        if color:
            self.cards_list.itemconfig(i, background=color, foreground=TEXT_ON_PASTEL)
        else:
            self.cards_list.itemconfig(i, background=WHITE, foreground=INK)

    def add_field(self):
        card = self.book.find(self.current_id)
        if card is None:
            return
        kind = card.get("type", "account")
        missing = [c for c in OPTIONAL_FIELDS.get(kind, []) if not field_visible(card, c)]

        f = tk.Toplevel(self.root)
        f.title(_("Add a field"))
        f.configure(bg=WHITE, padx=24, pady=18)
        f.transient(self.root)
        f.resizable(False, False)
        tk.Label(f, text=_("Which field should be added to this card?"), font=self.f_bold,
                 bg=WHITE, fg=INK).pack(anchor="w", pady=(0, 10))

        def add_standard(field):
            card.setdefault("added_fields", []).append(field)
            self._focus_after = field
            f.destroy()
            self.show_card(card)
            self.schedule_save()

        if missing:
            line = tk.Frame(f, bg=WHITE)
            line.pack(anchor="w", pady=(0, 12))
            for field in missing:
                self.button(line, _(FIELD_LABELS[field]),
                            lambda c=field: add_standard(c)).pack(side="left", padx=(0, 8))

        tk.Label(f, text=_("Or another field, with your own name (e.g. Customer number, Secret question):"),
                 font=self.f_small, bg=WHITE, fg=GREY).pack(anchor="w")
        name_var = tk.StringVar()
        entry_widget = self.text_entry(f, name_var)
        entry_widget.pack(fill="x", ipady=4, pady=(4, 12))

        def add_custom(_event=None):
            name = name_var.get().strip()
            if not name:
                entry_widget.focus_set()
                return
            card.setdefault("custom", []).append({"label": name, "value": ""})
            self._focus_after = ("custom", len(card["custom"]) - 1)
            f.destroy()
            self.show_card(card)
            self.schedule_save()

        entry_widget.bind("<Return>", add_custom)
        buttons = tk.Frame(f, bg=WHITE)
        buttons.pack(fill="x")
        self.button(buttons, _("Cancel"), f.destroy).pack(side="right")
        self.button(buttons, _("＋  Add this field"), add_custom, "blue").pack(side="right", padx=10)
        f.grab_set()
        entry_widget.focus_set()

    def remove_field(self, key, custom_index=None):
        card = self.book.find(self.current_id)
        if card is None:
            return
        if custom_index is not None:
            customs = card.get("custom", [])
            if custom_index >= len(customs):
                return
            label, value = customs[custom_index].get("label", ""), customs[custom_index].get("value", "")
        else:
            label, value = _(FIELD_LABELS.get(key, key)), card.get(key, "")
        if value and not messagebox.askyesno(
                _("Remove the field?"),
                _("Remove “{field}” from this card?\n\nWhat is written in it will be erased:",
                  field=label) + "\n" + value,
                icon="warning", default="no"):
            return
        if custom_index is not None:
            del card["custom"][custom_index]
        else:
            card[key] = ""
            if key in card.get("added_fields", []):
                card["added_fields"].remove(key)
            if key == "category":
                self._update_list_row(card)
        card["modified_at"] = datetime.now().isoformat(timespec="seconds")
        card["edited_by_hand"] = True   # synchronization will not overwrite it
        self.show_card(card)
        self.schedule_save()

    # ---------------------------------------------------------- settings page
    def _section_card(self, parent, title_text, explanation=""):
        card_frame = tk.Frame(parent, bg=WHITE, padx=20, pady=16,
                              highlightthickness=2, highlightbackground=BORDER)
        tk.Label(card_frame, text=title_text, font=self.f_title, bg=WHITE, fg=INK,
                 anchor="w").pack(fill="x")
        if explanation:
            tk.Label(card_frame, text=explanation, font=self.f_small, bg=WHITE, fg=GREY,
                     anchor="w", justify="left", wraplength=520).pack(fill="x", pady=(2, 10))
        return card_frame

    def _settings_page(self):
        p = self.settings_page = tk.Frame(self.center, bg=BG, padx=16, pady=12)

        left_column = tk.Frame(p, bg=BG)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 16))

        # --- About (bottom left)
        about = self._section_card(left_column, _("About"),
                                   _("Pocket Book {version} — works entirely without internet: "
                                     "nothing leaves this computer.", version=VERSION))
        about.pack(side="bottom", fill="x", pady=(16, 0))
        tk.Label(about, text=_("Your data is here:") + f"\n{DATA_FOLDER}", font=self.f_small,
                 bg=WHITE, fg=INK, anchor="w", justify="left", wraplength=520).pack(fill="x")
        about_row = tk.Frame(about, bg=WHITE)
        about_row.pack(fill="x", pady=(10, 0))
        self.button(about_row, _("Open the data folder"),
                    lambda: open_with_system(DATA_FOLDER)).pack(side="left")
        if can_install() and same_file(sys.executable, install_paths()["exe"]):
            self.button(about_row, _("Uninstall…"), self.uninstall_from_settings,
                        "danger").pack(side="right")

        # --- Categories
        cat = self._section_card(left_column, _("Categories"),
                                 _("Categories are used to sort cards. Each one has its own colour, "
                                   "shown in the list of cards."))
        cat.pack(side="top", fill="both", expand=True)
        frame = tk.Frame(cat, bg=WHITE)
        frame.pack(fill="both", expand=True)
        self.category_list = tk.Listbox(
            frame, font=self.f_base, activestyle="none", height=10,
            bg=WHITE, fg=INK, selectbackground=BLUE, selectforeground=ON_ACCENT,
            relief="solid", bd=1, highlightthickness=0, exportselection=False)
        bar = ttk.Scrollbar(frame, orient="vertical", command=self.category_list.yview)
        self.category_list.configure(yscrollcommand=bar.set)
        self.category_list.pack(side="left", fill="both", expand=True)
        bar.pack(side="right", fill="y")
        buttons = tk.Frame(cat, bg=WHITE)
        buttons.pack(fill="x", pady=(10, 0))
        self.button(buttons, _("＋  New"), self.new_category, "blue").pack(side="left")
        self.button(buttons, _("Rename"), self.rename_category).pack(side="left", padx=(8, 0))
        self.button(buttons, _("Colour…"), self.category_color).pack(side="left", padx=(8, 0))
        self.button(buttons, _("Delete"), self.delete_category, "danger").pack(side="right")

        right = tk.Frame(p, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        # --- Language
        language = self._section_card(right, _("Language"))
        language.pack(fill="x", pady=(0, 16))
        languages_row = tk.Frame(language, bg=WHITE)
        languages_row.pack(fill="x")
        for code, name in LANGUAGES.items():
            active = code == current_language()
            tk.Button(languages_row, text=("✔ " if active else "") + name, font=self.f_bold,
                      bg=BLUE if active else WHITE, fg=ON_ACCENT if active else INK,
                      activebackground=BLUE_DARK if active else BLUE_LIGHT,
                      activeforeground=ON_ACCENT if active else INK, relief="solid", bd=1,
                      padx=10, pady=6, cursor="hand2", highlightthickness=0,
                      command=lambda c=code: self.choose_interface_language(c)).pack(
                side="left", padx=(0, 6), pady=2)

        # --- Themes
        theme = self._section_card(right, _("Screen colours"),
                                   _("Choose whatever is easiest to read."))
        theme.pack(fill="x")
        grid_frame = tk.Frame(theme, bg=WHITE)
        grid_frame.pack(fill="x")
        current = self.book.settings.get("theme", "light")
        for i, (key, t) in enumerate(THEMES.items()):
            active = key == current
            b = tk.Button(grid_frame, text=("✔  " if active else "") + _(t["name"]), font=self.f_bold,
                          bg=t["BG"], fg=t["INK"], activebackground=t["WHITE"],
                          activeforeground=t["INK"], relief="solid", bd=4 if active else 1,
                          padx=14, pady=12, cursor="hand2", highlightthickness=0,
                          command=lambda c=key: self.choose_theme(c))
            b.grid(row=i // 2, column=i % 2, sticky="ew", padx=4, pady=4)
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # --- .txt copy
        txt = self._section_card(right, _("Copy of cards as .txt"),
                                 _("Each card is copied into a .txt file that updates itself. Make "
                                   "changes in the notebook, not in the .txt files."))
        txt.pack(fill="x", pady=(16, 0))
        self.txt_label = tk.Label(txt, text="", font=self.f_small, bg=WHITE, fg=INK,
                                  anchor="w", justify="left", wraplength=520)
        self.txt_label.pack(fill="x")
        line = tk.Frame(txt, bg=WHITE)
        line.pack(fill="x", pady=(10, 0))
        self.button(line, _("Change folder…"), self.choose_txt_folder).pack(side="left")
        self.button(line, _("Open the folder"), self.open_txt_folder).pack(side="left", padx=8)

    def uninstall_from_settings(self):
        self.save()
        if uninstall_window(self.root):
            self.root.destroy()

    def fill_categories(self, choose=None):
        self.category_list.delete(0, "end")
        for i, c in enumerate(self.book.categories()):
            n = self.book.category_card_count(c["name"])
            self.category_list.insert("end", f"  {c['name']}   (" + n_(n, "{n} card", "{n} cards") + ")")
            self.category_list.itemconfig(i, background=c.get("color") or WHITE,
                                          foreground=TEXT_ON_PASTEL if c.get("color") else INK)
            if c["name"] == choose:
                self.category_list.selection_set(i)
                self.category_list.see(i)

    def _selected_category(self):
        selection = self.category_list.curselection()
        if not selection:
            messagebox.showinfo(APP_NAME, _("First click on a category in the list."))
            return None
        return self.book.categories()[selection[0]]["name"]

    def _categories_changed(self, choose=None):
        self.fill_categories(choose)
        self.schedule_save()

    def new_category(self):
        name = ask_text(self, _("New category"), _("Name of the new category:"))
        if name is None:
            return
        if not self.book.add_category(name):
            messagebox.showinfo(APP_NAME, _("The category “{name}” already exists.", name=name.strip()))
            return
        self._categories_changed(name.strip())

    def rename_category(self):
        old = self._selected_category()
        if old is None:
            return
        new = ask_text(self, _("Rename the category"), _("New name:"), old)
        if new is None or new.strip() == old:
            return
        if not self.book.rename_category(old, new):
            messagebox.showinfo(APP_NAME, _("The category “{name}” already exists.", name=new.strip()))
            return
        self._categories_changed(new.strip())

    def category_color(self):
        name = self._selected_category()
        if name is None:
            return
        color = choose_color(self, name)
        if color is None:
            return
        for c in self.book.categories():
            if c["name"] == name:
                c["color"] = color
        self._categories_changed(name)

    def delete_category(self):
        name = self._selected_category()
        if name is None:
            return
        n = self.book.category_card_count(name)
        text_value = _("Delete the category “{name}”?", name=name)
        if n:
            text_value += "\n\n" + n_(n, "{n} card will no longer have a category (the card itself is not deleted).",
                                      "{n} cards will no longer have a category (the cards themselves are not deleted).")
        if not messagebox.askyesno(_("Delete the category?"), text_value, icon="warning", default="no"):
            return
        self.book.delete_category(name)
        self._categories_changed()

    def choose_interface_language(self, code):
        if code == current_language():
            return
        set_language(code)
        self.book.settings["language"] = code
        self._rebuild()
        self.schedule_save()  # the .txt copies are rewritten in the new language

    def choose_theme(self, key):
        if key == self.book.settings.get("theme", "light"):
            return
        self.book.settings["theme"] = key
        apply_theme_colors(key)
        self._rebuild()
        self.schedule_save()

    def _rebuild(self):
        """Redraw the whole window (after a theme change)."""
        page = self.page
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=BG)
        self._style()
        self._build()
        self.apply_size(self.book.settings.get("text_size", 1), save=False)
        self._show_folder()
        self.show_page(page)

    # --------------------------------------------------------- documents page
    def _documents_page(self):
        p = self.documents_page = tk.Frame(self.center, bg=BG, padx=16, pady=12)

        top = tk.Frame(p, bg=BG)
        top.pack(fill="x", pady=(0, 8))
        self.folder_label = tk.Label(top, text="", font=self.f_base, bg=BG,
                                     fg=INK, anchor="w", justify="left")
        self.folder_label.pack(fill="x")
        self.doc_buttons_area = tk.Frame(p, bg=BG)
        self.doc_buttons_area.pack(fill="x", pady=(0, 4))
        doc_buttons = [
            self.button(self.doc_buttons_area, _("↻  Sync now"),
                        self.sync_now, "green"),
            self.button(self.doc_buttons_area, _("Choose the folder…"), self.choose_folder),
            self.button(self.doc_buttons_area, _("Import files…"),
                        self.choose_files_to_import),
        ]
        self.doc_buttons_area.bind("<Configure>", lambda e: self._wrap_in_rows(
            self.doc_buttons_area, doc_buttons, gap=4))
        self.sync_var = tk.BooleanVar(value=bool(self.book.settings.get("auto_sync", True)))
        tk.Checkbutton(p, text=_("File the documents in this folder automatically (new and "
                                 "changed ones), at every start and every minute"),
                       variable=self.sync_var, command=self._auto_sync_changed,
                       font=self.f_small, bg=BG, fg=INK, activebackground=BG,
                       activeforeground=INK, selectcolor=WHITE, anchor="w",
                       justify="left").pack(fill="x", pady=(0, 8))

        filters = tk.Frame(p, bg=BG)
        filters.pack(fill="x", pady=(0, 8))
        tk.Label(filters, text=_("Show:"), font=self.f_bold, bg=BG, fg=GREY).pack(
            side="left", anchor="n", pady=(8, 0))
        filters_area = tk.Frame(filters, bg=BG)
        filters_area.pack(side="left", fill="x", expand=True, padx=(4, 0))
        # By default: only what is left to file (the rest is already in the book)
        self.kind_filter = getattr(self, "kind_filter", "to_file")
        self.filter_buttons = {}
        for kind, text_value in (("to_file", _("To file")), ("all", _("All")),
                                 ("account", _("Passwords")), ("contact", _("Contacts")),
                                 ("other", _("Not recognised"))):
            self.filter_buttons[kind] = self.button(filters_area, text_value,
                                                    lambda g=kind: self.choose_filter(g))
        filters_area.bind("<Configure>", lambda e: self._wrap_in_rows(
            filters_area, list(self.filter_buttons.values()), gap=4))

        body = tk.Frame(p, bg=BG)
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="y", padx=(0, 16))
        tk.Label(left, text=_("Search in the documents"), font=self.f_bold,
                 bg=BG, fg=INK, anchor="w").pack(fill="x")
        self.docs_search_var = tk.StringVar()
        self.docs_search_var.trace_add("write", lambda *a: self._docs_search_changed())
        self.text_entry(left, self.docs_search_var).pack(fill="x", ipady=4, pady=(2, 6))
        self.docs_count_label = tk.Label(left, text="", font=self.f_small,
                                         bg=BG, fg=GREY, anchor="w", justify="left")
        self.docs_count_label.pack(fill="x")
        list_frame = tk.Frame(left, bg=BG)
        list_frame.pack(fill="both", expand=True, pady=6)
        self.docs_list = tk.Listbox(
            list_frame, font=self.f_base, width=32, activestyle="none",
            bg=WHITE, fg=INK, selectbackground=BLUE, selectforeground=ON_ACCENT,
            relief="solid", bd=1, highlightthickness=0, exportselection=False)
        bar = ttk.Scrollbar(list_frame, orient="vertical", command=self.docs_list.yview)
        self.docs_list.configure(yscrollcommand=bar.set)
        self.docs_list.pack(side="left", fill="both", expand=True)
        bar.pack(side="right", fill="y")
        self.docs_list.bind("<<ListboxSelect>>", lambda e: self._document_selected())

        right = tk.Frame(body, bg=WHITE, padx=22, pady=16,
                         highlightthickness=2, highlightbackground=BORDER)
        right.pack(side="left", fill="both", expand=True)
        self.doc_title = tk.Label(right, text=_("Choose a document in the list."),
                                  font=self.f_title, bg=WHITE, fg=INK, anchor="w",
                                  justify="left")
        self.doc_title.pack(fill="x")
        self.doc_kind = tk.Label(right, text=_("This document is never changed by the notebook."),
                                 font=self.f_small, bg=WHITE, fg=GREY, anchor="w")
        self.doc_kind.pack(fill="x", pady=(2, 8))
        buttons = tk.Frame(right, bg=WHITE)
        buttons.pack(side="bottom", fill="x", pady=(10, 0))
        self.doc_card_button = self.button(buttons, _("＋  Create a card from this document"),
                                           self.card_from_document, "blue")
        self.doc_card_button.pack(side="left")
        self.button(buttons, _("Open in Word"), self.open_document).pack(side="left", padx=10)

        # "What the book understood": the document reformatted, field by field
        self.understood_frame = tk.Frame(right, bg=YELLOW_BG, padx=14, pady=10,
                                         highlightthickness=2, highlightbackground=YELLOW_BORDER)
        self.understood_frame.pack(fill="x", pady=(0, 10))
        tk.Label(right, text=_("Document text:"), font=self.f_small, bg=WHITE, fg=GREY,
                 anchor="w").pack(fill="x")

        text_frame = tk.Frame(right, bg=WHITE)
        text_frame.pack(fill="both", expand=True)
        self.doc_text = tk.Text(text_frame, font=self.f_base, wrap="word", bg=TEXT_BG,
                                fg=INK, relief="solid", bd=1, padx=12, pady=10,
                                highlightthickness=0, state="disabled")
        txt_bar = ttk.Scrollbar(text_frame, orient="vertical", command=self.doc_text.yview)
        self.doc_text.configure(yscrollcommand=txt_bar.set)
        self.doc_text.pack(side="left", fill="both", expand=True)
        txt_bar.pack(side="right", fill="y")
        self.doc_text.tag_configure("match", background="#FFE08A", foreground=TEXT_ON_PASTEL)

    # ------------------------------------------------------------ navigation
    def show_page(self, page):
        self.page = page
        self.cards_page.pack_forget()
        self.documents_page.pack_forget()
        self.settings_page.pack_forget()
        # The letter bar is not used in the settings
        if page == "settings":
            self.letter_bar.pack_forget()
            self.letter_separator.pack_forget()
        elif not self.letter_bar.winfo_ismapped():
            self.letter_bar.pack(fill="x", before=self.center)
            self.letter_separator.pack(fill="x", before=self.center)
        if page == "documents":
            self.documents_page.pack(fill="both", expand=True)
        elif page == "settings":
            self.settings_page.pack(fill="both", expand=True)
        else:
            self.cards_page.pack(fill="both", expand=True)
            contact = page == "contact"
            self.search_title.configure(text=_("Search for a contact") if contact
                                        else _("Search for a card"))
            self.new_button.configure(text=_("＋  New contact") if contact
                                      else _("＋  New card"))
            self.no_card.configure(
                text=(_("No contact is selected.\n\n") if contact else
                      _("No card is selected.\n\n"))
                + _("• Click a name in the list on the left,\n")
                + (_("• or on “New contact” to create one.") if contact else
                   _("• or on “New card” to create one."))
                + _("\n\nTip: drag .docx or .txt files (or a whole folder)\nfrom your file "
                    "manager onto this window to file them all at once."))
            if self.search_var.get():
                self.search_var.set("")
            if self.category_filter_var.get() != all_categories():
                self.category_filter_var.set(all_categories())
        for name, b in self.tabs.items():
            active = name == page
            b.configure(bg=BLUE if active else WHITE, fg=ON_ACCENT if active else INK,
                        activebackground=BLUE_DARK if active else BLUE_LIGHT,
                        activeforeground=ON_ACCENT if active else INK)
        self.letter = "All"
        self.refresh()

    def refresh(self):
        if self.page == "documents":
            self.fill_docs_list()
        elif self.page == "settings":
            self.fill_categories()
            self._show_txt_folder()
        else:
            self.fill_cards_list()

    def choose_letter(self, letter):
        # A letter clears the search, so the two don't mix.
        var = self.docs_search_var if self.page == "documents" else self.search_var
        if var.get():
            var.set("")
        self.letter = letter
        self.refresh()

    def _color_letters(self, letters_present):
        for letter, b in self.letter_buttons.items():
            active = letter == self.letter
            present = letter == "All" or letter in letters_present
            if active:
                b.configure(bg=BLUE, fg=ON_ACCENT, activebackground=BLUE_DARK,
                            activeforeground=ON_ACCENT, state="normal", cursor="hand2")
            elif present:
                b.configure(bg=WHITE, fg=INK, activebackground=BLUE_LIGHT,
                            activeforeground=INK, state="normal", cursor="hand2")
            else:
                b.configure(bg=BAR, fg=LETTER_OFF, state="disabled",
                            disabledforeground=LETTER_OFF, cursor="arrow")

    # --------------------------------------------------------------- text size
    def apply_size(self, level, save=True):
        level = max(0, min(len(SIZES) - 1, int(level)))
        t = SIZES[level]
        self.f_base.configure(size=t)
        self.f_bold.configure(size=t)
        self.f_small.configure(size=max(t - 2, 11))
        self.f_title.configure(size=t + 6)
        self.f_password.configure(size=t + 6)
        self.f_letter.configure(size=t - 1)
        for i, b in enumerate(self.size_buttons):
            active = i == level
            b.configure(bg=BLUE if active else WHITE, fg=ON_ACCENT if active else INK,
                        activebackground=BLUE_DARK if active else BLUE_LIGHT,
                        activeforeground=ON_ACCENT if active else INK)
        self.root.after(20, self._place_letters)
        self.root.after(20, lambda: self._wrap_in_rows(
            self.tabs_area, list(self.tabs.values()), gap=6))
        if save and self.book.settings.get("text_size") != level:
            self.book.settings["text_size"] = level
            self.schedule_save()

    # -------------------------------------------------------------- card list
    def _cards_search_changed(self):
        if self.search_var.get():
            self.letter = "All"
        if self.page in ("account", "contact"):
            self.fill_cards_list()

    def fill_cards_list(self):
        kind = self.page
        search = normalize(self.search_var.get().strip())
        all_cards = sorted((f for f in self.book.cards if f.get("type", "account") == kind),
                           key=lambda f: sort_key(f["name"]))
        found_cards = [f for f in all_cards if card_matches(f, search)]
        cat_names = self.book.category_names()
        self.category_filter_choice.configure(values=[all_categories()] + cat_names + [no_category()])
        filter_fn = self.category_filter_var.get()
        if filter_fn not in [all_categories(), no_category()] + cat_names:
            filter_fn = all_categories()
            self.category_filter_var.set(filter_fn)
        if filter_fn == no_category():
            found_cards = [f for f in found_cards if not f.get("category")]
        elif filter_fn != all_categories():
            found_cards = [f for f in found_cards if f.get("category") == filter_fn]
        self._color_letters({first_letter(f["name"]) for f in found_cards})
        if self.letter != "All":
            found_cards = [f for f in found_cards if first_letter(f["name"]) == self.letter]

        self.cards_list.delete(0, "end")
        self.shown_ids = []
        for i, card in enumerate(found_cards):
            self.cards_list.insert("end", "  " + (card["name"] or _("Untitled")))
            self._color_row(i, card)
            self.shown_ids.append(card["id"])
        if self.current_id in self.shown_ids:
            i = self.shown_ids.index(self.current_id)
            self.cards_list.selection_set(i)
            self.cards_list.see(i)

        n = len(found_cards)
        if kind == "contact":
            text_value = n_(n, "{n} contact", "{n} contacts")
            if search:
                text_value = n_(n, "{n} contact found", "{n} contacts found")
        else:
            text_value = n_(n, "{n} card", "{n} cards")
            if search:
                text_value = n_(n, "{n} card found", "{n} cards found")
        if not search:
            text_value += _(", from A to Z") if self.letter == "All" else _(" starting with {letter}", letter=self.letter)
        if filter_fn != all_categories():
            text_value += f" — {filter_fn}"
        self.count_label.configure(text=text_value)
        self.show_card(self.book.find(self.current_id))

    def _card_selected(self):
        selection = self.cards_list.curselection()
        if not selection:
            return
        self.current_id = self.shown_ids[selection[0]]
        self.show_card(self.book.find(self.current_id))

    def show_card(self, card):
        if card is None or card.get("type", "account") != self.page:
            self.form_area.pack_forget()
            self.no_card.pack(anchor="nw")
            return
        self.no_card.pack_forget()
        self.form_area.pack(fill="both", expand=True)
        self._build_form(card)

    def create_card(self):
        kind = self.page if self.page in ("account", "contact") else "account"
        card = self.book.new_card(type=kind)
        self.current_id = card["id"]
        if self.search_var.get():
            self.search_var.set("")
        self.letter = "All"
        self.fill_cards_list()
        self.schedule_save()
        # Offer to type the name right away.
        if self.name_entry is not None:
            self.name_entry.focus_set()
            self.name_entry.select_range(0, "end")

    def delete_card(self):
        card = self.book.find(self.current_id)
        if card is None:
            return
        if card.get("type") == "contact":
            question = _("Do you really want to delete the contact “{name}”?", name=card["name"])
        else:
            question = _("Do you really want to delete the card “{name}”?", name=card["name"])
        if not messagebox.askyesno(
                _("Delete?"),
                question + "\n\n" + _("A copy stays in today's backups."),
                icon="warning", default="no"):
            return
        self.book.delete(card["id"])
        self.current_id = None
        self.fill_cards_list()
        self.schedule_save()

    # ------------------------------------------------------------ small helpers
    def copy(self, text_value, button=None):
        if not text_value:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text_value)
        self.root.update()
        if button is not None:
            old = button.cget("text")
            if not old.startswith("✔"):
                button.configure(text=_("✔ Copied"))
                self.root.after(1500, lambda: button.configure(text=old))

    def open_site(self):
        address = self.card_vars["site"].get().strip() if "site" in self.card_vars else ""
        if not address:
            messagebox.showinfo(_("Website"), _("No website address is written on this card."))
            return
        if not re.match(r"^https?://", address, re.IGNORECASE):
            address = "https://" + address
        webbrowser.open(address)

    # ---------------------------------------------------------------- generator
    def open_generator(self):
        card = self.book.find(self.current_id)
        if card is None:
            return
        if card.get("password") and not messagebox.askyesno(
                _("Change the password?"),
                _("Do you really want to change the password for “{name}”?\n\nCareful: this only "
                  "changes the notebook. You must also change it on the website itself, "
                  "otherwise you will no longer be able to log in.\n\n(The old password will be "
                  "kept in the notes.)", name=card.get("name", "")),
                icon="warning", default="no"):
            return
        GeneratorWindow(self)

    def replace_password(self, new):
        card = self.book.find(self.current_id)
        if card is None:
            return
        old = card.get("password", "")
        if old and old != new:
            date = datetime.now().strftime(_("%m/%d/%Y"))
            note = _("Old password (replaced on {date}): {old}", date=date, old=old)
            notes = card.get("notes", "").rstrip()
            card["notes"] = (notes + "\n" + note).strip()
        card["password"] = new
        card["modified_at"] = datetime.now().isoformat(timespec="seconds")
        card["edited_by_hand"] = True   # synchronization will not overwrite it
        self.show_card(card)
        self.schedule_save()

    # --------------------------------------------------------------------- save
    def schedule_save(self):
        self.status_label.configure(text=_("✎ Editing…"), fg=GREY)
        if self._timer is not None:
            self.root.after_cancel(self._timer)
        self._timer = self.root.after(800, self.save)

    def save(self):
        self._timer = None
        copy_ok = self.book.sync_txt()  # the .txt files first (updates their list)
        try:
            self.book.save()
        except Exception as exc:
            self.status_label.configure(text=_("⚠ Could not save!"), fg=RED)
            messagebox.showerror(
                _("Saving problem"),
                _("The notebook could not be saved.\n\n") + str(exc))
            return False
        time_str = datetime.now().strftime("%H:%M")
        if copy_ok:
            self.status_label.configure(text=_("✔ Everything is saved ({time_str})", time_str=time_str), fg=GREEN_TEXT)
            self._txt_alert_shown = False
        else:
            # The book is saved; only the .txt copy failed (USB stick removed…).
            self.status_label.configure(
                text=_("✔ Saved ({time_str}) — ⚠ .txt copy failed", time_str=time_str), fg=RED)
            if not self._txt_alert_shown:
                self._txt_alert_shown = True
                messagebox.showwarning(
                    APP_NAME, _("The notebook is saved, but the .txt copy of the cards could "
                                "not be made.\n\nThe folder may be disconnected (USB stick, "
                                "network drive).\n\n") + self.book.txt_message)
        return True

    def save_now(self):
        if self._timer is not None:
            self.root.after_cancel(self._timer)
            self._timer = None
        if self.save():
            try:
                self.book.daily_backup()
            except OSError:
                pass

    def quit_app(self):
        if self._timer is not None:
            self.root.after_cancel(self._timer)
        if not self.save():
            if not messagebox.askyesno(_("Close anyway?"),
                                       _("The notebook could not be saved.\nClose anyway?"), default="no"):
                return
        self.root.destroy()

    # ---------------------------------------------------------------- documents
    def _after_opening(self):
        if self.book.recovery_message:
            messagebox.showwarning(APP_NAME, self.book.recovery_message)
        if BOOK_FILE.exists():
            self.status_label.configure(text=_("✔ Everything is saved"), fg=GREEN_TEXT)
        folder = self.book.settings.get("documents_folder", "")
        self._show_folder()
        if self.book.cards:
            self.save()  # create any missing .txt files
        if folder and os.path.isdir(folder):
            self.start_reading()

    def _show_txt_folder(self):
        folder = self.book.settings.get("txt_folder", "")
        self.txt_label.configure(
            text=(_("Copy of each card as .txt, updated automatically, in:\n") + folder)
            if folder else _("Copy of cards as .txt: turned off."))

    def choose_txt_folder(self):
        folder = filedialog.askdirectory(
            title=_("Which folder should hold the .txt copy of the cards?"),
            initialdir=self.book.settings.get("txt_folder") or str(DATA_FOLDER))
        if not folder:
            return
        folder = os.path.normpath(folder)
        docs = self.book.settings.get("documents_folder", "")
        if docs and os.path.normcase(folder) == os.path.normcase(os.path.normpath(docs)):
            messagebox.showwarning(
                APP_NAME, _("Choose a folder other than the one with the original "
                            "documents\n(for example a “Cards as text” subfolder)."))
            return
        self.book.change_txt_folder(folder)
        self._show_txt_folder()
        self.save()
        messagebox.showinfo(APP_NAME, _("The .txt copy of the cards is now in:\n") + folder
                            + _("\n\nThe old folder has not been changed."))

    def open_card_file(self, what):
        """Open the card's .txt copy, its source document, or the folder (file selected)."""
        card = self.book.find(self.current_id)
        if card is None:
            return
        if what == "source":
            path = card.get("source", "")
        else:
            self.save()  # the .txt copy must be up to date before opening it
            rel = card.get("txt_file", "")
            path = str(Path(self.book.settings.get("txt_folder", "")) / rel) if rel else ""
        if not path or not os.path.exists(path):
            messagebox.showinfo(APP_NAME, _("This file does not exist (or no longer exists) on the computer."))
            return
        try:
            if what == "folder":
                show_in_folder(path)
            else:
                open_with_system(path)
        except OSError as exc:
            messagebox.showerror(APP_NAME, _("The file could not be opened.\n\n") + str(exc))

    def open_txt_folder(self):
        folder = self.book.settings.get("txt_folder", "")
        if not folder:
            return
        Path(folder).mkdir(parents=True, exist_ok=True)
        try:
            open_with_system(folder)
        except OSError as exc:
            messagebox.showerror(APP_NAME, _("The folder could not be opened.\n\n") + str(exc))

    def _show_folder(self):
        self._show_txt_folder()
        folder = self.book.settings.get("documents_folder", "")
        if folder:
            self.folder_label.configure(text=_("Documents folder:\n") + folder)
        else:
            self.folder_label.configure(
                text=_("No folder chosen. Click “Choose the folder…”."))

    def choose_folder(self):
        folder = filedialog.askdirectory(
            title=_("Where are your documents kept?"),
            initialdir=self.book.settings.get("documents_folder") or str(Path.home()))
        if not folder:
            return
        self.book.settings["documents_folder"] = os.path.normpath(folder)
        self.schedule_save()
        self._show_folder()
        self.start_reading()

    def start_reading(self):
        folder = self.book.settings.get("documents_folder", "")
        if not folder or not os.path.isdir(folder):
            messagebox.showinfo(APP_NAME, _("First choose the folder where your documents are kept."))
            return
        if self.reading_in_progress:
            return
        self.reading_in_progress = True
        self.docs_count_label.configure(text=_("Reading documents…"))
        old = self.index

        def work():
            try:
                result = index_documents(folder, old,
                                         lambda i, n: self.message_queue.put(("progress", i, n)),
                                         exclude=[self.book.settings.get("txt_folder", "")])
                try:
                    write_json_safely(INDEX_FILE, result)
                except OSError:
                    pass
                self.message_queue.put(("done", result))
            except Exception as exc:
                self.message_queue.put(("error", str(exc)))

        threading.Thread(target=work, daemon=True).start()
        self.root.after(100, self._follow_reading)

    def _follow_reading(self):
        try:
            while True:
                message = self.message_queue.get_nowait()
                if message[0] == "progress":
                    _type, i, n = message
                    self.docs_count_label.configure(
                        text=_("Reading documents: {i} of {n}…", i=i, n=n))
                elif message[0] == "done":
                    self.index = message[1]
                    self.reading_in_progress = False
                    request = self._sync_requested
                    self._sync_requested = False
                    if request or self.book.settings.get("auto_sync", True):
                        self._apply_sync(show_summary=request)
                    if self.page == "documents":
                        self.fill_docs_list()
                    else:
                        self._count_docs()
                    return
                elif message[0] == "error":
                    self.reading_in_progress = False
                    self.docs_count_label.configure(text=_("Reading failed."))
                    messagebox.showerror(APP_NAME, _("The documents could not be read.\n\n") + message[1])
                    return
        except queue.Empty:
            pass
        self.root.after(100, self._follow_reading)

    # ------------------------------------------------------- synchronization
    def _apply_sync(self, show_summary=False):
        documents = self._documents()
        if not documents:
            return
        summary = self.book.sync_documents(documents, self._keep_categories)
        total = summary["created"] + summary["updated"] + summary["to_check"]
        if total:
            self.save()
            if self.page in ("account", "contact"):
                self.fill_cards_list()
        parts = []
        if summary["created"]:
            parts.append(n_(summary["created"], "{n} card created", "{n} cards created"))
        if summary["updated"]:
            parts.append(n_(summary["updated"], "{n} card updated", "{n} cards updated"))
        if summary["to_check"]:
            parts.append(n_(summary["to_check"], "{n} to check (⚠ in the notes)",
                            "{n} to check (⚠ in the notes)"))
        if parts:
            time_str = datetime.now().strftime("%H:%M")
            self.sync_label.configure(
                text=_("↻ Documents synced at {time_str}: ", time_str=time_str) + ", ".join(parts))
        if show_summary:
            messagebox.showinfo(
                _("Sync"),
                (_("From the documents:\n\n   • ") + "\n   • ".join(parts)) if parts
                else _("Everything is already up to date: no card to create or change."))

    def sync_now(self):
        folder = self.book.settings.get("documents_folder", "")
        if not folder or not os.path.isdir(folder):
            messagebox.showinfo(APP_NAME, _("First choose the folder where your documents are kept."))
            return
        self._sync_requested = True
        self.start_reading()

    def _auto_sync_changed(self):
        self.book.settings["auto_sync"] = bool(self.sync_var.get())
        self.schedule_save()
        if self.sync_var.get():
            self.sync_now()

    def _periodic_sync(self):
        """Every minute: rescan the folder (only changed files are read again)."""
        folder = self.book.settings.get("documents_folder", "")
        if (self.book.settings.get("auto_sync", True) and folder
                and os.path.isdir(folder) and not self.reading_in_progress):
            self.start_reading()
        self.root.after(60000, self._periodic_sync)

    def _documents(self):
        return self.index.get("documents", {}) if self.index.get(
            "folder") == self.book.settings.get("documents_folder") else {}

    def _count_docs(self):
        n = len(self._documents())
        self.docs_count_label.configure(text=n_(n, "{n} document", "{n} documents"))

    def _docs_search_changed(self):
        if self.docs_search_var.get():
            self.letter = "All"
        if self._search_timer is not None:
            self.root.after_cancel(self._search_timer)
        self._search_timer = self.root.after(250, self.fill_docs_list)

    def choose_filter(self, kind):
        self.kind_filter = kind
        self.fill_docs_list()

    def fill_docs_list(self):
        self._search_timer = None
        for kind, b in self.filter_buttons.items():
            active = kind == self.kind_filter
            b.configure(bg=BLUE if active else WHITE, fg=ON_ACCENT if active else INK,
                        activebackground=BLUE_DARK if active else BLUE_LIGHT,
                        activeforeground=ON_ACCENT if active else INK)
        documents = self._documents()
        search = normalize(self.docs_search_var.get().strip())
        entries = sorted(documents.items(), key=lambda kv: sort_key(kv[1]["name"]))
        already = self.book.known_sources()
        all_documents = len(entries)
        if self.kind_filter == "to_file":
            entries = [(c, d) for c, d in entries if os.path.normcase(c) not in already]
        elif self.kind_filter != "all":
            entries = [(c, d) for c, d in entries if d.get("kind", "other") == self.kind_filter]
        if search:
            entries = [(c, d) for c, d in entries if search in self._searchable_text(c, d)]
        self._color_letters({first_letter(d["name"]) for _c, d in entries})
        if self.letter != "All":
            entries = [(c, d) for c, d in entries if first_letter(d["name"]) == self.letter]

        self.docs_list.delete(0, "end")
        self.shown_paths = []
        for path, doc in entries:
            kind = doc.get("kind", "other")
            mark = "✔ " if os.path.normcase(path) in already else "   "
            self.docs_list.insert("end", f" {mark}{_(KIND_LABELS[kind])} · {doc['name']}")
            self.docs_list.itemconfig("end", foreground=kind_color(kind))
            self.shown_paths.append(path)

        n = len(entries)
        if self.reading_in_progress:
            return
        if not self.book.settings.get("documents_folder"):
            text_value = _("No folder chosen.")
        else:
            if self.kind_filter == "to_file":
                text_value = (n_(n, "{n} document to file (out of {total})", "{n} documents to file (out of {total})",
                                 total=all_documents) if n else
                              _("✔ Everything is filed ({total} documents).\nClick “All” to see them again.",
                                total=all_documents))
            elif search:
                text_value = n_(n, "{n} document found", "{n} documents found")
            else:
                text_value = n_(n, "{n} document", "{n} documents")
            if not search and self.letter != "All" and n:
                text_value += _(" starting with {letter}", letter=self.letter)
            text_value += "\n" + _("✔ = already filed in the notebook")
            old_entries = self.index.get("old_doc_count", 0)
            if old_entries:
                text_value += "\n" + n_(old_entries, "⚠ {n} old .doc file not read\n   (save it as .docx with Word)",
                                        "⚠ {n} old .doc files not read\n   (save them as .docx with Word)")
        self.docs_count_label.configure(text=text_value)

    def _searchable_text(self, path, doc):
        """Name + text without accents, cached for fast searching."""
        key = (path, doc.get("mtime"))
        if key not in self._search_cache:
            self._search_cache[key] = normalize(doc["name"] + "\n" + doc.get("text", ""))
        return self._search_cache[key]

    def _current_document(self):
        selection = self.docs_list.curselection()
        if not selection:
            return None, None
        path = self.shown_paths[selection[0]]
        return path, self._documents().get(path)

    def _document_selected(self):
        path, doc = self._current_document()
        if doc is None:
            return
        self.doc_title.configure(text=doc["name"])
        kind = doc.get("kind", "other")
        self.doc_kind.configure(
            text=_("Recognised as: {kind}   —   this document is never changed.",
                   kind=_(KIND_NAMES[kind])),
            fg=kind_color(kind))
        self._show_understood(path, doc)
        self.doc_text.configure(state="normal")
        self.doc_text.delete("1.0", "end")
        self.doc_text.insert("1.0", doc["error"] or doc["text"] or _("(Empty document)"))
        search = self.docs_search_var.get().strip()
        if search:
            start = "1.0"
            while True:
                pos = self.doc_text.search(search, start, stopindex="end", nocase=True)
                if not pos:
                    break
                end = f"{pos}+{len(search)}c"
                self.doc_text.tag_add("match", pos, end)
                start = end
            first = self.doc_text.tag_nextrange("match", "1.0")
            if first:
                self.doc_text.see(first[0])
        self.doc_text.configure(state="disabled")

    def _cards_of_document(self, path):
        return [f for f in self.book.cards
                if os.path.normcase(f.get("source", "")) == os.path.normcase(path)]

    def _show_understood(self, path, doc):
        """Show the reformatted document (or the card it was already filed into)."""
        for w in self.understood_frame.winfo_children():
            w.destroy()
        rows = self._cards_of_document(path)
        kind = doc.get("kind", "other")
        if rows:
            cards, title_text = rows, _("Already filed in the notebook:")
            self.doc_card_button.configure(text=_("→  See the card"), command=lambda: self.view_card(rows[0]))
        elif kind in ("account", "contact") and not doc.get("error"):
            cards = self._keep_categories(guess(doc["name"], doc["text"], kind))
            title_text = _("What the notebook understood:")
            self.doc_card_button.configure(text=_("＋  Create a card from this document"),
                                           command=self.card_from_document)
        else:
            self.doc_card_button.configure(text=_("＋  Create a card from this document"),
                                           command=self.card_from_document)
            tk.Label(self.understood_frame, text=_("The notebook did not recognise this document. "
                                                   "You can still create a card: it will ask "
                                                   "whether it is a password or a contact."), font=self.f_small, bg=YELLOW_BG, fg=YELLOW_TEXT,
                     anchor="w", justify="left", wraplength=700).pack(fill="x")
            return
        tk.Label(self.understood_frame, text=title_text, font=self.f_bold, bg=YELLOW_BG,
                 fg=YELLOW_TEXT, anchor="w").pack(fill="x")
        grid_frame = tk.Frame(self.understood_frame, bg=YELLOW_BG)
        grid_frame.pack(fill="x", pady=(4, 0))
        r = 0
        for card in cards[:6]:
            lines = [(_("Name"), card.get("name", ""))]
            for field in FIELD_ORDER.get(card.get("type", "account"), []):
                value = card.get(field, "")
                if value and field != "notes":
                    lines.append((_(FIELD_LABELS[field]), value.replace("\n", ", ")))
            lines += [(p.get("label", ""), p.get("value", "")) for p in card.get("custom", [])]
            if card.get("notes"):
                lines.append((_("Notes"), card["notes"].replace("\n", " · ")[:120]))
            for label, value in lines:
                tk.Label(grid_frame, text=with_colon(label), font=self.f_small, bg=YELLOW_BG,
                         fg=YELLOW_TEXT, anchor="w").grid(row=r, column=0, sticky="nw", padx=(0, 12))
                tk.Label(grid_frame, text=value, font=self.f_password if label == _("Password")
                         else self.f_bold, bg=YELLOW_BG, fg=INK, anchor="w", justify="left",
                         wraplength=650).grid(row=r, column=1, sticky="w")
                r += 1
            r += 1
        if len(cards) > 6:
            tk.Label(grid_frame, text=_("… and {n} more contacts", n=len(cards) - 6), font=self.f_small,
                     bg=YELLOW_BG, fg=YELLOW_TEXT).grid(row=r, column=0, columnspan=2, sticky="w")

    def view_card(self, card):
        """Switch to the card's tab and select it."""
        self.current_id = card["id"]
        self.show_page(card.get("type", "account"))

    def open_document(self):
        path, doc = self._current_document()
        if not path:
            messagebox.showinfo(APP_NAME, _("First choose a document in the list."))
            return
        try:
            open_with_system(path)
        except OSError as exc:
            messagebox.showerror(APP_NAME, _("The document could not be opened.\n\n") + str(exc))

    def card_from_document(self):
        path, doc = self._current_document()
        if doc is None:
            messagebox.showinfo(APP_NAME, _("First choose a document in the list."))
            return
        if os.path.normcase(path) in self.book.known_sources():
            if not messagebox.askyesno(
                    APP_NAME, _("“{name}” is already filed in the notebook.\nCreate another "
                                "card anyway?", name=doc["name"]), default="no"):
                return
        kind = doc.get("kind", "other")
        if kind == "other":
            kind = ask_kind(self, doc["name"])
            if kind is None:
                return
        suggestions = self._keep_categories(guess(doc["name"], doc["text"], kind))
        self.book.restore_source(path)
        now_str = datetime.now().isoformat(timespec="seconds")
        cards = [self.book.new_card(source=path, source_mtime=doc.get("mtime"),
                                    imported_at=now_str, **fields)
                 for fields in suggestions]
        self.current_id = cards[0]["id"]
        self.schedule_save()
        self.show_page(kind)
        if len(cards) > 1:
            text_value = _("This document contained {n} contacts: they have all been created.", n=len(cards))
        else:
            text_value = _("The card was filled in from the document.")
        text_value += "\n\n" + _("Check that each piece of information is in the right place.")
        messagebox.showinfo(_("Card created"), text_value)

    # -------------------------------------------------- drag and drop / import
    def _enable_drag_and_drop(self):
        """Accept files dragged from Windows Explorer onto the window."""
        self.drops = queue.Queue()
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
            define = (user32.SetWindowLongPtrW if ctypes.sizeof(ctypes.c_void_p) == 8
                      else user32.SetWindowLongW)
            define.restype = ctypes.c_void_p
            define.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_void_p]
            user32.CallWindowProcW.restype = LRESULT
            user32.CallWindowProcW.argtypes = [ctypes.c_void_p, wintypes.HWND, wintypes.UINT,
                                               wintypes.WPARAM, wintypes.LPARAM]
            shell32.DragQueryFileW.restype = wintypes.UINT
            shell32.DragQueryFileW.argtypes = [ctypes.c_void_p, wintypes.UINT,
                                               wintypes.LPWSTR, wintypes.UINT]
            shell32.DragFinish.argtypes = [ctypes.c_void_p]
            shell32.DragAcceptFiles.argtypes = [wintypes.HWND, wintypes.BOOL]

            hwnd = int(self.root.wm_frame(), 16)
            old_backup = {}

            def procedure(h, message, wparam, lparam):
                if message == WM_DROPFILES:
                    try:
                        n = shell32.DragQueryFileW(wparam, 0xFFFFFFFF, None, 0)
                        paths = []
                        for i in range(n):
                            buffer = ctypes.create_unicode_buffer(32768)
                            shell32.DragQueryFileW(wparam, i, buffer, 32768)
                            paths.append(buffer.value)
                        self.drops.put(paths)
                    finally:
                        shell32.DragFinish(wparam)
                    return 0
                return user32.CallWindowProcW(old_backup["proc"], h, message, wparam, lparam)

            self._drop_procedure = WNDPROC(procedure)   # kept in memory (important)
            old_backup["proc"] = define(hwnd, GWLP_WNDPROC,
                                        ctypes.cast(self._drop_procedure, ctypes.c_void_p))
            shell32.DragAcceptFiles(hwnd, True)
        except Exception:
            return  # no drag and drop: the "Import files…" button is still there
        self.root.after(300, self._watch_drops)

    def _watch_drops(self):
        try:
            while True:
                self.import_paths(self.drops.get_nowait())
        except queue.Empty:
            pass
        self.root.after(300, self._watch_drops)

    def choose_files_to_import(self):
        paths = filedialog.askopenfilenames(
            title=_("Choose the documents to file (several at once is fine)"),
            filetypes=[(_("Word and text documents"), "*.docx *.txt"), (_("All files"), "*.*")])
        if paths:
            self.import_paths(list(paths))

    def import_paths(self, paths):
        """File away files (or whole folders) dragged in or chosen."""
        txt_folder = self.book.settings.get("txt_folder", "")
        files, old_doc_count, ignores = [], 0, 0
        for path in paths:
            if os.path.isdir(path):
                found, old_entries = list_documents(path, [txt_folder])
                files += found
                old_doc_count += old_entries
            elif os.path.basename(path).startswith("~$"):
                continue
            elif path.lower().endswith(READ_EXTENSIONS):
                files.append(path)
            elif path.lower().endswith(".doc"):
                old_doc_count += 1
            else:
                ignores += 1

        already = self.book.known_sources()
        to_file, unrecognised, already_count = [], [], 0
        for path in sorted(set(files), key=lambda c: sort_key(Path(c).stem)):
            if os.path.normcase(path) in already:
                already_count += 1
                continue
            try:
                text_value = read_document(path)
            except Exception:
                unrecognised.append((path, ""))
                continue
            kind = classify_document(text_value)
            if kind == "other":
                unrecognised.append((path, text_value))
            else:
                to_file.append((path, self._keep_categories(
                    guess(Path(path).stem, text_value, kind))))

        account_count = sum(1 for _c, fs in to_file for f in fs if f["type"] == "account")
        contact_count = sum(1 for _c, fs in to_file for f in fs if f["type"] == "contact")
        remarks = []
        if already_count:
            remarks.append(n_(already_count, "{n} document already filed: skipped.",
                              "{n} documents already filed: skipped."))
        if old_doc_count:
            remarks.append(n_(old_doc_count, "{n} old .doc file not read (save it as .docx with Word).",
                              "{n} old .doc files not read (save them as .docx with Word)."))
        if ignores:
            remarks.append(n_(ignores, "{n} file of another type skipped.",
                              "{n} files of another type skipped."))
        if unrecognised:
            names = ", ".join(Path(c).stem for c, _t in unrecognised[:6])
            names += "…" if len(unrecognised) > 6 else ""
            remarks.append(n_(len(unrecognised), "{n} document not recognised: {names}",
                              "{n} documents not recognised: {names}", names=names))

        if not to_file and not unrecognised:
            messagebox.showinfo(APP_NAME, _("Nothing new to file.\n\n") + "\n".join(remarks))
            return
        if to_file and not messagebox.askyesno(
                _("File these documents?"),
                _("The notebook will file:") + "\n\n   • "
                + n_(account_count, "{n} password  →  “My passwords”",
                     "{n} passwords  →  “My passwords”") + "\n   • "
                + n_(contact_count, "{n} contact  →  “My contacts”",
                     "{n} contacts  →  “My contacts”") + "\n\n"
                + ("\n".join(remarks) + "\n\n" if remarks else "")
                + _("The documents themselves are not changed. Continue?")):
            return
        forced = False
        if unrecognised:
            forced = messagebox.askyesno(
                _("Documents not recognised"),
                n_(len(unrecognised), "{n} document looks like neither a password nor a contact.",
                   "{n} documents look like neither a password nor a contact.")
                + "\n\n" + _("File them anyway in “My passwords”?\n(their text will go into the "
                             "card's Notes)"), default="no")
        try:
            self.book.save()
            self.book.daily_backup(force=True)
        except OSError:
            pass
        first_line = None
        now_str = datetime.now().isoformat(timespec="seconds")
        for path, suggestions in to_file:
            for fields in suggestions:
                self.book.restore_source(path)
                card = self.book.new_card(source=path, imported_at=now_str,
                                          source_mtime=self._mtime(path), **fields)
                first_line = first_line or card
        if forced:
            for path, text_value in unrecognised:
                fields = self._keep_categories([guess_card(Path(path).stem, text_value)])[0]
                self.book.restore_source(path)
                card = self.book.new_card(source=path, imported_at=now_str,
                                          source_mtime=self._mtime(path), **fields)
                first_line = first_line or card
        if first_line is None:
            return
        self.save()
        self.current_id = first_line["id"]
        total = account_count + contact_count + (len(unrecognised) if forced else 0)
        self.show_page("contact" if contact_count > account_count + (len(unrecognised) if forced else 0)
                       else "account")
        messagebox.showinfo(_("All filed!"), n_(total, "{n} card created.", "{n} cards created."))

    @staticmethod
    def _mtime(path):
        try:
            return os.stat(path).st_mtime
        except OSError:
            return None

    def _keep_categories(self, suggestions):
        """A guessed category is only kept if it exists in the settings."""
        for fields in suggestions:
            if "category" in fields:
                fields["category"] = self.book.existing_category(fields["category"])
        return suggestions

    def import_all(self):
        """Former "File everything" button: it is now the synchronization."""
        self.sync_now()


def ask_text(app, title_text, question, value=""):
    """Small window to type some text (in large print). None if cancelled."""
    answer = {"text": None}
    f = tk.Toplevel(app.root)
    f.title(title_text)
    f.configure(bg=WHITE, padx=24, pady=18)
    f.transient(app.root)
    f.resizable(False, False)
    tk.Label(f, text=question, font=app.f_bold, bg=WHITE, fg=INK).pack(anchor="w")
    var = tk.StringVar(value=value)
    entry_widget = app.text_entry(f, var)
    entry_widget.pack(fill="x", ipady=4, pady=(6, 14))

    def validate(_event=None):
        if var.get().strip():
            answer["text"] = var.get()
            f.destroy()

    entry_widget.bind("<Return>", validate)
    buttons = tk.Frame(f, bg=WHITE)
    buttons.pack(fill="x")
    app.button(buttons, _("Cancel"), f.destroy).pack(side="right")
    app.button(buttons, _("✔  OK"), validate, "green").pack(side="right", padx=10)
    f.grab_set()
    entry_widget.focus_set()
    entry_widget.select_range(0, "end")
    app.root.wait_window(f)
    return answer["text"]


def choose_color(app, name):
    """Grid of soft colors (all readable with dark text)."""
    answer = {"color": None}
    f = tk.Toplevel(app.root)
    f.title(_("Category colour"))
    f.configure(bg=WHITE, padx=24, pady=18)
    f.transient(app.root)
    f.resizable(False, False)
    tk.Label(f, text=_("Colour for “{name}”:", name=name), font=app.f_bold, bg=WHITE,
             fg=INK).pack(anchor="w", pady=(0, 10))
    grid_frame = tk.Frame(f, bg=WHITE)
    grid_frame.pack()

    def choose(color):
        answer["color"] = color
        f.destroy()

    for i, (label, color) in enumerate(CATEGORY_PALETTE):
        tk.Button(grid_frame, text=_(label), font=app.f_bold, bg=color, fg=TEXT_ON_PASTEL,
                  activebackground=color, activeforeground=TEXT_ON_PASTEL, width=10,
                  relief="solid", bd=1, pady=10, cursor="hand2", highlightthickness=0,
                  command=lambda c=color: choose(c)).grid(row=i // 5, column=i % 5,
                                                          padx=4, pady=4)
    app.button(f, _("Cancel"), f.destroy).pack(anchor="e", pady=(12, 0))
    f.grab_set()
    app.root.wait_window(f)
    return answer["color"]


def ask_kind(app, name):
    """Small window asking: is it a password or a contact?"""
    answer = {"kind": None}
    f = tk.Toplevel(app.root)
    f.title(_("What kind of document?"))
    f.configure(bg=WHITE, padx=24, pady=18)
    f.transient(app.root)
    f.resizable(False, False)
    tk.Label(f, text=f"« {name} »\n\n" + _("What does this document contain?"), font=app.f_bold,
             bg=WHITE, fg=INK, justify="left").pack(anchor="w", pady=(0, 14))

    def choose(kind):
        answer["kind"] = kind
        f.destroy()

    buttons = tk.Frame(f, bg=WHITE)
    buttons.pack(fill="x")
    app.button(buttons, _("A password"), lambda: choose("account"), "blue").pack(side="left")
    app.button(buttons, _("A contact"), lambda: choose("contact"), "blue").pack(side="left", padx=10)
    app.button(buttons, _("Cancel"), f.destroy).pack(side="right")
    f.grab_set()
    f.focus_set()
    app.root.wait_window(f)
    return answer["kind"]


class GeneratorWindow:
    """Small window to create a password."""

    def __init__(self, app):
        self.app = app
        f = self.window = tk.Toplevel(app.root)
        f.title(_("Create a new password"))
        f.configure(bg=WHITE, padx=24, pady=18)
        f.transient(app.root)
        f.resizable(False, False)

        tk.Label(f, text=_("Create a new password"), font=app.f_title,
                 bg=WHITE, fg=INK).pack(anchor="w")

        self.kind_var = tk.StringVar(value="easy")
        selection = tk.Frame(f, bg=WHITE)
        selection.pack(anchor="w", pady=(12, 6))
        for value, text_value in (("easy", _("Easy to read (words)")),
                                  ("strong", _("Very strong (letters and symbols)"))):
            tk.Radiobutton(selection, text=text_value, value=value, variable=self.kind_var,
                           command=self.new, font=app.f_base, bg=WHITE,
                           fg=INK, activebackground=WHITE, selectcolor=BLUE_LIGHT,
                           anchor="w").pack(anchor="w", pady=2)

        line = tk.Frame(f, bg=WHITE)
        line.pack(anchor="w", pady=6)
        tk.Label(line, text=_("Length:"), font=app.f_bold, bg=WHITE, fg=GREY).pack(side="left")
        self.length_var = tk.IntVar(value=4)
        self.slider = tk.Scale(line, from_=3, to=6, orient="horizontal",
                               variable=self.length_var, length=260,
                               command=lambda v: self.new(), font=app.f_base,
                               bg=WHITE, highlightthickness=0, sliderlength=36, width=22)
        self.slider.pack(side="left", padx=10)
        self.unit_label = tk.Label(line, text=_("words"), font=app.f_base, bg=WHITE, fg=GREY)
        self.unit_label.pack(side="left")

        self.password_var = tk.StringVar()
        tk.Entry(f, textvariable=self.password_var, font=app.f_password, bg=YELLOW_BG, fg=INK,
                 relief="solid", bd=1, justify="center", width=28,
                 highlightthickness=2, highlightbackground=YELLOW_BORDER,
                 readonlybackground=YELLOW_BG, state="readonly").pack(fill="x", pady=12, ipady=8)

        buttons = tk.Frame(f, bg=WHITE)
        buttons.pack(fill="x", pady=(4, 0))
        app.button(buttons, _("↻  Another one"), self.new).pack(side="left")
        self.copy_button = app.button(buttons, _("Copy"), None)
        self.copy_button.configure(command=lambda: app.copy(self.password_var.get(), self.copy_button))
        self.copy_button.pack(side="left", padx=10)
        app.button(buttons, _("Cancel"), f.destroy).pack(side="right")
        app.button(buttons, _("✔  Use this password"), self.use, "green").pack(side="right", padx=10)

        tk.Label(f, text=_("The old password will be kept in the card's notes."),
                 font=app.f_small, bg=WHITE, fg=GREY).pack(anchor="w", pady=(12, 0))

        self._previous_kind = None
        self.new()
        f.grab_set()
        f.focus_set()

    def new(self):
        kind = self.kind_var.get()
        if kind != self._previous_kind:
            self._previous_kind = kind
            if kind == "easy":
                self.slider.configure(from_=3, to=6)
                self.length_var.set(4)
                self.unit_label.configure(text=_("words"))
            else:
                self.slider.configure(from_=12, to=32)
                self.length_var.set(16)
                self.unit_label.configure(text=_("characters"))
        n = self.length_var.get()
        if kind == "easy":
            self.password_var.set(generate_passphrase(n))
        else:
            self.password_var.set(generate_password(n))

    def use(self):
        self.app.replace_password(self.password_var.get())
        self.window.destroy()


# ---------------------------------------------------------------------------
# Installation / uninstallation (built program: Windows and Linux;
# on Mac, the app is simply dragged into "Applications")
# ---------------------------------------------------------------------------

PUBLISHER = "Louis"
UNINSTALL_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\PocketBook"


def special_folder(num, fallback_path):
    """Windows folder (Desktop = 0x10, Start menu Programs = 0x02)."""
    try:
        import ctypes
        from ctypes import wintypes
        buffer = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        if ctypes.windll.shell32.SHGetFolderPathW(None, num, None, 0, buffer) == 0:
            return Path(buffer.value)
    except Exception:
        pass
    return fallback_path


def linux_desktop_folder():
    try:
        import subprocess
        path = subprocess.run(["xdg-user-dir", "DESKTOP"], capture_output=True,
                              text=True, timeout=5).stdout.strip()
        if path and os.path.isdir(path):
            return Path(path)
    except Exception:
        pass
    return Path.home() / "Desktop"


def can_install():
    """Only the built program (.exe, Linux binary) installs itself."""
    return getattr(sys, "frozen", False) and (IS_WINDOWS or IS_LINUX)


def install_paths():
    if IS_WINDOWS:
        base = Path(os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local"))
        return {
            "folder": base / "Pocket Book",
            "exe": base / "Pocket Book" / "Pocket Book.exe",
            "desktop": special_folder(0x10, Path.home() / "Desktop") / "Pocket Book.lnk",
            "menu": special_folder(0x02, Path.home()) / "Pocket Book.lnk",
        }
    data = Path(os.environ.get("XDG_DATA_HOME") or (Path.home() / ".local" / "share"))
    return {
        "folder": data / "pocket-book",
        "exe": data / "pocket-book" / "pocket-book",
        "icon": data / "pocket-book" / "pocketbook.png",
        "desktop": linux_desktop_folder() / "pocket-book.desktop",
        "menu": data / "applications" / "pocket-book.desktop",
        "command": Path.home() / ".local" / "bin" / "pocket-book",
        "options": data / "pocket-book" / "installation.json",
    }


def create_shortcut(link, target_path):
    """Windows: .lnk shortcut (built-in Windows tool). Linux: .desktop launcher."""
    import subprocess
    link = Path(link)
    link.parent.mkdir(parents=True, exist_ok=True)
    if IS_WINDOWS:
        script = ("$r = (New-Object -ComObject WScript.Shell).CreateShortcut($env:MC_LINK);"
                  "$r.TargetPath = $env:MC_TARGET;"
                  "$r.WorkingDirectory = Split-Path $env:MC_TARGET;"
                  "$r.IconLocation = $env:MC_TARGET + ',0';"
                  "$r.Description = 'Pocket Book';"
                  "$r.Save()")
        env = dict(os.environ, MC_LINK=str(link), MC_TARGET=str(target_path))
        subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                        "-Command", script], env=env, check=True, timeout=30,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return
    icon_path = install_paths()["icon"]
    link.write_text(
        "[Desktop Entry]\n"
        "Type=Application\n"
        f"Name={APP_NAME}\n"
        f"Comment={_('Passwords and contacts, without internet')}\n"
        f'Exec="{target_path}"\n'
        f"Icon={icon_path}\n"
        "Terminal=false\n"
        "Categories=Utility;Office;\n", encoding="utf-8")
    os.chmod(link, 0o755)
    try:  # GNOME: allow launching from the Desktop
        subprocess.run(["gio", "set", str(link), "metadata::trusted", "true"],
                       capture_output=True, timeout=5)
    except Exception:
        pass


def same_file(a, b):
    try:
        return os.path.normcase(str(Path(a).resolve())) == os.path.normcase(str(Path(b).resolve()))
    except OSError:
        return False


def read_registry(name, fallback=None):
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, UNINSTALL_KEY) as key:
            return winreg.QueryValueEx(key, name)[0]
    except (OSError, ImportError):
        return fallback


def desktop_option():
    """Had the user chosen a Desktop icon?"""
    if IS_WINDOWS:
        return bool(read_registry("DesktopShortcut", read_registry("RaccourciBureau", 1)))
    try:
        with open(install_paths()["options"], encoding="utf-8") as f:
            options = json.load(f)
        return bool(options.get("desktop", options.get("bureau", True)))   # "bureau": before 1.1
    except (OSError, ValueError):
        return True


def already_installed():
    return install_paths()["exe"].exists()


def register_in_windows(exe, with_desktop):
    """Make "Pocket Book" appear in Settings > Apps (so it can be uninstalled)."""
    import winreg
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, UNINSTALL_KEY) as key:
        value_list = {
            "DisplayName": APP_NAME,
            "DisplayVersion": VERSION,
            "Publisher": PUBLISHER,
            "DisplayIcon": f"{exe},0",
            "InstallLocation": str(Path(exe).parent),
            "UninstallString": f'"{exe}" --uninstall',
            "InstallDate": datetime.now().strftime("%Y%m%d"),
        }
        for name, value in value_list.items():
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
        for name, value in (("NoModify", 1), ("NoRepair", 1),
                            ("EstimatedSize", max(1, os.path.getsize(exe) // 1024)),
                            ("DesktopShortcut", 1 if with_desktop else 0)):
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)


def install(source_exe, with_desktop):
    """Copy the program, create the shortcuts, register it with the system.

    Returns (success, error message).
    """
    paths = install_paths()
    exe = paths["exe"]
    try:
        exe.parent.mkdir(parents=True, exist_ok=True)
        if not same_file(source_exe, exe):
            if IS_LINUX and exe.exists():
                exe.unlink()  # Linux: a program can be replaced even while it is running
            shutil.copy2(source_exe, exe)
        if IS_LINUX:
            os.chmod(exe, 0o755)
            shutil.copy2(resource("pocketbook.png"), paths["icon"])
    except PermissionError:
        return False, _("Pocket Book is probably still open.\nClose it, then click “Install” again.")
    except OSError as exc:
        return False, _("Copying the program failed.") + "\n\n" + str(exc)

    links = [paths["menu"]] + ([paths["desktop"]] if with_desktop else [])
    for link in links:
        try:
            create_shortcut(link, exe)
        except Exception:
            pass
    if not with_desktop and paths["desktop"].exists():
        try:
            paths["desktop"].unlink()
        except OSError:
            pass
    try:
        if IS_WINDOWS:
            register_in_windows(exe, with_desktop)
        else:
            write_json_safely(paths["options"], {"desktop": with_desktop, "version": VERSION})
            command = paths["command"]
            command.parent.mkdir(parents=True, exist_ok=True)
            if command.is_symlink() or command.exists():
                command.unlink()
            command.symlink_to(exe)
    except Exception:
        pass
    return True, ""


def remove_installation(delete_data):
    """Remove the program, shortcuts and registration. Returns a closing text."""
    import subprocess
    paths = install_paths()
    for key in ("desktop", "menu", "command"):
        link = paths.get(key)
        try:
            if link and (link.exists() or link.is_symlink()):
                link.unlink()
        except OSError:
            pass
    if IS_WINDOWS:
        try:
            import winreg
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, UNINSTALL_KEY)
        except OSError:
            pass
    if delete_data:
        shutil.rmtree(DATA_FOLDER, ignore_errors=True)
    folder = paths["folder"]
    if IS_WINDOWS:
        # The program is running: its folder is deleted right after it closes.
        subprocess.Popen(
            f'cmd /c ping 127.0.0.1 -n 4 > nul & rmdir /s /q "{folder}"',
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0), cwd=str(Path.home()))
    else:
        shutil.rmtree(folder, ignore_errors=True)
    text_value = _("Pocket Book has been uninstalled.")
    if not delete_data:
        text_value += "\n\n" + _("Your cards are still in:") + f"\n{DATA_FOLDER}"
    return text_value


def _simple_window(title_text, parent=None):
    """Small, clear and readable window for the installation."""
    apply_theme_colors("light")
    root = tk.Toplevel(parent) if parent is not None else tk.Tk()
    root.title(title_text)
    root.configure(bg=WHITE, padx=34, pady=28)
    root.resizable(False, False)
    set_icon(root)
    family_name = available_font(TEXT_FONTS)
    fonts = {
        "title": tkfont.Font(family=family_name, size=22, weight="bold"),
        "base": tkfont.Font(family=family_name, size=14),
        "bold": tkfont.Font(family=family_name, size=14, weight="bold"),
    }
    return root, fonts


def _big_button(parent, text_value, command, fonts, primary=False):
    return tk.Button(parent, text=text_value, command=command, font=fonts["bold"],
                     bg=GREEN if primary else WHITE, fg=ON_ACCENT if primary else INK,
                     activebackground=GREEN_DARK if primary else BLUE_LIGHT,
                     activeforeground=ON_ACCENT if primary else INK,
                     relief="solid", bd=1, padx=22, pady=10, cursor="hand2", highlightthickness=0)


def _install_language_choice(area, fonts, refresh):
    """Small row of languages at the top of the installation window."""
    line = tk.Frame(area, bg=WHITE)
    line.pack(anchor="e", pady=(0, 10))
    for code, name in LANGUAGES.items():
        active = code == current_language()
        tk.Button(line, text=name, font=fonts["base"] if not active else fonts["bold"],
                  bg=BLUE if active else WHITE, fg=ON_ACCENT if active else INK,
                  activebackground=BLUE_LIGHT, relief="solid", bd=1, padx=8, pady=2,
                  cursor="hand2", highlightthickness=0,
                  command=lambda c=code: (set_language(c), refresh())).pack(side="left", padx=2)


def install_window():
    """Launched from a download, a USB stick…: offer to install (or update)."""
    import subprocess
    paths = install_paths()
    already = already_installed()
    root, fonts = _simple_window(_("Installing Pocket Book"))
    area = tk.Frame(root, bg=WHITE)
    area.pack(fill="both", expand=True)
    desktop_var = tk.BooleanVar(value=desktop_option())

    def clear():
        for w in area.winfo_children():
            w.destroy()

    def welcome_screen():
        clear()
        root.title(_("Installing Pocket Book"))
        _install_language_choice(area, fonts, welcome_screen)
        tk.Label(area, text=_("Update Pocket Book") if already else _("Install Pocket Book"),
                 font=fonts["title"], bg=WHITE, fg=INK).pack(anchor="w")
        text_value = (_("A new version of Pocket Book will replace the old one.\nYour cards are not "
                        "touched.") if already else
                      _("Pocket Book will be installed on this computer.\nIt works without internet: "
                        "nothing leaves the computer.\nYour cards will be kept in:") + f"\n{DATA_FOLDER}")
        tk.Label(area, text=text_value, font=fonts["base"], bg=WHITE, fg=GREY,
                 justify="left").pack(anchor="w", pady=(10, 16))
        tk.Checkbutton(area, text=_("Put a “Pocket Book” icon on the Desktop"),
                       variable=desktop_var, font=fonts["base"], bg=WHITE, fg=INK,
                       activebackground=WHITE, selectcolor=WHITE).pack(anchor="w", pady=(0, 20))
        buttons = tk.Frame(area, bg=WHITE)
        buttons.pack(fill="x")
        _big_button(buttons, _("Cancel"), root.destroy, fonts).pack(side="right")
        _big_button(buttons, _("Update") if already else _("Install"), start_install, fonts,
                    primary=True).pack(side="right", padx=(0, 12))

    def start_install():
        clear()
        tk.Label(area, text=_("Installing…"), font=fonts["title"], bg=WHITE,
                 fg=INK).pack(anchor="w")
        root.update()
        success, error = install(Path(sys.executable), desktop_var.get())
        clear()
        if not success:
            tk.Label(area, text=_("The installation could not be completed"), font=fonts["title"],
                     bg=WHITE, fg=RED).pack(anchor="w")
            tk.Label(area, text=error, font=fonts["base"], bg=WHITE, fg=INK,
                     justify="left").pack(anchor="w", pady=(10, 20))
            buttons = tk.Frame(area, bg=WHITE)
            buttons.pack(fill="x")
            _big_button(buttons, _("Close"), root.destroy, fonts).pack(side="right")
            _big_button(buttons, _("Try again"), welcome_screen, fonts).pack(side="right", padx=(0, 12))
            return
        tk.Label(area, text="✔  " + _("Pocket Book is installed"), font=fonts["title"], bg=WHITE,
                 fg=GREEN_TEXT).pack(anchor="w")
        if desktop_var.get():
            where = _("To open it, double-click the “Pocket Book” icon on the Desktop\n(or look for "
                      "“Pocket Book” in the applications menu).")
        else:
            where = _("To open it, look for “Pocket Book” in the applications menu.")
        tk.Label(area, text=where + "\n\n" + _("This installation file can now be put away or deleted."),
                 font=fonts["base"], bg=WHITE, fg=GREY, justify="left").pack(anchor="w", pady=(10, 20))
        buttons = tk.Frame(area, bg=WHITE)
        buttons.pack(fill="x")

        def open_row():
            subprocess.Popen([str(paths["exe"]), "--language", current_language()],
                             cwd=str(paths["exe"].parent))
            root.destroy()

        _big_button(buttons, _("Close"), root.destroy, fonts).pack(side="right")
        _big_button(buttons, _("Open Pocket Book"), open_row, fonts,
                    primary=True).pack(side="right", padx=(0, 12))

    welcome_screen()
    root.mainloop()


def uninstall_window(parent=None):
    """Windows: Settings > Apps > Uninstall. Linux: button in the Settings.

    Returns True if the program was uninstalled.
    """
    root, fonts = _simple_window(_("Uninstall Pocket Book"), parent)
    result = {"done": False}
    tk.Label(root, text=_("Uninstall Pocket Book?"), font=fonts["title"], bg=WHITE,
             fg=INK).pack(anchor="w")
    tk.Label(root, text=_("The program and its icons will be removed from this computer.\nYour "
                          "cards are kept, in:") + f"\n{DATA_FOLDER}",
             font=fonts["base"], bg=WHITE, fg=GREY, justify="left").pack(anchor="w", pady=(10, 14))
    data_var = tk.BooleanVar(value=False)
    tk.Checkbutton(root, text=_("Also delete all my cards and their backups"),
                   variable=data_var, font=fonts["base"], bg=WHITE, fg=RED,
                   activebackground=WHITE, selectcolor=WHITE).pack(anchor="w", pady=(0, 20))

    def confirm():
        if data_var.get() and not messagebox.askyesno(
                _("Delete the cards?"),
                _("All cards, backups and .txt copies in this folder will be permanently erased:") + f"\n{DATA_FOLDER}\n\n" + _("Continue?"),
                icon="warning", default="no", parent=root):
            return
        text_value = remove_installation(data_var.get())
        messagebox.showinfo(APP_NAME, text_value, parent=root)
        result["done"] = True
        root.destroy()

    buttons = tk.Frame(root, bg=WHITE)
    buttons.pack(fill="x")
    _big_button(buttons, _("Cancel"), root.destroy, fonts).pack(side="right")
    tk.Button(buttons, text=_("Uninstall"), command=confirm, font=fonts["bold"], bg=RED,
              fg=ON_ACCENT, activebackground="#7E2617", activeforeground=ON_ACCENT,
              relief="solid", bd=1, padx=22, pady=10, cursor="hand2",
              highlightthickness=0).pack(side="right", padx=(0, 12))
    if parent is None:
        root.mainloop()
    else:
        root.transient(parent)
        root.grab_set()
        parent.wait_window(root)
    return result["done"]


def install_if_needed():
    """Return True if the program must stop here (installation or uninstallation)."""
    if not can_install():
        return False
    if "--uninstall" in sys.argv or "--desinstaller" in sys.argv:   # old flag: installs before 1.1
        uninstall_window()
        return True
    paths = install_paths()
    if not same_file(sys.executable, paths["exe"]):
        install_window()
        return True
    # Launched from the installed copy: repair whatever is missing.
    if IS_WINDOWS and read_registry("DisplayName") is None:
        try:
            register_in_windows(paths["exe"], True)
        except Exception:
            pass
    if desktop_option() and not paths["desktop"].exists():
        try:
            create_shortcut(paths["desktop"], paths["exe"])
        except Exception:
            pass
    return False


def main():
    if "--language" in sys.argv:  # language chosen in the installation window
        i = sys.argv.index("--language")
        if i + 1 < len(sys.argv):
            set_language(sys.argv[i + 1])
            FORCED_LANGUAGE[0] = sys.argv[i + 1]
    else:
        set_language(system_language())
    if IS_WINDOWS:
        try:  # sharp text on high-DPI screens
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    if install_if_needed():
        return
    migrate_old_folder()
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    root = tk.Tk()
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()
