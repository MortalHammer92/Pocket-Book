# -*- coding: utf-8 -*-
"""Pocket Book interface translations.

The program is written in English: each dictionary maps an English sentence to its
translation. A missing sentence simply stays in English (nothing breaks).
The {words} in braces are replaced by values: keep them as they are.

To add a language: add its name to LANGUAGES, a dictionary to TRANSLATIONS
and a list of simple words to EASY_WORDS (for "easy to read" passwords).
`python scripts/check_translations.py` reports missing sentences.
"""

LANGUAGES = {
    "fr": "Français",
    "en": "English",
    "es": "Español",
    "de": "Deutsch",
    "it": "Italiano",
}

# Simple words (no accents, easy to type) for "easy to read" passwords
EASY_WORDS = {
    "en": """
acorn anchor apple arrow autumn badger bakery balloon bamboo banana barn basket
beach bear bell berry bicycle biscuit blossom boat bottle breeze brick bridge
brook bubble bucket butter button cabin cactus camel candle canoe canyon carrot
castle cedar cherry chimney cloud clover coconut comet cookie copper cotton
crayon cricket daisy desert dolphin dragon eagle ember falcon feather fern
fiddle forest fossil fountain garden ginger glacier goose grape harbor hazel
hedge honey island jacket jasmine kettle kitten ladder lantern lemon lily
lizard maple meadow melon mitten moon moss mountain muffin nectar ocean olive
orchard otter owl paddle panda parrot peach pebble pepper piano pillow pine
planet plum pocket pond poppy puffin pumpkin rabbit rainbow river robin rocket
saddle sailor shell silver snail sparrow spruce squirrel star stone sugar
summer sunset teapot thistle thunder tiger tulip turtle valley velvet violin
walnut willow window winter
""".split(),
    "es": """
abeja abeto aguila album almendra ancla arbol arena arroz azucar ballena bambu
barco bosque botella brisa buho caballo cactus calle camino campana canela
caracol carta castillo cebolla cereza cesta cielo cisne cohete cometa conejo
copa coral cuaderno delfin dragon duna escoba espiga estrella faro farol flor
fresa fuente galleta gato gaviota girasol globo granja guitarra hamaca helado
hoja hormiga huerto invierno isla jardin jirafa lago lapiz laurel lechuza leon
libro limon llave lluvia lobo luna maiz mango manzana mapa mar margarita melon
miel molino montana naranja nido nieve nube nuez oliva oso otono palmera paloma
panda papel pato pera perla piano pinguino pino pluma pueblo puente queso rana
rio roble rosa sandia semilla sol sombrero tambor taza tigre tomate tortuga
trebol trigo tulipan uva valle vela velero verano viento violeta volcan
""".split(),
    "de": """
adler ahorn amsel anker apfel apfelbaum bach backofen ballon banane bauernhof
baum beere berg biene birne blatt blume boot brezel bruecke brunnen buch burg
butter dachs delfin dorf drache eiche eichhorn eimer engel ente erdbeere
fahrrad falke feder feld fenster fichte fisch fluss frosch fuchs garten geige
gipfel glocke gurke hafen hamster hase hecke heft himmel honig hund igel insel
kaffee kaktus kamel kamin karotte kastanie katze kerze kirsche kiste klee
koffer korb kuchen kuerbis lampe laterne leiter linde loeffel loewe mantel meer
melone mond moos muehle muschel nadel nebel nest nuss ofen olive orange otter
palme papier pfeffer pferd pflaume pilz pinguin pinsel planet quelle rabe
rakete regen ring rose sand schaf schiff schnee schuh sommer sonne stern strand
tanne tasse teller tiger tomate traube tulpe turm vogel wagen wald wasser wiese
wind winter wolke zebra zitrone zucker
""".split(),
    "it": """
abete acero alba albero ancora anguria ape aquila arancia arco autunno balena
banana barca bicicletta biscotto bosco bottone brezza bussola cammello campana
candela capanna cappello carciofo carota castagna castello cavallo cavolo cielo
cigno ciliegia ciotola cipresso collina cometa conchiglia coniglio corallo
cuore delfino duna estate farfalla faro fico fiore fiume foglia fontana
formaggio formica fragola fragranza gabbiano gallina gatto gelato giardino
giraffa girasole grano gufo inverno isola lago lampada lanterna leone lepre
libro limone lucciola luna mandorla mango mare margherita matita mela melone
miele mirtillo montagna mulino nave neve nido nocciola noce nuvola oliva
ombrello orologio orso panda pane papavero pappagallo pera pesca pesce piano
pigna pino pioggia pomodoro ponte prato primavera quaderno rana riccio rosa
ruscello sale sasso scoiattolo sedia sole stella tamburo tartaruga tazza tigre
torre trifoglio tulipano uva valle vela vento viola vulcano zucca
""".split(),
}

TRANSLATIONS = {
    "fr": {
        "(none)": "(aucune)",
        "All categories": "Toutes",
        "Pocket Book has been uninstalled.": "Pocket Book a été désinstallé.",
        "File type not supported": "Type de fichier non pris en charge",
        "This file is rewritten after every change: edit the card in the notebook.":
            "Ce fichier est réécrit à chaque changement : modifiez la fiche dans le carnet.",
        "Delete the category “{name}”?": "Supprimer la catégorie « {name} » ?",
        "Category colour": "Couleur de la catégorie",
        "What kind of document?": "Quel genre de document ?",
        "Installing Pocket Book": "Installation de Pocket Book",
        "Uninstall Pocket Book": "Désinstaller Pocket Book",
        "Untitled": "Sans nom",
        "New contact": "Nouveau contact",
        "New card": "Nouvelle fiche",
        "%m/%d/%Y at %H:%M": "%d/%m/%Y à %H:%M",
        "Notes": "Notes",
        "Automatic copy made by Pocket Book (card changed on {date}).":
            "Copie automatique faite par Pocket Book (fiche modifiée le {date}).",
        "Automatic copy made by Pocket Book.": "Copie automatique faite par Pocket Book.",
        "Name": "Nom",
        "Copy": "Copier",
        "✎  Edit by hand": "✎  Modifier à la main",
        "Add a field": "Ajouter un champ",
        "Categories": "Catégories",
        "Categories are used to sort cards. Each one has its own colour, shown in the list of cards.":
            "Les catégories servent à trier les fiches. Chacune a sa couleur, qui apparaît dans la liste des fiches.",
        "Language": "Langue",
        "Screen colours": "Couleurs de l'écran",
        "Choose whatever is easiest to read.": "Choisissez ce qui est le plus agréable à lire.",
        "Copy of cards as .txt": "Copie des fiches en .txt",
        "Each card is copied into a .txt file that updates itself. Make changes in the notebook, not in the .txt files.":
            "Chaque fiche est recopiée dans un fichier .txt, mis à jour tout seul. Les changements se font dans le carnet, pas dans les .txt.",
        "New category": "Nouvelle catégorie",
        "Name of the new category:": "Nom de la nouvelle catégorie :",
        "Rename the category": "Renommer la catégorie",
        "New name:": "Nouveau nom :",
        "＋  Create a card from this document": "＋  Créer une fiche avec ce document",
        "{n} contact": "{n} contact",
        "{n} contacts": "{n} contacts",
        "{n} card": "{n} fiche",
        "{n} cards": "{n} fiches",
        "Do you really want to delete the contact “{name}”?":
            "Voulez-vous vraiment supprimer le contact « {name} » ?",
        "Do you really want to delete the card “{name}”?":
            "Voulez-vous vraiment supprimer la fiche « {name} » ?",
        "Old password (replaced on {date}): {old}":
            "Ancien mot de passe (remplacé le {date}) : {old}",
        "No folder chosen.": "Aucun dossier choisi.",
        "This document contained {n} contacts: they have all been created.":
            "Ce document contenait {n} contacts : ils ont tous été créés.",
        "The card was filled in from the document.": "La fiche a été remplie à partir du document.",
        "Check that each piece of information is in the right place.":
            "Vérifiez que chaque information est au bon endroit.",
        "Card created": "Fiche créée",
        "All filed!": "C'est rangé !",
        "{n} card created.": "{n} fiche créée.",
        "{n} cards created.": "{n} fiches créées.",
        "Create a new password": "Créer un nouveau mot de passe",
        "A new version of Pocket Book will replace the old one.\nYour cards are not touched.":
            "Une nouvelle version de Pocket Book va remplacer l'ancienne.\nVos fiches ne sont pas touchées.",
        "To open it, double-click the “Pocket Book” icon on the Desktop\n(or look for “Pocket Book” in the applications menu).":
            "Pour l'ouvrir, double-cliquez sur l'icône « Pocket Book » du Bureau\n(ou cherchez « Pocket Book » dans le menu des applications).",
        "To open it, look for “Pocket Book” in the applications menu.":
            "Pour l'ouvrir, cherchez « Pocket Book » dans le menu des applications.",
        "The notebook was damaged and no backup could be read. A copy was kept: {file_path}":
            "Le carnet était abîmé et aucune sauvegarde n'a pu être lue. Une copie a été gardée : {file_path}",
        "My passwords": "Mes mots de passe",
        "My contacts": "Mes contacts",
        "My documents": "Mes documents",
        "First click on a category in the list.":
            "Cliquez d'abord sur une catégorie dans la liste.",
        "The category “{name}” already exists.": "La catégorie « {name} » existe déjà.",
        "{n} card will no longer have a category (the card itself is not deleted).":
            "{n} fiche n'aura plus de catégorie (la fiche elle-même n'est pas supprimée).",
        "{n} cards will no longer have a category (the cards themselves are not deleted).":
            "{n} fiches n'auront plus de catégorie (les fiches elles-mêmes ne sont pas supprimées).",
        "Delete the category?": "Supprimer la catégorie ?",
        "↻  Sync now": "↻  Synchroniser maintenant",
        "Choose the folder…": "Choisir le dossier…",
        "Import files…": "Importer des fichiers…",
        "To file": "À ranger",
        "All": "Tout",
        "Passwords": "Mots de passe",
        "Contacts": "Contacts",
        "Not recognised": "Non reconnus",
        "Choose a document in the list.": "Choisissez un document dans la liste.",
        "This document is never changed by the notebook.":
            "Ce document n'est jamais modifié par le carnet.",
        "{n} contact found": "{n} contact trouvé",
        "{n} contacts found": "{n} contacts trouvés",
        "{n} card found": "{n} fiche trouvée",
        "{n} cards found": "{n} fiches trouvées",
        ", from A to Z": ", de A à Z",
        " starting with {letter}": " à la lettre {letter}",
        "Delete?": "Supprimer ?",
        "Website": "Site internet",
        "No website address is written on this card.":
            "Aucune adresse de site n'est notée sur cette fiche.",
        "%m/%d/%Y": "%d/%m/%Y",
        "✎ Editing…": "✎ Modification en cours…",
        "Which folder should hold the .txt copy of the cards?":
            "Dans quel dossier ranger la copie .txt des fiches ?",
        "Choose a folder other than the one with the original documents\n(for example a “Cards as text” subfolder).":
            "Choisissez un autre dossier que celui des documents d'origine\n(par exemple un sous-dossier « Fiches en texte »).",
        "\n\nThe old folder has not been changed.": "\n\nL'ancien dossier n'a pas été modifié.",
        "This file does not exist (or no longer exists) on the computer.":
            "Ce fichier n'existe pas (ou plus) sur l'ordinateur.",
        "Where are your documents kept?": "Où sont rangés vos documents ?",
        "First choose the folder where your documents are kept.":
            "Choisissez d'abord le dossier où sont rangés vos documents.",
        "Reading documents…": "Lecture des documents…",
        "{n} card created": "{n} fiche créée",
        "{n} cards created": "{n} fiches créées",
        "{n} card updated": "{n} mise à jour",
        "{n} cards updated": "{n} mises à jour",
        "{n} to check (⚠ in the notes)": "{n} à vérifier (⚠ dans les notes)",
        "Sync": "Synchronisation",
        "{n} document": "{n} document",
        "{n} documents": "{n} documents",
        "✔ = already filed in the notebook": "✔ = déjà rangé dans le carnet",
        "Recognised as: {kind}   —   this document is never changed.":
            "Reconnu comme : {kind}   —   ce document n'est jamais modifié.",
        "(Empty document)": "(Document vide)",
        "Already filed in the notebook:": "Déjà rangé dans le carnet :",
        "What the notebook understood:": "Ce que le carnet a compris :",
        "First choose a document in the list.": "Choisissez d'abord un document dans la liste.",
        "Choose the documents to file (several at once is fine)":
            "Choisissez les documents à ranger (plusieurs à la fois possible)",
        "{n} document already filed: skipped.": "{n} document déjà rangé : ignoré.",
        "{n} documents already filed: skipped.": "{n} documents déjà rangés : ignorés.",
        "{n} old .doc file not read (save it as .docx with Word).":
            "{n} ancien fichier .doc non lu (à enregistrer en .docx avec Word).",
        "{n} old .doc files not read (save them as .docx with Word).":
            "{n} anciens fichiers .doc non lus (à enregistrer en .docx avec Word).",
        "{n} file of another type skipped.": "{n} fichier d'un autre type ignoré.",
        "{n} files of another type skipped.": "{n} fichiers d'un autre type ignorés.",
        "{n} document not recognised: {names}": "{n} document non reconnu : {names}",
        "{n} documents not recognised: {names}": "{n} documents non reconnus : {names}",
        "Documents not recognised": "Documents non reconnus",
        "Cancel": "Annuler",
        "✔  OK": "✔  Valider",
        "A password": "Un mot de passe",
        "A contact": "Un contact",
        "Easy to read (words)": "Facile à lire (des mots)",
        "Very strong (letters and symbols)": "Très solide (lettres et signes)",
        "words": "mots",
        "Passwords and contacts, without internet": "Mots de passe et contacts, sans internet",
        "Pocket Book is probably still open.\nClose it, then click “Install” again.":
            "Pocket Book est sans doute encore ouvert.\nFermez-le, puis cliquez à nouveau sur « Installer ».",
        "Your cards are still in:": "Vos fiches sont toujours dans :",
        "Pocket Book will be installed on this computer.\nIt works without internet: nothing leaves the computer.\nYour cards will be kept in:":
            "Pocket Book va être installé sur cet ordinateur.\nIl fonctionne sans internet : rien ne quitte l'ordinateur.\nVos fiches seront rangées dans :",
        "Cards as text": "Fiches en texte",
        "⚠ The document “{name}” changed on {date}: check this card (it was not replaced).":
            "⚠ Le document « {name} » a changé le {date} : vérifiez cette fiche (elle n'a pas été remplacée).",
        "Could not read this document ({error}).": "Impossible de lire ce document ({error}).",
        "Settings": "Réglages",
        "A": "A",
        "Save now": "Enregistrer maintenant",
        "Field": "Champ",
        "＋  Add a field": "＋  Ajouter un champ",
        "The .txt copy": "La copie .txt",
        "The folder": "Le dossier",
        "↻  Create a new password": "↻  Créer un nouveau mot de passe",
        "＋  Add this field": "＋  Ajouter ce champ",
        "Remove the field?": "Retirer le champ ?",
        "＋  New": "＋  Nouvelle",
        "Rename": "Renommer",
        "Colour…": "Couleur…",
        "Delete": "Supprimer",
        "Change folder…": "Changer de dossier…",
        "Open the folder": "Ouvrir le dossier",
        "Open in Word": "Ouvrir dans Word",
        "A copy stays in today's backups.": "Une copie reste dans les sauvegardes du jour.",
        "Change the password?": "Changer le mot de passe ?",
        "Do you really want to change the password for “{name}”?\n\nCareful: this only changes the notebook. You must also change it on the website itself, otherwise you will no longer be able to log in.\n\n(The old password will be kept in the notes.)":
            "Voulez-vous vraiment changer le mot de passe de « {name} » ?\n\nAttention : cela change seulement le carnet. Il faudra aussi le changer sur le site lui-même, sinon vous ne pourrez plus vous connecter.\n\n(L'ancien mot de passe sera gardé dans les notes.)",
        "Saving problem": "Problème d'enregistrement",
        "✔ Everything is saved ({time_str})": "✔ Tout est enregistré (à {time_str})",
        "✔ Saved ({time_str}) — ⚠ .txt copy failed":
            "✔ Enregistré (à {time_str}) — ⚠ copie .txt impossible",
        "Close anyway?": "Fermer quand même ?",
        "The notebook could not be saved.\nClose anyway?":
            "Le carnet n'a pas pu être enregistré.\nFermer quand même ?",
        "✔ Everything is saved": "✔ Tout est enregistré",
        "Copy of cards as .txt: turned off.": "Copie des fiches en .txt : désactivée.",
        "The .txt copy of the cards is now in:\n":
            "La copie .txt des fiches est maintenant dans :\n",
        "No folder chosen. Click “Choose the folder…”.":
            "Aucun dossier choisi. Cliquez sur « Choisir le dossier… ».",
        "Everything is already up to date: no card to create or change.":
            "Tout est déjà à jour : aucune fiche à créer ou à modifier.",
        "{n} document to file (out of {total})": "{n} document à ranger (sur {total})",
        "{n} documents to file (out of {total})": "{n} documents à ranger (sur {total})",
        "✔ Everything is filed ({total} documents).\nClick “All” to see them again.":
            "✔ Tout est rangé ({total} documents).\nCliquez sur « Tout » pour les revoir.",
        "{n} document found": "{n} document trouvé",
        "{n} documents found": "{n} documents trouvés",
        "⚠ {n} old .doc file not read\n   (save it as .docx with Word)":
            "⚠ {n} ancien fichier .doc non lu\n   (à enregistrer en .docx avec Word)",
        "⚠ {n} old .doc files not read\n   (save them as .docx with Word)":
            "⚠ {n} anciens fichiers .doc non lus\n   (à enregistrer en .docx avec Word)",
        "→  See the card": "→  Voir la fiche",
        "“{name}” is already filed in the notebook.\nCreate another card anyway?":
            "« {name} » est déjà rangé dans le carnet.\nEn créer une autre fiche quand même ?",
        "Nothing new to file.\n\n": "Rien de nouveau à ranger.\n\n",
        "File these documents?": "Ranger ces documents ?",
        "File them anyway in “My passwords”?\n(their text will go into the card's Notes)":
            "Les ranger quand même dans « Mes mots de passe » ?\n(leur texte ira dans les Notes de la fiche)",
        "Colour for “{name}”:": "Couleur pour « {name} » :",
        "↻  Another one": "↻  Un autre",
        "✔  Use this password": "✔  Utiliser ce mot de passe",
        "Close": "Fermer",
        "Open Pocket Book": "Ouvrir Pocket Book",
        "Uninstall Pocket Book?": "Désinstaller Pocket Book ?",
        "Also delete all my cards and their backups":
            "Supprimer aussi toutes mes fiches et leurs sauvegardes",
        "Delete the cards?": "Supprimer les fiches ?",
        "Uninstall": "Désinstaller",
        "The notebook was damaged. The backup from {date} has been restored.":
            "Le carnet était abîmé. La sauvegarde du {date} a été reprise.",
        "Text": "Texte",
        "Category:": "Catégorie :",
        "Open on the computer:": "Ouvrir sur l'ordinateur :",
        "The original document": "Le document d'origine",
        "Delete this contact": "Supprimer ce contact",
        "Delete this card": "Supprimer cette fiche",
        "Password": "Mot de passe",
        "✔  Done": "✔  Terminé",
        "Which field should be added to this card?": "Quel champ ajouter à cette fiche ?",
        "Or another field, with your own name (e.g. Customer number, Secret question):":
            "Ou un autre champ, à nommer (ex. : Numéro client, Question secrète) :",
        "File the documents in this folder automatically (new and changed ones), at every start and every minute":
            "Ranger tout seul les documents de ce dossier (nouveaux et modifiés), à chaque ouverture et toutes les minutes",
        "Show:": "Montrer :",
        "Search in the documents": "Chercher dans les documents",
        "Document text:": "Texte du document :",
        "✔ Copied": "✔ Copié",
        "⚠ Could not save!": "⚠ Impossible d'enregistrer !",
        "The notebook could not be saved.\n\n": "Le carnet n'a pas pu être enregistré.\n\n",
        "The notebook is saved, but the .txt copy of the cards could not be made.\n\nThe folder may be disconnected (USB stick, network drive).\n\n":
            "Le carnet est bien enregistré, mais la copie des fiches en .txt n'a pas pu être faite.\n\nLe dossier est peut-être débranché (clé USB, disque réseau).\n\n",
        "Copy of each card as .txt, updated automatically, in:\n":
            "Copie de chaque fiche en .txt, mise à jour toute seule, dans :\n",
        "The file could not be opened.\n\n": "Le fichier n'a pas pu être ouvert.\n\n",
        "The folder could not be opened.\n\n": "Le dossier n'a pas pu être ouvert.\n\n",
        "Documents folder:\n": "Dossier des documents :\n",
        "↻ Documents synced at {time_str}: ": "↻ Documents synchronisés à {time_str} : ",
        "From the documents:\n\n   • ": "Depuis les documents :\n\n   • ",
        "The document could not be opened.\n\n": "Le document n'a pas pu être ouvert.\n\n",
        "Word and text documents": "Documents Word et texte",
        "All files": "Tous les fichiers",
        "The documents themselves are not changed. Continue?":
            "Les documents eux-mêmes ne sont pas modifiés. Continuer ?",
        "{n} document looks like neither a password nor a contact.":
            "{n} document ne ressemble ni à un mot de passe ni à un contact.",
        "{n} documents look like neither a password nor a contact.":
            "{n} documents ne ressemblent ni à un mot de passe ni à un contact.",
        "What does this document contain?": "Que contient ce document ?",
        "Length:": "Longueur :",
        "The old password will be kept in the card's notes.":
            "L'ancien mot de passe sera gardé dans les notes de la fiche.",
        "characters": "caractères",
        "Copying the program failed.": "La copie du programme a échoué.",
        "Put a “Pocket Book” icon on the Desktop": "Mettre une icône « Pocket Book » sur le Bureau",
        "Update": "Mettre à jour",
        "Install": "Installer",
        "Installing…": "Installation en cours…",
        "Try again": "Réessayer",
        "The program and its icons will be removed from this computer.\nYour cards are kept, in:":
            "Le programme et ses icônes vont être retirés de cet ordinateur.\nVos fiches sont gardées, dans :",
        "Continue?": "Continuer ?",
        "Deleted cards": "Fiches supprimées",
        "card": "fiche",
        "Remove “{field}” from this card?\n\nWhat is written in it will be erased:":
            "Retirer « {field} » de cette fiche ?\n\nCe qui est écrit dedans sera effacé :",
        "Search for a contact": "Chercher un contact",
        "Search for a card": "Chercher une fiche",
        "＋  New contact": "＋  Nouveau contact",
        "＋  New card": "＋  Nouvelle fiche",
        "\n\nTip: drag .docx or .txt files (or a whole folder)\nfrom your file manager onto this window to file them all at once.":
            "\n\nAstuce : glissez des fichiers .docx ou .txt (ou tout un dossier)\ndepuis l'Explorateur sur cette fenêtre pour les ranger d'un coup.",
        "Reading documents: {i} of {n}…": "Lecture des documents : {i} sur {n}…",
        "… and {n} more contacts": "… et {n} autres contacts",
        "Update Pocket Book": "Mettre à jour Pocket Book",
        "Install Pocket Book": "Installer Pocket Book",
        "The installation could not be completed": "L'installation n'a pas pu se faire",
        "Pocket Book is installed": "Pocket Book est installé",
        "This installation file can now be put away or deleted.":
            "Ce fichier d'installation peut maintenant être rangé ou supprimé.",
        "All cards, backups and .txt copies in this folder will be permanently erased:":
            "Toutes les fiches, les sauvegardes et les copies .txt de ce dossier seront effacées définitivement :",
        "Open": "Ouvrir",
        "From the document: ": "Venu du document : ",
        "The notebook did not recognise this document. You can still create a card: it will ask whether it is a password or a contact.":
            "Le carnet n'a pas reconnu ce document. Vous pouvez quand même créer une fiche : il vous demandera s'il s'agit d'un mot de passe ou d'un contact.",
        "• Click a name in the list on the left,\n":
            "• Cliquez sur un nom dans la liste à gauche,\n",
        "• or on “New contact” to create one.": "• ou sur « Nouveau contact » pour en créer un.",
        "• or on “New card” to create one.": "• ou sur « Nouvelle fiche » pour en créer une.",
        "Reading failed.": "La lecture a échoué.",
        "The documents could not be read.\n\n": "Les documents n'ont pas pu être lus.\n\n",
        "{n} contact  →  “My contacts”": "{n} contact  →  « Mes contacts »",
        "{n} contacts  →  “My contacts”": "{n} contacts  →  « Mes contacts »",
        "No contact is selected.\n\n": "Aucun contact n'est choisi.\n\n",
        "No card is selected.\n\n": "Aucune fiche n'est choisie.\n\n",
        "{n} password  →  “My passwords”": "{n} mot de passe  →  « Mes mots de passe »",
        "{n} passwords  →  “My passwords”": "{n} mots de passe  →  « Mes mots de passe »",
        "The notebook will file:": "Le carnet va ranger :",
        "Category": "Catégorie",
        "Username": "Identifiant",
        "Email address": "Adresse e-mail",
        "Mobile": "Portable",
        "Landline": "Téléphone fixe",
        "Address": "Adresse",
        "Birthday": "Anniversaire",
        "Contact": "Contact",
        "?": "?",
        "a password": "un mot de passe",
        "a contact": "un contact",
        "not recognised": "non reconnu",
        "Blue": "Bleu",
        "Green": "Vert",
        "Yellow": "Jaune",
        "Orange": "Orange",
        "Red": "Rouge",
        "Purple": "Violet",
        "Pink": "Rose",
        "Turquoise": "Turquoise",
        "Grey": "Gris",
        "Brown": "Marron",
        "Bank": "Banque",
        "Administration": "Administration",
        "Health": "Santé",
        "Email": "Messagerie",
        "Shopping": "Achats",
        "Bills": "Factures",
        "Leisure": "Loisirs",
        "Family": "Famille",
        "Work": "Travail",
        "Light": "Clair",
        "Dark": "Sombre",
        "High contrast": "Contraste fort",
        "Soft sepia": "Sépia doux",
        "Other": "Autres",
        "About": "À propos",
        "Pocket Book {version} — works entirely without internet: nothing leaves this computer.":
            "Pocket Book {version} — fonctionne entièrement sans internet : rien ne quitte cet ordinateur.",
        "Your data is here:": "Vos données sont ici :",
        "Open the data folder": "Ouvrir le dossier des données",
        "Uninstall…": "Désinstaller…",
    },
    "es": {
        "(none)": "(ninguna)",
        "All categories": "Todas",
        "Pocket Book has been uninstalled.": "Pocket Book se ha desinstalado.",
        "File type not supported": "Tipo de archivo no compatible",
        "This file is rewritten after every change: edit the card in the notebook.":
            "Este archivo se reescribe con cada cambio: modifique la ficha en el cuaderno.",
        "Delete the category “{name}”?": "¿Eliminar la categoría «{name}»?",
        "Category colour": "Color de la categoría",
        "What kind of document?": "¿Qué tipo de documento?",
        "Installing Pocket Book": "Instalación de Pocket Book",
        "Uninstall Pocket Book": "Desinstalar Pocket Book",
        "Untitled": "Sin nombre",
        "New contact": "Nuevo contacto",
        "New card": "Nueva ficha",
        "%m/%d/%Y at %H:%M": "%d/%m/%Y a las %H:%M",
        "Notes": "Notas",
        "Automatic copy made by Pocket Book (card changed on {date}).":
            "Copia automática hecha por Pocket Book (ficha modificada el {date}).",
        "Automatic copy made by Pocket Book.": "Copia automática hecha por Pocket Book.",
        "Name": "Nombre",
        "Copy": "Copiar",
        "✎  Edit by hand": "✎  Modificar a mano",
        "Add a field": "Añadir un campo",
        "Categories": "Categorías",
        "Categories are used to sort cards. Each one has its own colour, shown in the list of cards.":
            "Las categorías sirven para ordenar las fichas. Cada una tiene su color, que aparece en la lista de fichas.",
        "Language": "Idioma",
        "Screen colours": "Colores de la pantalla",
        "Choose whatever is easiest to read.": "Elija lo que le resulte más cómodo de leer.",
        "Copy of cards as .txt": "Copia de las fichas en .txt",
        "Each card is copied into a .txt file that updates itself. Make changes in the notebook, not in the .txt files.":
            "Cada ficha se copia en un archivo .txt que se actualiza solo. Los cambios se hacen en el cuaderno, no en los .txt.",
        "New category": "Nueva categoría",
        "Name of the new category:": "Nombre de la nueva categoría:",
        "Rename the category": "Cambiar el nombre de la categoría",
        "New name:": "Nuevo nombre:",
        "＋  Create a card from this document": "＋  Crear una ficha con este documento",
        "{n} contact": "{n} contacto",
        "{n} contacts": "{n} contactos",
        "{n} card": "{n} ficha",
        "{n} cards": "{n} fichas",
        "Do you really want to delete the contact “{name}”?":
            "¿Seguro que quiere eliminar el contacto «{name}»?",
        "Do you really want to delete the card “{name}”?":
            "¿Seguro que quiere eliminar la ficha «{name}»?",
        "Old password (replaced on {date}): {old}":
            "Contraseña anterior (cambiada el {date}): {old}",
        "No folder chosen.": "Ninguna carpeta elegida.",
        "This document contained {n} contacts: they have all been created.":
            "Este documento contenía {n} contactos: se han creado todos.",
        "The card was filled in from the document.":
            "La ficha se ha rellenado a partir del documento.",
        "Check that each piece of information is in the right place.":
            "Compruebe que cada dato está en su sitio.",
        "Card created": "Ficha creada",
        "All filed!": "¡Todo ordenado!",
        "{n} card created.": "{n} ficha creada.",
        "{n} cards created.": "{n} fichas creadas.",
        "Create a new password": "Crear una contraseña nueva",
        "A new version of Pocket Book will replace the old one.\nYour cards are not touched.":
            "Una nueva versión de Pocket Book va a sustituir a la anterior.\nSus fichas no se tocan.",
        "To open it, double-click the “Pocket Book” icon on the Desktop\n(or look for “Pocket Book” in the applications menu).":
            "Para abrirlo, haga doble clic en el icono «Pocket Book» del Escritorio\n(o busque «Pocket Book» en el menú de aplicaciones).",
        "To open it, look for “Pocket Book” in the applications menu.":
            "Para abrirlo, busque «Pocket Book» en el menú de aplicaciones.",
        "The notebook was damaged and no backup could be read. A copy was kept: {file_path}":
            "El cuaderno estaba dañado y no se pudo leer ninguna copia de seguridad. Se ha guardado una copia: {file_path}",
        "My passwords": "Mis contraseñas",
        "My contacts": "Mis contactos",
        "My documents": "Mis documentos",
        "First click on a category in the list.": "Primero haga clic en una categoría de la lista.",
        "The category “{name}” already exists.": "La categoría «{name}» ya existe.",
        "{n} card will no longer have a category (the card itself is not deleted).":
            "{n} ficha se quedará sin categoría (la ficha no se elimina).",
        "{n} cards will no longer have a category (the cards themselves are not deleted).":
            "{n} fichas se quedarán sin categoría (las fichas no se eliminan).",
        "Delete the category?": "¿Eliminar la categoría?",
        "↻  Sync now": "↻  Sincronizar ahora",
        "Choose the folder…": "Elegir la carpeta…",
        "Import files…": "Importar archivos…",
        "To file": "Por ordenar",
        "All": "Todo",
        "Passwords": "Contraseñas",
        "Contacts": "Contactos",
        "Not recognised": "No reconocidos",
        "Choose a document in the list.": "Elija un documento de la lista.",
        "This document is never changed by the notebook.":
            "El cuaderno nunca modifica este documento.",
        "{n} contact found": "{n} contacto encontrado",
        "{n} contacts found": "{n} contactos encontrados",
        "{n} card found": "{n} ficha encontrada",
        "{n} cards found": "{n} fichas encontradas",
        ", from A to Z": ", de la A a la Z",
        " starting with {letter}": " con la letra {letter}",
        "Delete?": "¿Eliminar?",
        "Website": "Sitio web",
        "No website address is written on this card.":
            "Esta ficha no tiene ninguna dirección de sitio web.",
        "%m/%d/%Y": "%d/%m/%Y",
        "✎ Editing…": "✎ Modificando…",
        "Which folder should hold the .txt copy of the cards?":
            "¿En qué carpeta guardar la copia .txt de las fichas?",
        "Choose a folder other than the one with the original documents\n(for example a “Cards as text” subfolder).":
            "Elija una carpeta distinta de la de los documentos originales\n(por ejemplo una subcarpeta «Fichas en texto»).",
        "\n\nThe old folder has not been changed.": "\n\nLa carpeta anterior no se ha modificado.",
        "This file does not exist (or no longer exists) on the computer.":
            "Este archivo no existe (o ya no existe) en el ordenador.",
        "Where are your documents kept?": "¿Dónde están guardados sus documentos?",
        "First choose the folder where your documents are kept.":
            "Primero elija la carpeta donde están guardados sus documentos.",
        "Reading documents…": "Leyendo los documentos…",
        "{n} card created": "{n} ficha creada",
        "{n} cards created": "{n} fichas creadas",
        "{n} card updated": "{n} actualizada",
        "{n} cards updated": "{n} actualizadas",
        "{n} to check (⚠ in the notes)": "{n} por revisar (⚠ en las notas)",
        "Sync": "Sincronización",
        "{n} document": "{n} documento",
        "{n} documents": "{n} documentos",
        "✔ = already filed in the notebook": "✔ = ya ordenado en el cuaderno",
        "Recognised as: {kind}   —   this document is never changed.":
            "Reconocido como: {kind}   —   este documento nunca se modifica.",
        "(Empty document)": "(Documento vacío)",
        "Already filed in the notebook:": "Ya ordenado en el cuaderno:",
        "What the notebook understood:": "Lo que el cuaderno ha entendido:",
        "First choose a document in the list.": "Primero elija un documento de la lista.",
        "Choose the documents to file (several at once is fine)":
            "Elija los documentos que quiere ordenar (puede elegir varios)",
        "{n} document already filed: skipped.": "{n} documento ya ordenado: omitido.",
        "{n} documents already filed: skipped.": "{n} documentos ya ordenados: omitidos.",
        "{n} old .doc file not read (save it as .docx with Word).":
            "{n} archivo .doc antiguo sin leer (guárdelo como .docx con Word).",
        "{n} old .doc files not read (save them as .docx with Word).":
            "{n} archivos .doc antiguos sin leer (guárdelos como .docx con Word).",
        "{n} file of another type skipped.": "{n} archivo de otro tipo omitido.",
        "{n} files of another type skipped.": "{n} archivos de otro tipo omitidos.",
        "{n} document not recognised: {names}": "{n} documento no reconocido: {names}",
        "{n} documents not recognised: {names}": "{n} documentos no reconocidos: {names}",
        "Documents not recognised": "Documentos no reconocidos",
        "Cancel": "Cancelar",
        "✔  OK": "✔  Aceptar",
        "A password": "Una contraseña",
        "A contact": "Un contacto",
        "Easy to read (words)": "Fácil de leer (palabras)",
        "Very strong (letters and symbols)": "Muy segura (letras y símbolos)",
        "words": "palabras",
        "Passwords and contacts, without internet": "Contraseñas y contactos, sin internet",
        "Pocket Book is probably still open.\nClose it, then click “Install” again.":
            "Pocket Book probablemente sigue abierto.\nCiérrelo y vuelva a hacer clic en «Instalar».",
        "Your cards are still in:": "Sus fichas siguen en:",
        "Pocket Book will be installed on this computer.\nIt works without internet: nothing leaves the computer.\nYour cards will be kept in:":
            "Pocket Book se va a instalar en este ordenador.\nFunciona sin internet: nada sale del ordenador.\nSus fichas se guardarán en:",
        "Cards as text": "Fichas en texto",
        "⚠ The document “{name}” changed on {date}: check this card (it was not replaced).":
            "⚠ El documento «{name}» cambió el {date}: revise esta ficha (no se ha sustituido).",
        "Could not read this document ({error}).": "No se pudo leer este documento ({error}).",
        "Settings": "Ajustes",
        "A": "A",
        "Save now": "Guardar ahora",
        "Field": "Campo",
        "＋  Add a field": "＋  Añadir un campo",
        "The .txt copy": "La copia .txt",
        "The folder": "La carpeta",
        "↻  Create a new password": "↻  Crear una contraseña nueva",
        "＋  Add this field": "＋  Añadir este campo",
        "Remove the field?": "¿Quitar el campo?",
        "＋  New": "＋  Nueva",
        "Rename": "Cambiar nombre",
        "Colour…": "Color…",
        "Delete": "Eliminar",
        "Change folder…": "Cambiar de carpeta…",
        "Open the folder": "Abrir la carpeta",
        "Open in Word": "Abrir en Word",
        "A copy stays in today's backups.": "Queda una copia en las copias de seguridad del día.",
        "Change the password?": "¿Cambiar la contraseña?",
        "Do you really want to change the password for “{name}”?\n\nCareful: this only changes the notebook. You must also change it on the website itself, otherwise you will no longer be able to log in.\n\n(The old password will be kept in the notes.)":
            "¿Seguro que quiere cambiar la contraseña de «{name}»?\n\nAtención: esto solo cambia el cuaderno. También hay que cambiarla en el propio sitio web; si no, ya no podrá conectarse.\n\n(La contraseña anterior se guardará en las notas.)",
        "Saving problem": "Problema al guardar",
        "✔ Everything is saved ({time_str})": "✔ Todo está guardado ({time_str})",
        "✔ Saved ({time_str}) — ⚠ .txt copy failed": "✔ Guardado ({time_str}) — ⚠ copia .txt imposible",
        "Close anyway?": "¿Cerrar de todos modos?",
        "The notebook could not be saved.\nClose anyway?":
            "No se pudo guardar el cuaderno.\n¿Cerrar de todos modos?",
        "✔ Everything is saved": "✔ Todo está guardado",
        "Copy of cards as .txt: turned off.": "Copia de las fichas en .txt: desactivada.",
        "The .txt copy of the cards is now in:\n": "La copia .txt de las fichas está ahora en:\n",
        "No folder chosen. Click “Choose the folder…”.":
            "Ninguna carpeta elegida. Haga clic en «Elegir la carpeta…».",
        "Everything is already up to date: no card to create or change.":
            "Todo está al día: ninguna ficha que crear o modificar.",
        "{n} document to file (out of {total})": "{n} documento por ordenar (de {total})",
        "{n} documents to file (out of {total})": "{n} documentos por ordenar (de {total})",
        "✔ Everything is filed ({total} documents).\nClick “All” to see them again.":
            "✔ Todo está ordenado ({total} documentos).\nHaga clic en «Todo» para volver a verlos.",
        "{n} document found": "{n} documento encontrado",
        "{n} documents found": "{n} documentos encontrados",
        "⚠ {n} old .doc file not read\n   (save it as .docx with Word)":
            "⚠ {n} archivo .doc antiguo sin leer\n   (guárdelo como .docx con Word)",
        "⚠ {n} old .doc files not read\n   (save them as .docx with Word)":
            "⚠ {n} archivos .doc antiguos sin leer\n   (guárdelos como .docx con Word)",
        "→  See the card": "→  Ver la ficha",
        "“{name}” is already filed in the notebook.\nCreate another card anyway?":
            "«{name}» ya está ordenado en el cuaderno.\n¿Crear otra ficha de todos modos?",
        "Nothing new to file.\n\n": "Nada nuevo que ordenar.\n\n",
        "File these documents?": "¿Ordenar estos documentos?",
        "File them anyway in “My passwords”?\n(their text will go into the card's Notes)":
            "¿Ordenarlos de todos modos en «Mis contraseñas»?\n(su texto irá a las Notas de la ficha)",
        "Colour for “{name}”:": "Color para «{name}»:",
        "↻  Another one": "↻  Otra",
        "✔  Use this password": "✔  Usar esta contraseña",
        "Close": "Cerrar",
        "Open Pocket Book": "Abrir Pocket Book",
        "Uninstall Pocket Book?": "¿Desinstalar Pocket Book?",
        "Also delete all my cards and their backups":
            "Eliminar también todas mis fichas y sus copias de seguridad",
        "Delete the cards?": "¿Eliminar las fichas?",
        "Uninstall": "Desinstalar",
        "The notebook was damaged. The backup from {date} has been restored.":
            "El cuaderno estaba dañado. Se ha recuperado la copia de seguridad del {date}.",
        "Text": "Texto",
        "Category:": "Categoría:",
        "Open on the computer:": "Abrir en el ordenador:",
        "The original document": "El documento original",
        "Delete this contact": "Eliminar este contacto",
        "Delete this card": "Eliminar esta ficha",
        "Password": "Contraseña",
        "✔  Done": "✔  Hecho",
        "Which field should be added to this card?": "¿Qué campo añadir a esta ficha?",
        "Or another field, with your own name (e.g. Customer number, Secret question):":
            "U otro campo, con el nombre que quiera (p. ej.: Número de cliente, Pregunta secreta):",
        "File the documents in this folder automatically (new and changed ones), at every start and every minute":
            "Ordenar solos los documentos de esta carpeta (nuevos y modificados), al abrir y cada minuto",
        "Show:": "Mostrar:",
        "Search in the documents": "Buscar en los documentos",
        "Document text:": "Texto del documento:",
        "✔ Copied": "✔ Copiado",
        "⚠ Could not save!": "⚠ ¡No se pudo guardar!",
        "The notebook could not be saved.\n\n": "No se pudo guardar el cuaderno.\n\n",
        "The notebook is saved, but the .txt copy of the cards could not be made.\n\nThe folder may be disconnected (USB stick, network drive).\n\n":
            "El cuaderno está guardado, pero no se pudo hacer la copia .txt de las fichas.\n\nQuizás la carpeta esté desconectada (memoria USB, disco de red).\n\n",
        "Copy of each card as .txt, updated automatically, in:\n":
            "Copia de cada ficha en .txt, actualizada sola, en:\n",
        "The file could not be opened.\n\n": "No se pudo abrir el archivo.\n\n",
        "The folder could not be opened.\n\n": "No se pudo abrir la carpeta.\n\n",
        "Documents folder:\n": "Carpeta de los documentos:\n",
        "↻ Documents synced at {time_str}: ": "↻ Documentos sincronizados a las {time_str}: ",
        "From the documents:\n\n   • ": "A partir de los documentos:\n\n   • ",
        "The document could not be opened.\n\n": "No se pudo abrir el documento.\n\n",
        "Word and text documents": "Documentos de Word y de texto",
        "All files": "Todos los archivos",
        "The documents themselves are not changed. Continue?":
            "Los documentos en sí no se modifican. ¿Continuar?",
        "{n} document looks like neither a password nor a contact.":
            "{n} documento no parece ni una contraseña ni un contacto.",
        "{n} documents look like neither a password nor a contact.":
            "{n} documentos no parecen ni una contraseña ni un contacto.",
        "What does this document contain?": "¿Qué contiene este documento?",
        "Length:": "Longitud:",
        "The old password will be kept in the card's notes.":
            "La contraseña anterior se guardará en las notas de la ficha.",
        "characters": "caracteres",
        "Copying the program failed.": "No se pudo copiar el programa.",
        "Put a “Pocket Book” icon on the Desktop": "Poner un icono «Pocket Book» en el Escritorio",
        "Update": "Actualizar",
        "Install": "Instalar",
        "Installing…": "Instalando…",
        "Try again": "Reintentar",
        "The program and its icons will be removed from this computer.\nYour cards are kept, in:":
            "El programa y sus iconos se quitarán de este ordenador.\nSus fichas se conservan, en:",
        "Continue?": "¿Continuar?",
        "Deleted cards": "Fichas eliminadas",
        "card": "ficha",
        "Remove “{field}” from this card?\n\nWhat is written in it will be erased:":
            "¿Quitar «{field}» de esta ficha?\n\nLo que tiene escrito se borrará:",
        "Search for a contact": "Buscar un contacto",
        "Search for a card": "Buscar una ficha",
        "＋  New contact": "＋  Nuevo contacto",
        "＋  New card": "＋  Nueva ficha",
        "\n\nTip: drag .docx or .txt files (or a whole folder)\nfrom your file manager onto this window to file them all at once.":
            "\n\nConsejo: arrastre archivos .docx o .txt (o una carpeta entera)\ndesde el explorador a esta ventana para ordenarlos de una vez.",
        "Reading documents: {i} of {n}…": "Leyendo los documentos: {i} de {n}…",
        "… and {n} more contacts": "… y {n} contactos más",
        "Update Pocket Book": "Actualizar Pocket Book",
        "Install Pocket Book": "Instalar Pocket Book",
        "The installation could not be completed": "No se pudo realizar la instalación",
        "Pocket Book is installed": "Pocket Book está instalado",
        "This installation file can now be put away or deleted.":
            "Este archivo de instalación ya se puede guardar o eliminar.",
        "All cards, backups and .txt copies in this folder will be permanently erased:":
            "Todas las fichas, copias de seguridad y copias .txt de esta carpeta se borrarán definitivamente:",
        "Open": "Abrir",
        "From the document: ": "Procede del documento: ",
        "The notebook did not recognise this document. You can still create a card: it will ask whether it is a password or a contact.":
            "El cuaderno no ha reconocido este documento. Aun así puede crear una ficha: le preguntará si es una contraseña o un contacto.",
        "• Click a name in the list on the left,\n":
            "• Haga clic en un nombre de la lista de la izquierda,\n",
        "• or on “New contact” to create one.": "• o en «Nuevo contacto» para crear uno.",
        "• or on “New card” to create one.": "• o en «Nueva ficha» para crear una.",
        "Reading failed.": "La lectura ha fallado.",
        "The documents could not be read.\n\n": "No se pudieron leer los documentos.\n\n",
        "{n} contact  →  “My contacts”": "{n} contacto  →  «Mis contactos»",
        "{n} contacts  →  “My contacts”": "{n} contactos  →  «Mis contactos»",
        "No contact is selected.\n\n": "No hay ningún contacto elegido.\n\n",
        "No card is selected.\n\n": "No hay ninguna ficha elegida.\n\n",
        "{n} password  →  “My passwords”": "{n} contraseña  →  «Mis contraseñas»",
        "{n} passwords  →  “My passwords”": "{n} contraseñas  →  «Mis contraseñas»",
        "The notebook will file:": "El cuaderno va a ordenar:",
        "Category": "Categoría",
        "Username": "Usuario",
        "Email address": "Correo electrónico",
        "Mobile": "Móvil",
        "Landline": "Teléfono fijo",
        "Address": "Dirección",
        "Birthday": "Cumpleaños",
        "Contact": "Contacto",
        "?": "?",
        "a password": "una contraseña",
        "a contact": "un contacto",
        "not recognised": "no reconocido",
        "Blue": "Azul",
        "Green": "Verde",
        "Yellow": "Amarillo",
        "Orange": "Naranja",
        "Red": "Rojo",
        "Purple": "Morado",
        "Pink": "Rosa",
        "Turquoise": "Turquesa",
        "Grey": "Gris",
        "Brown": "Marrón",
        "Bank": "Banco",
        "Administration": "Administración",
        "Health": "Salud",
        "Email": "Correo",
        "Shopping": "Compras",
        "Bills": "Facturas",
        "Leisure": "Ocio",
        "Family": "Familia",
        "Work": "Trabajo",
        "Light": "Claro",
        "Dark": "Oscuro",
        "High contrast": "Alto contraste",
        "Soft sepia": "Sepia suave",
        "Other": "Otros",
        "About": "Acerca de",
        "Pocket Book {version} — works entirely without internet: nothing leaves this computer.":
            "Pocket Book {version} — funciona totalmente sin internet: nada sale de este ordenador.",
        "Your data is here:": "Sus datos están aquí:",
        "Open the data folder": "Abrir la carpeta de datos",
        "Uninstall…": "Desinstalar…",
    },
    "de": {
        "(none)": "(keine)",
        "All categories": "Alle",
        "Pocket Book has been uninstalled.": "Pocket Book wurde deinstalliert.",
        "File type not supported": "Dateityp wird nicht unterstützt",
        "This file is rewritten after every change: edit the card in the notebook.":
            "Diese Datei wird bei jeder Änderung neu geschrieben: Bearbeiten Sie die Karte im Notizbuch.",
        "Delete the category “{name}”?": "Kategorie „{name}“ löschen?",
        "Category colour": "Farbe der Kategorie",
        "What kind of document?": "Was für ein Dokument ist das?",
        "Installing Pocket Book": "Installation von Pocket Book",
        "Uninstall Pocket Book": "Pocket Book deinstallieren",
        "Untitled": "Ohne Namen",
        "New contact": "Neuer Kontakt",
        "New card": "Neue Karte",
        "%m/%d/%Y at %H:%M": "%d.%m.%Y um %H:%M",
        "Notes": "Notizen",
        "Automatic copy made by Pocket Book (card changed on {date}).":
            "Automatische Kopie von Pocket Book (Karte geändert am {date}).",
        "Automatic copy made by Pocket Book.": "Automatische Kopie von Pocket Book.",
        "Name": "Name",
        "Copy": "Kopieren",
        "✎  Edit by hand": "✎  Von Hand ändern",
        "Add a field": "Feld hinzufügen",
        "Categories": "Kategorien",
        "Categories are used to sort cards. Each one has its own colour, shown in the list of cards.":
            "Kategorien dienen zum Sortieren der Karten. Jede hat ihre eigene Farbe, die in der Kartenliste erscheint.",
        "Language": "Sprache",
        "Screen colours": "Bildschirmfarben",
        "Choose whatever is easiest to read.": "Wählen Sie, was sich am angenehmsten lesen lässt.",
        "Copy of cards as .txt": "Kopie der Karten als .txt",
        "Each card is copied into a .txt file that updates itself. Make changes in the notebook, not in the .txt files.":
            "Jede Karte wird in eine .txt-Datei kopiert, die sich selbst aktualisiert. Änderungen macht man im Notizbuch, nicht in den .txt-Dateien.",
        "New category": "Neue Kategorie",
        "Name of the new category:": "Name der neuen Kategorie:",
        "Rename the category": "Kategorie umbenennen",
        "New name:": "Neuer Name:",
        "＋  Create a card from this document": "＋  Karte aus diesem Dokument erstellen",
        "{n} contact": "{n} Kontakt",
        "{n} contacts": "{n} Kontakte",
        "{n} card": "{n} Karte",
        "{n} cards": "{n} Karten",
        "Do you really want to delete the contact “{name}”?":
            "Möchten Sie den Kontakt „{name}“ wirklich löschen?",
        "Do you really want to delete the card “{name}”?":
            "Möchten Sie die Karte „{name}“ wirklich löschen?",
        "Old password (replaced on {date}): {old}":
            "Altes Passwort (ersetzt am {date}): {old}",
        "No folder chosen.": "Kein Ordner gewählt.",
        "This document contained {n} contacts: they have all been created.":
            "Dieses Dokument enthielt {n} Kontakte: Alle wurden erstellt.",
        "The card was filled in from the document.": "Die Karte wurde aus dem Dokument ausgefüllt.",
        "Check that each piece of information is in the right place.":
            "Prüfen Sie, ob jede Angabe an der richtigen Stelle steht.",
        "Card created": "Karte erstellt",
        "All filed!": "Alles eingeordnet!",
        "{n} card created.": "{n} Karte erstellt.",
        "{n} cards created.": "{n} Karten erstellt.",
        "Create a new password": "Neues Passwort erstellen",
        "A new version of Pocket Book will replace the old one.\nYour cards are not touched.":
            "Eine neue Version von Pocket Book ersetzt die alte.\nIhre Karten bleiben unberührt.",
        "To open it, double-click the “Pocket Book” icon on the Desktop\n(or look for “Pocket Book” in the applications menu).":
            "Zum Öffnen doppelklicken Sie auf das Symbol „Pocket Book“ auf dem Desktop\n(oder suchen Sie „Pocket Book“ im Anwendungsmenü).",
        "To open it, look for “Pocket Book” in the applications menu.":
            "Zum Öffnen suchen Sie „Pocket Book“ im Anwendungsmenü.",
        "The notebook was damaged and no backup could be read. A copy was kept: {file_path}":
            "Das Notizbuch war beschädigt und keine Sicherung konnte gelesen werden. Eine Kopie wurde aufbewahrt: {file_path}",
        "My passwords": "Meine Passwörter",
        "My contacts": "Meine Kontakte",
        "My documents": "Meine Dokumente",
        "First click on a category in the list.":
            "Klicken Sie zuerst auf eine Kategorie in der Liste.",
        "The category “{name}” already exists.": "Die Kategorie „{name}“ gibt es schon.",
        "{n} card will no longer have a category (the card itself is not deleted).":
            "{n} Karte hat dann keine Kategorie mehr (die Karte selbst wird nicht gelöscht).",
        "{n} cards will no longer have a category (the cards themselves are not deleted).":
            "{n} Karten haben dann keine Kategorie mehr (die Karten selbst werden nicht gelöscht).",
        "Delete the category?": "Kategorie löschen?",
        "↻  Sync now": "↻  Jetzt abgleichen",
        "Choose the folder…": "Ordner wählen…",
        "Import files…": "Dateien importieren…",
        "To file": "Einzuordnen",
        "All": "Alle",
        "Passwords": "Passwörter",
        "Contacts": "Kontakte",
        "Not recognised": "Nicht erkannt",
        "Choose a document in the list.": "Wählen Sie ein Dokument in der Liste.",
        "This document is never changed by the notebook.":
            "Dieses Dokument wird vom Notizbuch nie verändert.",
        "{n} contact found": "{n} Kontakt gefunden",
        "{n} contacts found": "{n} Kontakte gefunden",
        "{n} card found": "{n} Karte gefunden",
        "{n} cards found": "{n} Karten gefunden",
        ", from A to Z": ", von A bis Z",
        " starting with {letter}": " mit dem Buchstaben {letter}",
        "Delete?": "Löschen?",
        "Website": "Webseite",
        "No website address is written on this card.":
            "Auf dieser Karte ist keine Webseite eingetragen.",
        "%m/%d/%Y": "%d.%m.%Y",
        "✎ Editing…": "✎ Wird geändert…",
        "Which folder should hold the .txt copy of the cards?":
            "In welchem Ordner soll die .txt-Kopie der Karten liegen?",
        "Choose a folder other than the one with the original documents\n(for example a “Cards as text” subfolder).":
            "Wählen Sie einen anderen Ordner als den der Originaldokumente\n(zum Beispiel einen Unterordner „Karten als Text“).",
        "\n\nThe old folder has not been changed.": "\n\nDer alte Ordner wurde nicht verändert.",
        "This file does not exist (or no longer exists) on the computer.":
            "Diese Datei existiert (nicht mehr) auf dem Computer.",
        "Where are your documents kept?": "Wo sind Ihre Dokumente gespeichert?",
        "First choose the folder where your documents are kept.":
            "Wählen Sie zuerst den Ordner, in dem Ihre Dokumente liegen.",
        "Reading documents…": "Dokumente werden gelesen…",
        "{n} card created": "{n} Karte erstellt",
        "{n} cards created": "{n} Karten erstellt",
        "{n} card updated": "{n} aktualisiert",
        "{n} cards updated": "{n} aktualisiert",
        "{n} to check (⚠ in the notes)": "{n} zu prüfen (⚠ in den Notizen)",
        "Sync": "Abgleich",
        "{n} document": "{n} Dokument",
        "{n} documents": "{n} Dokumente",
        "✔ = already filed in the notebook": "✔ = schon im Notizbuch eingeordnet",
        "Recognised as: {kind}   —   this document is never changed.":
            "Erkannt als: {kind}   —   dieses Dokument wird nie verändert.",
        "(Empty document)": "(Leeres Dokument)",
        "Already filed in the notebook:": "Schon im Notizbuch eingeordnet:",
        "What the notebook understood:": "Was das Notizbuch verstanden hat:",
        "First choose a document in the list.": "Wählen Sie zuerst ein Dokument in der Liste.",
        "Choose the documents to file (several at once is fine)":
            "Wählen Sie die einzuordnenden Dokumente (mehrere auf einmal möglich)",
        "{n} document already filed: skipped.": "{n} Dokument schon eingeordnet: übersprungen.",
        "{n} documents already filed: skipped.": "{n} Dokumente schon eingeordnet: übersprungen.",
        "{n} old .doc file not read (save it as .docx with Word).":
            "{n} alte .doc-Datei nicht gelesen (in Word als .docx speichern).",
        "{n} old .doc files not read (save them as .docx with Word).":
            "{n} alte .doc-Dateien nicht gelesen (in Word als .docx speichern).",
        "{n} file of another type skipped.": "{n} Datei anderen Typs übersprungen.",
        "{n} files of another type skipped.": "{n} Dateien anderen Typs übersprungen.",
        "{n} document not recognised: {names}": "{n} Dokument nicht erkannt: {names}",
        "{n} documents not recognised: {names}": "{n} Dokumente nicht erkannt: {names}",
        "Documents not recognised": "Nicht erkannte Dokumente",
        "Cancel": "Abbrechen",
        "✔  OK": "✔  OK",
        "A password": "Ein Passwort",
        "A contact": "Ein Kontakt",
        "Easy to read (words)": "Leicht zu lesen (Wörter)",
        "Very strong (letters and symbols)": "Sehr sicher (Buchstaben und Zeichen)",
        "words": "Wörter",
        "Passwords and contacts, without internet": "Passwörter und Kontakte, ohne Internet",
        "Pocket Book is probably still open.\nClose it, then click “Install” again.":
            "Pocket Book ist wahrscheinlich noch geöffnet.\nSchließen Sie es und klicken Sie erneut auf „Installieren“.",
        "Your cards are still in:": "Ihre Karten befinden sich weiterhin in:",
        "Pocket Book will be installed on this computer.\nIt works without internet: nothing leaves the computer.\nYour cards will be kept in:":
            "Pocket Book wird auf diesem Computer installiert.\nEs funktioniert ohne Internet: Nichts verlässt den Computer.\nIhre Karten werden gespeichert in:",
        "Cards as text": "Karten als Text",
        "⚠ The document “{name}” changed on {date}: check this card (it was not replaced).":
            "⚠ Das Dokument „{name}“ hat sich am {date} geändert: Prüfen Sie diese Karte (sie wurde nicht ersetzt).",
        "Could not read this document ({error}).":
            "Dieses Dokument konnte nicht gelesen werden ({error}).",
        "Settings": "Einstellungen",
        "A": "A",
        "Save now": "Jetzt speichern",
        "Field": "Feld",
        "＋  Add a field": "＋  Feld hinzufügen",
        "The .txt copy": "Die .txt-Kopie",
        "The folder": "Den Ordner",
        "↻  Create a new password": "↻  Neues Passwort erstellen",
        "＋  Add this field": "＋  Dieses Feld hinzufügen",
        "Remove the field?": "Feld entfernen?",
        "＋  New": "＋  Neu",
        "Rename": "Umbenennen",
        "Colour…": "Farbe…",
        "Delete": "Löschen",
        "Change folder…": "Ordner ändern…",
        "Open the folder": "Ordner öffnen",
        "Open in Word": "In Word öffnen",
        "A copy stays in today's backups.": "Eine Kopie bleibt in den heutigen Sicherungen.",
        "Change the password?": "Passwort ändern?",
        "Do you really want to change the password for “{name}”?\n\nCareful: this only changes the notebook. You must also change it on the website itself, otherwise you will no longer be able to log in.\n\n(The old password will be kept in the notes.)":
            "Möchten Sie das Passwort für „{name}“ wirklich ändern?\n\nAchtung: Das ändert nur das Notizbuch. Sie müssen es auch auf der Webseite selbst ändern, sonst können Sie sich nicht mehr anmelden.\n\n(Das alte Passwort wird in den Notizen aufbewahrt.)",
        "Saving problem": "Problem beim Speichern",
        "✔ Everything is saved ({time_str})": "✔ Alles gespeichert ({time_str})",
        "✔ Saved ({time_str}) — ⚠ .txt copy failed":
            "✔ Gespeichert ({time_str}) — ⚠ .txt-Kopie fehlgeschlagen",
        "Close anyway?": "Trotzdem schließen?",
        "The notebook could not be saved.\nClose anyway?":
            "Das Notizbuch konnte nicht gespeichert werden.\nTrotzdem schließen?",
        "✔ Everything is saved": "✔ Alles gespeichert",
        "Copy of cards as .txt: turned off.": "Kopie der Karten als .txt: ausgeschaltet.",
        "The .txt copy of the cards is now in:\n": "Die .txt-Kopie der Karten liegt jetzt in:\n",
        "No folder chosen. Click “Choose the folder…”.":
            "Kein Ordner gewählt. Klicken Sie auf „Ordner wählen…“.",
        "Everything is already up to date: no card to create or change.":
            "Alles ist aktuell: keine Karte zu erstellen oder zu ändern.",
        "{n} document to file (out of {total})": "{n} Dokument einzuordnen (von {total})",
        "{n} documents to file (out of {total})": "{n} Dokumente einzuordnen (von {total})",
        "✔ Everything is filed ({total} documents).\nClick “All” to see them again.":
            "✔ Alles eingeordnet ({total} Dokumente).\nKlicken Sie auf „Alle“, um sie wieder zu sehen.",
        "{n} document found": "{n} Dokument gefunden",
        "{n} documents found": "{n} Dokumente gefunden",
        "⚠ {n} old .doc file not read\n   (save it as .docx with Word)":
            "⚠ {n} alte .doc-Datei nicht gelesen\n   (in Word als .docx speichern)",
        "⚠ {n} old .doc files not read\n   (save them as .docx with Word)":
            "⚠ {n} alte .doc-Dateien nicht gelesen\n   (in Word als .docx speichern)",
        "→  See the card": "→  Karte ansehen",
        "“{name}” is already filed in the notebook.\nCreate another card anyway?":
            "„{name}“ ist schon im Notizbuch eingeordnet.\nTrotzdem eine weitere Karte erstellen?",
        "Nothing new to file.\n\n": "Nichts Neues einzuordnen.\n\n",
        "File these documents?": "Diese Dokumente einordnen?",
        "File them anyway in “My passwords”?\n(their text will go into the card's Notes)":
            "Trotzdem unter „Meine Passwörter“ einordnen?\n(ihr Text kommt in die Notizen der Karte)",
        "Colour for “{name}”:": "Farbe für „{name}“:",
        "↻  Another one": "↻  Ein anderes",
        "✔  Use this password": "✔  Dieses Passwort verwenden",
        "Close": "Schließen",
        "Open Pocket Book": "Pocket Book öffnen",
        "Uninstall Pocket Book?": "Pocket Book deinstallieren?",
        "Also delete all my cards and their backups":
            "Auch alle meine Karten und ihre Sicherungen löschen",
        "Delete the cards?": "Karten löschen?",
        "Uninstall": "Deinstallieren",
        "The notebook was damaged. The backup from {date} has been restored.":
            "Das Notizbuch war beschädigt. Die Sicherung vom {date} wurde wiederhergestellt.",
        "Text": "Text",
        "Category:": "Kategorie:",
        "Open on the computer:": "Auf dem Computer öffnen:",
        "The original document": "Das Originaldokument",
        "Delete this contact": "Diesen Kontakt löschen",
        "Delete this card": "Diese Karte löschen",
        "Password": "Passwort",
        "✔  Done": "✔  Fertig",
        "Which field should be added to this card?":
            "Welches Feld soll zu dieser Karte hinzugefügt werden?",
        "Or another field, with your own name (e.g. Customer number, Secret question):":
            "Oder ein anderes Feld mit eigenem Namen (z. B. Kundennummer, Sicherheitsfrage):",
        "File the documents in this folder automatically (new and changed ones), at every start and every minute":
            "Dokumente dieses Ordners automatisch einordnen (neue und geänderte), bei jedem Start und jede Minute",
        "Show:": "Zeigen:",
        "Search in the documents": "In den Dokumenten suchen",
        "Document text:": "Text des Dokuments:",
        "✔ Copied": "✔ Kopiert",
        "⚠ Could not save!": "⚠ Speichern nicht möglich!",
        "The notebook could not be saved.\n\n":
            "Das Notizbuch konnte nicht gespeichert werden.\n\n",
        "The notebook is saved, but the .txt copy of the cards could not be made.\n\nThe folder may be disconnected (USB stick, network drive).\n\n":
            "Das Notizbuch ist gespeichert, aber die .txt-Kopie der Karten konnte nicht erstellt werden.\n\nDer Ordner ist vielleicht nicht verbunden (USB-Stick, Netzlaufwerk).\n\n",
        "Copy of each card as .txt, updated automatically, in:\n":
            "Kopie jeder Karte als .txt, automatisch aktualisiert, in:\n",
        "The file could not be opened.\n\n": "Die Datei konnte nicht geöffnet werden.\n\n",
        "The folder could not be opened.\n\n": "Der Ordner konnte nicht geöffnet werden.\n\n",
        "Documents folder:\n": "Dokumentenordner:\n",
        "↻ Documents synced at {time_str}: ": "↻ Dokumente abgeglichen um {time_str}: ",
        "From the documents:\n\n   • ": "Aus den Dokumenten:\n\n   • ",
        "The document could not be opened.\n\n": "Das Dokument konnte nicht geöffnet werden.\n\n",
        "Word and text documents": "Word- und Textdokumente",
        "All files": "Alle Dateien",
        "The documents themselves are not changed. Continue?":
            "Die Dokumente selbst werden nicht verändert. Fortfahren?",
        "{n} document looks like neither a password nor a contact.":
            "{n} Dokument sieht weder wie ein Passwort noch wie ein Kontakt aus.",
        "{n} documents look like neither a password nor a contact.":
            "{n} Dokumente sehen weder wie ein Passwort noch wie ein Kontakt aus.",
        "What does this document contain?": "Was enthält dieses Dokument?",
        "Length:": "Länge:",
        "The old password will be kept in the card's notes.":
            "Das alte Passwort wird in den Notizen der Karte aufbewahrt.",
        "characters": "Zeichen",
        "Copying the program failed.": "Das Kopieren des Programms ist fehlgeschlagen.",
        "Put a “Pocket Book” icon on the Desktop": "Ein Symbol „Pocket Book“ auf den Desktop legen",
        "Update": "Aktualisieren",
        "Install": "Installieren",
        "Installing…": "Wird installiert…",
        "Try again": "Erneut versuchen",
        "The program and its icons will be removed from this computer.\nYour cards are kept, in:":
            "Das Programm und seine Symbole werden von diesem Computer entfernt.\nIhre Karten bleiben erhalten, in:",
        "Continue?": "Fortfahren?",
        "Deleted cards": "Gelöschte Karten",
        "card": "Karte",
        "Remove “{field}” from this card?\n\nWhat is written in it will be erased:":
            "„{field}“ von dieser Karte entfernen?\n\nWas darin steht, wird gelöscht:",
        "Search for a contact": "Einen Kontakt suchen",
        "Search for a card": "Eine Karte suchen",
        "＋  New contact": "＋  Neuer Kontakt",
        "＋  New card": "＋  Neue Karte",
        "\n\nTip: drag .docx or .txt files (or a whole folder)\nfrom your file manager onto this window to file them all at once.":
            "\n\nTipp: Ziehen Sie .docx- oder .txt-Dateien (oder einen ganzen Ordner)\naus dem Datei-Explorer in dieses Fenster, um sie auf einmal einzuordnen.",
        "Reading documents: {i} of {n}…": "Dokumente werden gelesen: {i} von {n}…",
        "… and {n} more contacts": "… und {n} weitere Kontakte",
        "Update Pocket Book": "Pocket Book aktualisieren",
        "Install Pocket Book": "Pocket Book installieren",
        "The installation could not be completed":
            "Die Installation konnte nicht durchgeführt werden",
        "Pocket Book is installed": "Pocket Book ist installiert",
        "This installation file can now be put away or deleted.":
            "Diese Installationsdatei kann jetzt weggelegt oder gelöscht werden.",
        "All cards, backups and .txt copies in this folder will be permanently erased:":
            "Alle Karten, Sicherungen und .txt-Kopien in diesem Ordner werden endgültig gelöscht:",
        "Open": "Öffnen",
        "From the document: ": "Aus dem Dokument: ",
        "The notebook did not recognise this document. You can still create a card: it will ask whether it is a password or a contact.":
            "Das Notizbuch hat dieses Dokument nicht erkannt. Sie können trotzdem eine Karte erstellen: Es fragt Sie, ob es ein Passwort oder ein Kontakt ist.",
        "• Click a name in the list on the left,\n":
            "• Klicken Sie links in der Liste auf einen Namen,\n",
        "• or on “New contact” to create one.": "• oder auf „Neuer Kontakt“, um einen anzulegen.",
        "• or on “New card” to create one.": "• oder auf „Neue Karte“, um eine anzulegen.",
        "Reading failed.": "Das Lesen ist fehlgeschlagen.",
        "The documents could not be read.\n\n": "Die Dokumente konnten nicht gelesen werden.\n\n",
        "{n} contact  →  “My contacts”": "{n} Kontakt  →  „Meine Kontakte“",
        "{n} contacts  →  “My contacts”": "{n} Kontakte  →  „Meine Kontakte“",
        "No contact is selected.\n\n": "Kein Kontakt ausgewählt.\n\n",
        "No card is selected.\n\n": "Keine Karte ausgewählt.\n\n",
        "{n} password  →  “My passwords”": "{n} Passwort  →  „Meine Passwörter“",
        "{n} passwords  →  “My passwords”": "{n} Passwörter  →  „Meine Passwörter“",
        "The notebook will file:": "Das Notizbuch ordnet ein:",
        "Category": "Kategorie",
        "Username": "Benutzername",
        "Email address": "E-Mail-Adresse",
        "Mobile": "Handy",
        "Landline": "Festnetz",
        "Address": "Adresse",
        "Birthday": "Geburtstag",
        "Contact": "Kontakt",
        "?": "?",
        "a password": "ein Passwort",
        "a contact": "ein Kontakt",
        "not recognised": "nicht erkannt",
        "Blue": "Blau",
        "Green": "Grün",
        "Yellow": "Gelb",
        "Orange": "Orange",
        "Red": "Rot",
        "Purple": "Violett",
        "Pink": "Rosa",
        "Turquoise": "Türkis",
        "Grey": "Grau",
        "Brown": "Braun",
        "Bank": "Bank",
        "Administration": "Behörden",
        "Health": "Gesundheit",
        "Email": "E-Mail",
        "Shopping": "Einkäufe",
        "Bills": "Rechnungen",
        "Leisure": "Freizeit",
        "Family": "Familie",
        "Work": "Arbeit",
        "Light": "Hell",
        "Dark": "Dunkel",
        "High contrast": "Hoher Kontrast",
        "Soft sepia": "Sanftes Sepia",
        "Other": "Sonstige",
        "About": "Über",
        "Pocket Book {version} — works entirely without internet: nothing leaves this computer.":
            "Pocket Book {version} — funktioniert komplett ohne Internet: Nichts verlässt diesen Computer.",
        "Your data is here:": "Ihre Daten liegen hier:",
        "Open the data folder": "Datenordner öffnen",
        "Uninstall…": "Deinstallieren…",
    },
    "it": {
        "(none)": "(nessuna)",
        "All categories": "Tutte",
        "Pocket Book has been uninstalled.": "Pocket Book è stato disinstallato.",
        "File type not supported": "Tipo di file non supportato",
        "This file is rewritten after every change: edit the card in the notebook.":
            "Questo file viene riscritto a ogni modifica: modificate la scheda nel quaderno.",
        "Delete the category “{name}”?": "Eliminare la categoria «{name}»?",
        "Category colour": "Colore della categoria",
        "What kind of document?": "Che tipo di documento è?",
        "Installing Pocket Book": "Installazione di Pocket Book",
        "Uninstall Pocket Book": "Disinstalla Pocket Book",
        "Untitled": "Senza nome",
        "New contact": "Nuovo contatto",
        "New card": "Nuova scheda",
        "%m/%d/%Y at %H:%M": "%d/%m/%Y alle %H:%M",
        "Notes": "Note",
        "Automatic copy made by Pocket Book (card changed on {date}).":
            "Copia automatica fatta da Pocket Book (scheda modificata il {date}).",
        "Automatic copy made by Pocket Book.": "Copia automatica fatta da Pocket Book.",
        "Name": "Nome",
        "Copy": "Copia",
        "✎  Edit by hand": "✎  Modifica a mano",
        "Add a field": "Aggiungi un campo",
        "Categories": "Categorie",
        "Categories are used to sort cards. Each one has its own colour, shown in the list of cards.":
            "Le categorie servono a ordinare le schede. Ognuna ha il suo colore, che appare nell'elenco delle schede.",
        "Language": "Lingua",
        "Screen colours": "Colori dello schermo",
        "Choose whatever is easiest to read.": "Scegliete ciò che è più comodo da leggere.",
        "Copy of cards as .txt": "Copia delle schede in .txt",
        "Each card is copied into a .txt file that updates itself. Make changes in the notebook, not in the .txt files.":
            "Ogni scheda viene copiata in un file .txt che si aggiorna da solo. Le modifiche si fanno nel quaderno, non nei .txt.",
        "New category": "Nuova categoria",
        "Name of the new category:": "Nome della nuova categoria:",
        "Rename the category": "Rinomina la categoria",
        "New name:": "Nuovo nome:",
        "＋  Create a card from this document": "＋  Crea una scheda da questo documento",
        "{n} contact": "{n} contatto",
        "{n} contacts": "{n} contatti",
        "{n} card": "{n} scheda",
        "{n} cards": "{n} schede",
        "Do you really want to delete the contact “{name}”?":
            "Volete davvero eliminare il contatto «{name}»?",
        "Do you really want to delete the card “{name}”?":
            "Volete davvero eliminare la scheda «{name}»?",
        "Old password (replaced on {date}): {old}":
            "Vecchia password (sostituita il {date}): {old}",
        "No folder chosen.": "Nessuna cartella scelta.",
        "This document contained {n} contacts: they have all been created.":
            "Questo documento conteneva {n} contatti: sono stati creati tutti.",
        "The card was filled in from the document.":
            "La scheda è stata compilata a partire dal documento.",
        "Check that each piece of information is in the right place.":
            "Controllate che ogni informazione sia al posto giusto.",
        "Card created": "Scheda creata",
        "All filed!": "Tutto sistemato!",
        "{n} card created.": "{n} scheda creata.",
        "{n} cards created.": "{n} schede create.",
        "Create a new password": "Crea una nuova password",
        "A new version of Pocket Book will replace the old one.\nYour cards are not touched.":
            "Una nuova versione di Pocket Book sostituirà quella vecchia.\nLe vostre schede non vengono toccate.",
        "To open it, double-click the “Pocket Book” icon on the Desktop\n(or look for “Pocket Book” in the applications menu).":
            "Per aprirlo, fate doppio clic sull'icona «Pocket Book» sul Desktop\n(oppure cercate «Pocket Book» nel menu delle applicazioni).",
        "To open it, look for “Pocket Book” in the applications menu.":
            "Per aprirlo, cercate «Pocket Book» nel menu delle applicazioni.",
        "The notebook was damaged and no backup could be read. A copy was kept: {file_path}":
            "Il quaderno era danneggiato e nessun backup ha potuto essere letto. È stata conservata una copia: {file_path}",
        "My passwords": "Le mie password",
        "My contacts": "I miei contatti",
        "My documents": "I miei documenti",
        "First click on a category in the list.": "Prima fate clic su una categoria nell'elenco.",
        "The category “{name}” already exists.": "La categoria «{name}» esiste già.",
        "{n} card will no longer have a category (the card itself is not deleted).":
            "{n} scheda non avrà più una categoria (la scheda stessa non viene eliminata).",
        "{n} cards will no longer have a category (the cards themselves are not deleted).":
            "{n} schede non avranno più una categoria (le schede stesse non vengono eliminate).",
        "Delete the category?": "Eliminare la categoria?",
        "↻  Sync now": "↻  Sincronizza ora",
        "Choose the folder…": "Scegli la cartella…",
        "Import files…": "Importa file…",
        "To file": "Da sistemare",
        "All": "Tutto",
        "Passwords": "Password",
        "Contacts": "Contatti",
        "Not recognised": "Non riconosciuti",
        "Choose a document in the list.": "Scegliete un documento nell'elenco.",
        "This document is never changed by the notebook.":
            "Questo documento non viene mai modificato dal quaderno.",
        "{n} contact found": "{n} contatto trovato",
        "{n} contacts found": "{n} contatti trovati",
        "{n} card found": "{n} scheda trovata",
        "{n} cards found": "{n} schede trovate",
        ", from A to Z": ", dalla A alla Z",
        " starting with {letter}": " con la lettera {letter}",
        "Delete?": "Eliminare?",
        "Website": "Sito web",
        "No website address is written on this card.":
            "Su questa scheda non è indicato nessun sito web.",
        "%m/%d/%Y": "%d/%m/%Y",
        "✎ Editing…": "✎ Modifica in corso…",
        "Which folder should hold the .txt copy of the cards?":
            "In quale cartella mettere la copia .txt delle schede?",
        "Choose a folder other than the one with the original documents\n(for example a “Cards as text” subfolder).":
            "Scegliete una cartella diversa da quella dei documenti originali\n(per esempio una sottocartella «Schede in testo»).",
        "\n\nThe old folder has not been changed.":
            "\n\nLa vecchia cartella non è stata modificata.",
        "This file does not exist (or no longer exists) on the computer.":
            "Questo file non esiste (o non esiste più) sul computer.",
        "Where are your documents kept?": "Dove sono conservati i vostri documenti?",
        "First choose the folder where your documents are kept.":
            "Prima scegliete la cartella dove sono conservati i vostri documenti.",
        "Reading documents…": "Lettura dei documenti…",
        "{n} card created": "{n} scheda creata",
        "{n} cards created": "{n} schede create",
        "{n} card updated": "{n} aggiornata",
        "{n} cards updated": "{n} aggiornate",
        "{n} to check (⚠ in the notes)": "{n} da controllare (⚠ nelle note)",
        "Sync": "Sincronizzazione",
        "{n} document": "{n} documento",
        "{n} documents": "{n} documenti",
        "✔ = already filed in the notebook": "✔ = già sistemato nel quaderno",
        "Recognised as: {kind}   —   this document is never changed.":
            "Riconosciuto come: {kind}   —   questo documento non viene mai modificato.",
        "(Empty document)": "(Documento vuoto)",
        "Already filed in the notebook:": "Già sistemato nel quaderno:",
        "What the notebook understood:": "Ciò che il quaderno ha capito:",
        "First choose a document in the list.": "Prima scegliete un documento nell'elenco.",
        "Choose the documents to file (several at once is fine)":
            "Scegliete i documenti da sistemare (anche più di uno)",
        "{n} document already filed: skipped.": "{n} documento già sistemato: saltato.",
        "{n} documents already filed: skipped.": "{n} documenti già sistemati: saltati.",
        "{n} old .doc file not read (save it as .docx with Word).":
            "{n} vecchio file .doc non letto (salvatelo in .docx con Word).",
        "{n} old .doc files not read (save them as .docx with Word).":
            "{n} vecchi file .doc non letti (salvateli in .docx con Word).",
        "{n} file of another type skipped.": "{n} file di altro tipo saltato.",
        "{n} files of another type skipped.": "{n} file di altro tipo saltati.",
        "{n} document not recognised: {names}": "{n} documento non riconosciuto: {names}",
        "{n} documents not recognised: {names}": "{n} documenti non riconosciuti: {names}",
        "Documents not recognised": "Documenti non riconosciuti",
        "Cancel": "Annulla",
        "✔  OK": "✔  Conferma",
        "A password": "Una password",
        "A contact": "Un contatto",
        "Easy to read (words)": "Facile da leggere (parole)",
        "Very strong (letters and symbols)": "Molto sicura (lettere e simboli)",
        "words": "parole",
        "Passwords and contacts, without internet": "Password e contatti, senza internet",
        "Pocket Book is probably still open.\nClose it, then click “Install” again.":
            "Pocket Book è probabilmente ancora aperto.\nChiudetelo, poi fate di nuovo clic su «Installa».",
        "Your cards are still in:": "Le vostre schede sono sempre in:",
        "Pocket Book will be installed on this computer.\nIt works without internet: nothing leaves the computer.\nYour cards will be kept in:":
            "Pocket Book sarà installato su questo computer.\nFunziona senza internet: niente lascia il computer.\nLe vostre schede saranno conservate in:",
        "Cards as text": "Schede in testo",
        "⚠ The document “{name}” changed on {date}: check this card (it was not replaced).":
            "⚠ Il documento «{name}» è cambiato il {date}: controllate questa scheda (non è stata sostituita).",
        "Could not read this document ({error}).":
            "Impossibile leggere questo documento ({error}).",
        "Settings": "Impostazioni",
        "A": "A",
        "Save now": "Salva ora",
        "Field": "Campo",
        "＋  Add a field": "＋  Aggiungi un campo",
        "The .txt copy": "La copia .txt",
        "The folder": "La cartella",
        "↻  Create a new password": "↻  Crea una nuova password",
        "＋  Add this field": "＋  Aggiungi questo campo",
        "Remove the field?": "Togliere il campo?",
        "＋  New": "＋  Nuova",
        "Rename": "Rinomina",
        "Colour…": "Colore…",
        "Delete": "Elimina",
        "Change folder…": "Cambia cartella…",
        "Open the folder": "Apri la cartella",
        "Open in Word": "Apri in Word",
        "A copy stays in today's backups.": "Una copia resta nei backup di oggi.",
        "Change the password?": "Cambiare la password?",
        "Do you really want to change the password for “{name}”?\n\nCareful: this only changes the notebook. You must also change it on the website itself, otherwise you will no longer be able to log in.\n\n(The old password will be kept in the notes.)":
            "Volete davvero cambiare la password di «{name}»?\n\nAttenzione: questo cambia solo il quaderno. Bisogna cambiarla anche sul sito stesso, altrimenti non potrete più accedere.\n\n(La vecchia password sarà conservata nelle note.)",
        "Saving problem": "Problema di salvataggio",
        "✔ Everything is saved ({time_str})": "✔ Tutto è salvato ({time_str})",
        "✔ Saved ({time_str}) — ⚠ .txt copy failed": "✔ Salvato ({time_str}) — ⚠ copia .txt impossibile",
        "Close anyway?": "Chiudere comunque?",
        "The notebook could not be saved.\nClose anyway?":
            "Il quaderno non è stato salvato.\nChiudere comunque?",
        "✔ Everything is saved": "✔ Tutto è salvato",
        "Copy of cards as .txt: turned off.": "Copia delle schede in .txt: disattivata.",
        "The .txt copy of the cards is now in:\n": "La copia .txt delle schede ora è in:\n",
        "No folder chosen. Click “Choose the folder…”.":
            "Nessuna cartella scelta. Fate clic su «Scegli la cartella…».",
        "Everything is already up to date: no card to create or change.":
            "Tutto è già aggiornato: nessuna scheda da creare o modificare.",
        "{n} document to file (out of {total})": "{n} documento da sistemare (su {total})",
        "{n} documents to file (out of {total})": "{n} documenti da sistemare (su {total})",
        "✔ Everything is filed ({total} documents).\nClick “All” to see them again.":
            "✔ Tutto è sistemato ({total} documenti).\nFate clic su «Tutto» per rivederli.",
        "{n} document found": "{n} documento trovato",
        "{n} documents found": "{n} documenti trovati",
        "⚠ {n} old .doc file not read\n   (save it as .docx with Word)":
            "⚠ {n} vecchio file .doc non letto\n   (salvatelo in .docx con Word)",
        "⚠ {n} old .doc files not read\n   (save them as .docx with Word)":
            "⚠ {n} vecchi file .doc non letti\n   (salvateli in .docx con Word)",
        "→  See the card": "→  Vedi la scheda",
        "“{name}” is already filed in the notebook.\nCreate another card anyway?":
            "«{name}» è già sistemato nel quaderno.\nCreare comunque un'altra scheda?",
        "Nothing new to file.\n\n": "Niente di nuovo da sistemare.\n\n",
        "File these documents?": "Sistemare questi documenti?",
        "File them anyway in “My passwords”?\n(their text will go into the card's Notes)":
            "Sistemarli comunque in «Le mie password»?\n(il loro testo andrà nelle Note della scheda)",
        "Colour for “{name}”:": "Colore per «{name}»:",
        "↻  Another one": "↻  Un'altra",
        "✔  Use this password": "✔  Usa questa password",
        "Close": "Chiudi",
        "Open Pocket Book": "Apri Pocket Book",
        "Uninstall Pocket Book?": "Disinstallare Pocket Book?",
        "Also delete all my cards and their backups":
            "Elimina anche tutte le mie schede e i loro backup",
        "Delete the cards?": "Eliminare le schede?",
        "Uninstall": "Disinstalla",
        "The notebook was damaged. The backup from {date} has been restored.":
            "Il quaderno era danneggiato. È stato ripristinato il backup del {date}.",
        "Text": "Testo",
        "Category:": "Categoria:",
        "Open on the computer:": "Apri sul computer:",
        "The original document": "Il documento originale",
        "Delete this contact": "Elimina questo contatto",
        "Delete this card": "Elimina questa scheda",
        "Password": "Password",
        "✔  Done": "✔  Fatto",
        "Which field should be added to this card?": "Quale campo aggiungere a questa scheda?",
        "Or another field, with your own name (e.g. Customer number, Secret question):":
            "Oppure un altro campo, con il nome che volete (es.: Codice cliente, Domanda segreta):",
        "File the documents in this folder automatically (new and changed ones), at every start and every minute":
            "Sistema da solo i documenti di questa cartella (nuovi e modificati), a ogni apertura e ogni minuto",
        "Show:": "Mostra:",
        "Search in the documents": "Cerca nei documenti",
        "Document text:": "Testo del documento:",
        "✔ Copied": "✔ Copiato",
        "⚠ Could not save!": "⚠ Salvataggio impossibile!",
        "The notebook could not be saved.\n\n": "Il quaderno non è stato salvato.\n\n",
        "The notebook is saved, but the .txt copy of the cards could not be made.\n\nThe folder may be disconnected (USB stick, network drive).\n\n":
            "Il quaderno è salvato, ma la copia .txt delle schede non è stata fatta.\n\nForse la cartella è scollegata (chiavetta USB, disco di rete).\n\n",
        "Copy of each card as .txt, updated automatically, in:\n":
            "Copia di ogni scheda in .txt, aggiornata da sola, in:\n",
        "The file could not be opened.\n\n": "Impossibile aprire il file.\n\n",
        "The folder could not be opened.\n\n": "Impossibile aprire la cartella.\n\n",
        "Documents folder:\n": "Cartella dei documenti:\n",
        "↻ Documents synced at {time_str}: ": "↻ Documenti sincronizzati alle {time_str}: ",
        "From the documents:\n\n   • ": "Dai documenti:\n\n   • ",
        "The document could not be opened.\n\n": "Impossibile aprire il documento.\n\n",
        "Word and text documents": "Documenti Word e di testo",
        "All files": "Tutti i file",
        "The documents themselves are not changed. Continue?":
            "I documenti stessi non vengono modificati. Continuare?",
        "{n} document looks like neither a password nor a contact.":
            "{n} documento non sembra né una password né un contatto.",
        "{n} documents look like neither a password nor a contact.":
            "{n} documenti non sembrano né una password né un contatto.",
        "What does this document contain?": "Cosa contiene questo documento?",
        "Length:": "Lunghezza:",
        "The old password will be kept in the card's notes.":
            "La vecchia password sarà conservata nelle note della scheda.",
        "characters": "caratteri",
        "Copying the program failed.": "La copia del programma non è riuscita.",
        "Put a “Pocket Book” icon on the Desktop": "Metti un'icona «Pocket Book» sul Desktop",
        "Update": "Aggiorna",
        "Install": "Installa",
        "Installing…": "Installazione in corso…",
        "Try again": "Riprova",
        "The program and its icons will be removed from this computer.\nYour cards are kept, in:":
            "Il programma e le sue icone saranno tolti da questo computer.\nLe vostre schede vengono conservate, in:",
        "Continue?": "Continuare?",
        "Deleted cards": "Schede eliminate",
        "card": "scheda",
        "Remove “{field}” from this card?\n\nWhat is written in it will be erased:":
            "Togliere «{field}» da questa scheda?\n\nCiò che vi è scritto sarà cancellato:",
        "Search for a contact": "Cerca un contatto",
        "Search for a card": "Cerca una scheda",
        "＋  New contact": "＋  Nuovo contatto",
        "＋  New card": "＋  Nuova scheda",
        "\n\nTip: drag .docx or .txt files (or a whole folder)\nfrom your file manager onto this window to file them all at once.":
            "\n\nSuggerimento: trascinate file .docx o .txt (o un'intera cartella)\ndal gestore dei file su questa finestra per sistemarli tutti insieme.",
        "Reading documents: {i} of {n}…": "Lettura dei documenti: {i} di {n}…",
        "… and {n} more contacts": "… e altri {n} contatti",
        "Update Pocket Book": "Aggiorna Pocket Book",
        "Install Pocket Book": "Installa Pocket Book",
        "The installation could not be completed":
            "Non è stato possibile completare l'installazione",
        "Pocket Book is installed": "Pocket Book è installato",
        "This installation file can now be put away or deleted.":
            "Questo file di installazione ora può essere messo via o eliminato.",
        "All cards, backups and .txt copies in this folder will be permanently erased:":
            "Tutte le schede, i backup e le copie .txt di questa cartella saranno cancellati definitivamente:",
        "Open": "Apri",
        "From the document: ": "Dal documento: ",
        "The notebook did not recognise this document. You can still create a card: it will ask whether it is a password or a contact.":
            "Il quaderno non ha riconosciuto questo documento. Potete comunque creare una scheda: vi chiederà se si tratta di una password o di un contatto.",
        "• Click a name in the list on the left,\n":
            "• Fate clic su un nome nell'elenco a sinistra,\n",
        "• or on “New contact” to create one.": "• oppure su «Nuovo contatto» per crearne uno.",
        "• or on “New card” to create one.": "• oppure su «Nuova scheda» per crearne una.",
        "Reading failed.": "La lettura non è riuscita.",
        "The documents could not be read.\n\n": "Non è stato possibile leggere i documenti.\n\n",
        "{n} contact  →  “My contacts”": "{n} contatto  →  «I miei contatti»",
        "{n} contacts  →  “My contacts”": "{n} contatti  →  «I miei contatti»",
        "No contact is selected.\n\n": "Nessun contatto selezionato.\n\n",
        "No card is selected.\n\n": "Nessuna scheda selezionata.\n\n",
        "{n} password  →  “My passwords”": "{n} password  →  «Le mie password»",
        "{n} passwords  →  “My passwords”": "{n} password  →  «Le mie password»",
        "The notebook will file:": "Il quaderno sistemerà:",
        "Category": "Categoria",
        "Username": "Nome utente",
        "Email address": "Indirizzo e-mail",
        "Mobile": "Cellulare",
        "Landline": "Telefono fisso",
        "Address": "Indirizzo",
        "Birthday": "Compleanno",
        "Contact": "Contatto",
        "?": "?",
        "a password": "una password",
        "a contact": "un contatto",
        "not recognised": "non riconosciuto",
        "Blue": "Blu",
        "Green": "Verde",
        "Yellow": "Giallo",
        "Orange": "Arancione",
        "Red": "Rosso",
        "Purple": "Viola",
        "Pink": "Rosa",
        "Turquoise": "Turchese",
        "Grey": "Grigio",
        "Brown": "Marrone",
        "Bank": "Banca",
        "Administration": "Amministrazione",
        "Health": "Salute",
        "Email": "Posta",
        "Shopping": "Acquisti",
        "Bills": "Bollette",
        "Leisure": "Tempo libero",
        "Family": "Famiglia",
        "Work": "Lavoro",
        "Light": "Chiaro",
        "Dark": "Scuro",
        "High contrast": "Contrasto elevato",
        "Soft sepia": "Seppia tenue",
        "Other": "Altro",
        "About": "Informazioni",
        "Pocket Book {version} — works entirely without internet: nothing leaves this computer.":
            "Pocket Book {version} — funziona interamente senza internet: niente lascia questo computer.",
        "Your data is here:": "I vostri dati sono qui:",
        "Open the data folder": "Apri la cartella dei dati",
        "Uninstall…": "Disinstalla…",
    },
}
