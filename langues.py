# -*- coding: utf-8 -*-
"""Traductions de l'interface de Pocket Book / Interface translations.

Le programme est écrit en français : chaque dictionnaire associe une phrase française
à sa traduction. Une phrase absente reste en français (rien ne casse).
Les {mots} entre accolades sont remplacés par des valeurs : à garder tels quels.

Ajouter une langue : ajouter son nom dans LANGUES, un dictionnaire dans TRADUCTIONS
et une liste de mots simples dans MOTS_FACILES (pour les mots de passe « faciles à lire »).
`python scripts/verifier_traductions.py` signale les phrases manquantes.

The program is written in French: each dictionary maps a French sentence to its
translation. Missing sentences simply stay in French. Keep {placeholders} as they are.
"""

LANGUES = {
    "fr": "Français",
    "en": "English",
    "es": "Español",
    "de": "Deutsch",
    "it": "Italiano",
}

# Mots simples (sans accents, faciles à taper) pour les mots de passe « faciles à lire »
MOTS_FACILES = {
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

TRADUCTIONS = {
    "en": {
        "(aucune)":
            "(none)",
        "Toutes":
            "All",
        "Pocket Book a été désinstallé.":
            "Pocket Book has been uninstalled.",
        "Type de fichier non pris en charge":
            "File type not supported",
        "Ce fichier est réécrit à chaque changement : modifiez la fiche dans le carnet.":
            "This file is rewritten after every change: edit the card in the notebook.",
        "Supprimer la catégorie « {nom} » ?":
            "Delete the category “{nom}”?",
        "Couleur de la catégorie":
            "Category colour",
        "Quel genre de document ?":
            "What kind of document?",
        "Installation de Pocket Book":
            "Installing Pocket Book",
        "Désinstaller Pocket Book":
            "Uninstall Pocket Book",
        "Sans nom":
            "Untitled",
        "Nouveau contact":
            "New contact",
        "Nouvelle fiche":
            "New card",
        "%d/%m/%Y à %H:%M":
            "%m/%d/%Y at %H:%M",
        "Notes":
            "Notes",
        "Copie automatique faite par Pocket Book (fiche modifiée le {date}).":
            "Automatic copy made by Pocket Book (card changed on {date}).",
        "Copie automatique faite par Pocket Book.":
            "Automatic copy made by Pocket Book.",
        "Nom":
            "Name",
        "Copier":
            "Copy",
        "✎  Modifier à la main":
            "✎  Edit by hand",
        "Ajouter un champ":
            "Add a field",
        "Catégories":
            "Categories",
        "Les catégories servent à trier les fiches. Chacune a sa couleur, qui apparaît dans la liste des fiches.":
            "Categories are used to sort cards. Each one has its own colour, shown in the list of cards.",
        "Langue":
            "Language",
        "Couleurs de l'écran":
            "Screen colours",
        "Choisissez ce qui est le plus agréable à lire.":
            "Choose whatever is easiest to read.",
        "Copie des fiches en .txt":
            "Copy of cards as .txt",
        "Chaque fiche est recopiée dans un fichier .txt, mis à jour tout seul. Les changements se font dans le carnet, pas dans les .txt.":
            "Each card is copied into a .txt file that updates itself. Make changes in the notebook, not in the .txt files.",
        "Nouvelle catégorie":
            "New category",
        "Nom de la nouvelle catégorie :":
            "Name of the new category:",
        "Renommer la catégorie":
            "Rename the category",
        "Nouveau nom :":
            "New name:",
        "＋  Créer une fiche avec ce document":
            "＋  Create a card from this document",
        "{n} contact":
            "{n} contact",
        "{n} contacts":
            "{n} contacts",
        "{n} fiche":
            "{n} card",
        "{n} fiches":
            "{n} cards",
        "Voulez-vous vraiment supprimer le contact « {nom} » ?":
            "Do you really want to delete the contact “{nom}”?",
        "Voulez-vous vraiment supprimer la fiche « {nom} » ?":
            "Do you really want to delete the card “{nom}”?",
        "Ancien mot de passe (remplacé le {date}) : {ancien}":
            "Old password (replaced on {date}): {ancien}",
        "Aucun dossier choisi.":
            "No folder chosen.",
        "Ce document contenait {n} contacts : ils ont tous été créés.":
            "This document contained {n} contacts: they have all been created.",
        "La fiche a été remplie à partir du document.":
            "The card was filled in from the document.",
        "Vérifiez que chaque information est au bon endroit.":
            "Check that each piece of information is in the right place.",
        "Fiche créée":
            "Card created",
        "C'est rangé !":
            "All filed!",
        "{n} fiche créée.":
            "{n} card created.",
        "{n} fiches créées.":
            "{n} cards created.",
        "Créer un nouveau mot de passe":
            "Create a new password",
        "Une nouvelle version de Pocket Book va remplacer l'ancienne.\nVos fiches ne sont pas touchées.":
            "A new version of Pocket Book will replace the old one.\nYour cards are not touched.",
        "Pour l'ouvrir, double-cliquez sur l'icône « Pocket Book » du Bureau\n(ou cherchez « Pocket Book » dans le menu des applications).":
            "To open it, double-click the “Pocket Book” icon on the Desktop\n(or look for “Pocket Book” in the applications menu).",
        "Pour l'ouvrir, cherchez « Pocket Book » dans le menu des applications.":
            "To open it, look for “Pocket Book” in the applications menu.",
        "Le carnet était abîmé et aucune sauvegarde n'a pu être lue. Une copie a été gardée : {fichier}":
            "The notebook was damaged and no backup could be read. A copy was kept: {fichier}",
        "Mes mots de passe":
            "My passwords",
        "Mes contacts":
            "My contacts",
        "Mes documents":
            "My documents",
        "Cliquez d'abord sur une catégorie dans la liste.":
            "First click on a category in the list.",
        "La catégorie « {nom} » existe déjà.":
            "The category “{nom}” already exists.",
        "{n} fiche n'aura plus de catégorie (la fiche elle-même n'est pas supprimée).":
            "{n} card will no longer have a category (the card itself is not deleted).",
        "{n} fiches n'auront plus de catégorie (les fiches elles-mêmes ne sont pas supprimées).":
            "{n} cards will no longer have a category (the cards themselves are not deleted).",
        "Supprimer la catégorie ?":
            "Delete the category?",
        "↻  Synchroniser maintenant":
            "↻  Sync now",
        "Choisir le dossier…":
            "Choose the folder…",
        "Importer des fichiers…":
            "Import files…",
        "À ranger":
            "To file",
        "Tout":
            "All",
        "Mots de passe":
            "Passwords",
        "Contacts":
            "Contacts",
        "Non reconnus":
            "Not recognised",
        "Choisissez un document dans la liste.":
            "Choose a document in the list.",
        "Ce document n'est jamais modifié par le carnet.":
            "This document is never changed by the notebook.",
        "{n} contact trouvé":
            "{n} contact found",
        "{n} contacts trouvés":
            "{n} contacts found",
        "{n} fiche trouvée":
            "{n} card found",
        "{n} fiches trouvées":
            "{n} cards found",
        ", de A à Z":
            ", from A to Z",
        " à la lettre {lettre}":
            " starting with {lettre}",
        "Supprimer ?":
            "Delete?",
        "Site internet":
            "Website",
        "Aucune adresse de site n'est notée sur cette fiche.":
            "No website address is written on this card.",
        "%d/%m/%Y":
            "%m/%d/%Y",
        "✎ Modification en cours…":
            "✎ Editing…",
        "Dans quel dossier ranger la copie .txt des fiches ?":
            "Which folder should hold the .txt copy of the cards?",
        "Choisissez un autre dossier que celui des documents d'origine\n(par exemple un sous-dossier « Fiches en texte »).":
            "Choose a folder other than the one with the original documents\n(for example a “Cards as text” subfolder).",
        "\n\nL'ancien dossier n'a pas été modifié.":
            "\n\nThe old folder has not been changed.",
        "Ce fichier n'existe pas (ou plus) sur l'ordinateur.":
            "This file does not exist (or no longer exists) on the computer.",
        "Où sont rangés vos documents ?":
            "Where are your documents kept?",
        "Choisissez d'abord le dossier où sont rangés vos documents.":
            "First choose the folder where your documents are kept.",
        "Lecture des documents…":
            "Reading documents…",
        "{n} fiche créée":
            "{n} card created",
        "{n} fiches créées":
            "{n} cards created",
        "{n} mise à jour":
            "{n} updated",
        "{n} mises à jour":
            "{n} updated",
        "{n} à vérifier (⚠ dans les notes)":
            "{n} to check (⚠ in the notes)",
        "Synchronisation":
            "Sync",
        "{n} document":
            "{n} document",
        "{n} documents":
            "{n} documents",
        "✔ = déjà rangé dans le carnet":
            "✔ = already filed in the notebook",
        "Reconnu comme : {genre}   —   ce document n'est jamais modifié.":
            "Recognised as: {genre}   —   this document is never changed.",
        "(Document vide)":
            "(Empty document)",
        "Déjà rangé dans le carnet :":
            "Already filed in the notebook:",
        "Ce que le carnet a compris :":
            "What the notebook understood:",
        "Choisissez d'abord un document dans la liste.":
            "First choose a document in the list.",
        "Choisissez les documents à ranger (plusieurs à la fois possible)":
            "Choose the documents to file (several at once is fine)",
        "{n} document déjà rangé : ignoré.":
            "{n} document already filed: skipped.",
        "{n} documents déjà rangés : ignorés.":
            "{n} documents already filed: skipped.",
        "{n} ancien fichier .doc non lu (à enregistrer en .docx avec Word).":
            "{n} old .doc file not read (save it as .docx with Word).",
        "{n} anciens fichiers .doc non lus (à enregistrer en .docx avec Word).":
            "{n} old .doc files not read (save them as .docx with Word).",
        "{n} fichier d'un autre type ignoré.":
            "{n} file of another type skipped.",
        "{n} fichiers d'un autre type ignorés.":
            "{n} files of another type skipped.",
        "{n} document non reconnu : {noms}":
            "{n} document not recognised: {noms}",
        "{n} documents non reconnus : {noms}":
            "{n} documents not recognised: {noms}",
        "Documents non reconnus":
            "Documents not recognised",
        "Annuler":
            "Cancel",
        "✔  Valider":
            "✔  OK",
        "Un mot de passe":
            "A password",
        "Un contact":
            "A contact",
        "Facile à lire (des mots)":
            "Easy to read (words)",
        "Très solide (lettres et signes)":
            "Very strong (letters and symbols)",
        "mots":
            "words",
        "Mots de passe et contacts, sans internet":
            "Passwords and contacts, without internet",
        "Pocket Book est sans doute encore ouvert.\nFermez-le, puis cliquez à nouveau sur « Installer ».":
            "Pocket Book is probably still open.\nClose it, then click “Install” again.",
        "Vos fiches sont toujours dans :":
            "Your cards are still in:",
        "Pocket Book va être installé sur cet ordinateur.\nIl fonctionne sans internet : rien ne quitte l'ordinateur.\nVos fiches seront rangées dans :":
            "Pocket Book will be installed on this computer.\nIt works without internet: nothing leaves the computer.\nYour cards will be kept in:",
        "Fiches en texte":
            "Cards as text",
        "⚠ Le document « {nom} » a changé le {date} : vérifiez cette fiche (elle n'a pas été remplacée).":
            "⚠ The document “{nom}” changed on {date}: check this card (it was not replaced).",
        "Impossible de lire ce document ({erreur}).":
            "Could not read this document ({erreur}).",
        "Réglages":
            "Settings",
        "A":
            "A",
        "Enregistrer maintenant":
            "Save now",
        "Champ":
            "Field",
        "＋  Ajouter un champ":
            "＋  Add a field",
        "La copie .txt":
            "The .txt copy",
        "Le dossier":
            "The folder",
        "↻  Créer un nouveau mot de passe":
            "↻  Create a new password",
        "＋  Ajouter ce champ":
            "＋  Add this field",
        "Retirer le champ ?":
            "Remove the field?",
        "＋  Nouvelle":
            "＋  New",
        "Renommer":
            "Rename",
        "Couleur…":
            "Colour…",
        "Supprimer":
            "Delete",
        "Changer de dossier…":
            "Change folder…",
        "Ouvrir le dossier":
            "Open the folder",
        "Ouvrir dans Word":
            "Open in Word",
        "Une copie reste dans les sauvegardes du jour.":
            "A copy stays in today's backups.",
        "Changer le mot de passe ?":
            "Change the password?",
        "Voulez-vous vraiment changer le mot de passe de « {nom} » ?\n\nAttention : cela change seulement le carnet. Il faudra aussi le changer sur le site lui-même, sinon vous ne pourrez plus vous connecter.\n\n(L'ancien mot de passe sera gardé dans les notes.)":
            "Do you really want to change the password for “{nom}”?\n\nCareful: this only changes the notebook. You must also change it on the website itself, otherwise you will no longer be able to log in.\n\n(The old password will be kept in the notes.)",
        "Problème d'enregistrement":
            "Saving problem",
        "✔ Tout est enregistré (à {heure})":
            "✔ Everything is saved ({heure})",
        "✔ Enregistré (à {heure}) — ⚠ copie .txt impossible":
            "✔ Saved ({heure}) — ⚠ .txt copy failed",
        "Fermer quand même ?":
            "Close anyway?",
        "Le carnet n'a pas pu être enregistré.\nFermer quand même ?":
            "The notebook could not be saved.\nClose anyway?",
        "✔ Tout est enregistré":
            "✔ Everything is saved",
        "Copie des fiches en .txt : désactivée.":
            "Copy of cards as .txt: turned off.",
        "La copie .txt des fiches est maintenant dans :\n":
            "The .txt copy of the cards is now in:\n",
        "Aucun dossier choisi. Cliquez sur « Choisir le dossier… ».":
            "No folder chosen. Click “Choose the folder…”.",
        "Tout est déjà à jour : aucune fiche à créer ou à modifier.":
            "Everything is already up to date: no card to create or change.",
        "{n} document à ranger (sur {total})":
            "{n} document to file (out of {total})",
        "{n} documents à ranger (sur {total})":
            "{n} documents to file (out of {total})",
        "✔ Tout est rangé ({total} documents).\nCliquez sur « Tout » pour les revoir.":
            "✔ Everything is filed ({total} documents).\nClick “All” to see them again.",
        "{n} document trouvé":
            "{n} document found",
        "{n} documents trouvés":
            "{n} documents found",
        "⚠ {n} ancien fichier .doc non lu\n   (à enregistrer en .docx avec Word)":
            "⚠ {n} old .doc file not read\n   (save it as .docx with Word)",
        "⚠ {n} anciens fichiers .doc non lus\n   (à enregistrer en .docx avec Word)":
            "⚠ {n} old .doc files not read\n   (save them as .docx with Word)",
        "→  Voir la fiche":
            "→  See the card",
        "« {nom} » est déjà rangé dans le carnet.\nEn créer une autre fiche quand même ?":
            "“{nom}” is already filed in the notebook.\nCreate another card anyway?",
        "Rien de nouveau à ranger.\n\n":
            "Nothing new to file.\n\n",
        "Ranger ces documents ?":
            "File these documents?",
        "Les ranger quand même dans « Mes mots de passe » ?\n(leur texte ira dans les Notes de la fiche)":
            "File them anyway in “My passwords”?\n(their text will go into the card's Notes)",
        "Couleur pour « {nom} » :":
            "Colour for “{nom}”:",
        "↻  Un autre":
            "↻  Another one",
        "✔  Utiliser ce mot de passe":
            "✔  Use this password",
        "Fermer":
            "Close",
        "Ouvrir Pocket Book":
            "Open Pocket Book",
        "Désinstaller Pocket Book ?":
            "Uninstall Pocket Book?",
        "Supprimer aussi toutes mes fiches et leurs sauvegardes":
            "Also delete all my cards and their backups",
        "Supprimer les fiches ?":
            "Delete the cards?",
        "Désinstaller":
            "Uninstall",
        "Le carnet était abîmé. La sauvegarde du {date} a été reprise.":
            "The notebook was damaged. The backup from {date} has been restored.",
        "Texte":
            "Text",
        "Catégorie :":
            "Category:",
        "Ouvrir sur l'ordinateur :":
            "Open on the computer:",
        "Le document d'origine":
            "The original document",
        "Supprimer ce contact":
            "Delete this contact",
        "Supprimer cette fiche":
            "Delete this card",
        "Mot de passe":
            "Password",
        "✔  Terminé":
            "✔  Done",
        "Quel champ ajouter à cette fiche ?":
            "Which field should be added to this card?",
        "Ou un autre champ, à nommer (ex. : Numéro client, Question secrète) :":
            "Or another field, with your own name (e.g. Customer number, Secret question):",
        "Ranger tout seul les documents de ce dossier (nouveaux et modifiés), à chaque ouverture et toutes les minutes":
            "File the documents in this folder automatically (new and changed ones), at every start and every minute",
        "Montrer :":
            "Show:",
        "Chercher dans les documents":
            "Search in the documents",
        "Texte du document :":
            "Document text:",
        "✔ Copié":
            "✔ Copied",
        "⚠ Impossible d'enregistrer !":
            "⚠ Could not save!",
        "Le carnet n'a pas pu être enregistré.\n\n":
            "The notebook could not be saved.\n\n",
        "Le carnet est bien enregistré, mais la copie des fiches en .txt n'a pas pu être faite.\n\nLe dossier est peut-être débranché (clé USB, disque réseau).\n\n":
            "The notebook is saved, but the .txt copy of the cards could not be made.\n\nThe folder may be disconnected (USB stick, network drive).\n\n",
        "Copie de chaque fiche en .txt, mise à jour toute seule, dans :\n":
            "Copy of each card as .txt, updated automatically, in:\n",
        "Le fichier n'a pas pu être ouvert.\n\n":
            "The file could not be opened.\n\n",
        "Le dossier n'a pas pu être ouvert.\n\n":
            "The folder could not be opened.\n\n",
        "Dossier des documents :\n":
            "Documents folder:\n",
        "↻ Documents synchronisés à {heure} : ":
            "↻ Documents synced at {heure}: ",
        "Depuis les documents :\n\n   • ":
            "From the documents:\n\n   • ",
        "Le document n'a pas pu être ouvert.\n\n":
            "The document could not be opened.\n\n",
        "Documents Word et texte":
            "Word and text documents",
        "Tous les fichiers":
            "All files",
        "Les documents eux-mêmes ne sont pas modifiés. Continuer ?":
            "The documents themselves are not changed. Continue?",
        "{n} document ne ressemble ni à un mot de passe ni à un contact.":
            "{n} document looks like neither a password nor a contact.",
        "{n} documents ne ressemblent ni à un mot de passe ni à un contact.":
            "{n} documents look like neither a password nor a contact.",
        "Que contient ce document ?":
            "What does this document contain?",
        "Longueur :":
            "Length:",
        "L'ancien mot de passe sera gardé dans les notes de la fiche.":
            "The old password will be kept in the card's notes.",
        "caractères":
            "characters",
        "La copie du programme a échoué.":
            "Copying the program failed.",
        "Mettre une icône « Pocket Book » sur le Bureau":
            "Put a “Pocket Book” icon on the Desktop",
        "Mettre à jour":
            "Update",
        "Installer":
            "Install",
        "Installation en cours…":
            "Installing…",
        "Réessayer":
            "Try again",
        "Le programme et ses icônes vont être retirés de cet ordinateur.\nVos fiches sont gardées, dans :":
            "The program and its icons will be removed from this computer.\nYour cards are kept, in:",
        "Continuer ?":
            "Continue?",
        "Fiches supprimées":
            "Deleted cards",
        "fiche":
            "card",
        "Retirer « {champ} » de cette fiche ?\n\nCe qui est écrit dedans sera effacé :":
            "Remove “{champ}” from this card?\n\nWhat is written in it will be erased:",
        "Chercher un contact":
            "Search for a contact",
        "Chercher une fiche":
            "Search for a card",
        "＋  Nouveau contact":
            "＋  New contact",
        "＋  Nouvelle fiche":
            "＋  New card",
        "\n\nAstuce : glissez des fichiers .docx ou .txt (ou tout un dossier)\ndepuis l'Explorateur sur cette fenêtre pour les ranger d'un coup.":
            "\n\nTip: drag .docx or .txt files (or a whole folder)\nfrom your file manager onto this window to file them all at once.",
        "Lecture des documents : {i} sur {n}…":
            "Reading documents: {i} of {n}…",
        "… et {n} autres contacts":
            "… and {n} more contacts",
        "Mettre à jour Pocket Book":
            "Update Pocket Book",
        "Installer Pocket Book":
            "Install Pocket Book",
        "L'installation n'a pas pu se faire":
            "The installation could not be completed",
        "Pocket Book est installé":
            "Pocket Book is installed",
        "Ce fichier d'installation peut maintenant être rangé ou supprimé.":
            "This installation file can now be put away or deleted.",
        "Toutes les fiches, les sauvegardes et les copies .txt de ce dossier seront effacées définitivement :":
            "All cards, backups and .txt copies in this folder will be permanently erased:",
        "Ouvrir":
            "Open",
        "Venu du document : ":
            "From the document: ",
        "Le carnet n'a pas reconnu ce document. Vous pouvez quand même créer une fiche : il vous demandera s'il s'agit d'un mot de passe ou d'un contact.":
            "The notebook did not recognise this document. You can still create a card: it will ask whether it is a password or a contact.",
        "• Cliquez sur un nom dans la liste à gauche,\n":
            "• Click a name in the list on the left,\n",
        "• ou sur « Nouveau contact » pour en créer un.":
            "• or on “New contact” to create one.",
        "• ou sur « Nouvelle fiche » pour en créer une.":
            "• or on “New card” to create one.",
        "La lecture a échoué.":
            "Reading failed.",
        "Les documents n'ont pas pu être lus.\n\n":
            "The documents could not be read.\n\n",
        "{n} contact  →  « Mes contacts »":
            "{n} contact  →  “My contacts”",
        "{n} contacts  →  « Mes contacts »":
            "{n} contacts  →  “My contacts”",
        "Aucun contact n'est choisi.\n\n":
            "No contact is selected.\n\n",
        "Aucune fiche n'est choisie.\n\n":
            "No card is selected.\n\n",
        "{n} mot de passe  →  « Mes mots de passe »":
            "{n} password  →  “My passwords”",
        "{n} mots de passe  →  « Mes mots de passe »":
            "{n} passwords  →  “My passwords”",
        "Le carnet va ranger :":
            "The notebook will file:",
        "Catégorie":
            "Category",
        "Identifiant":
            "Username",
        "Adresse e-mail":
            "Email address",
        "Portable":
            "Mobile",
        "Téléphone fixe":
            "Landline",
        "Adresse":
            "Address",
        "Anniversaire":
            "Birthday",
        "Contact":
            "Contact",
        "?":
            "?",
        "un mot de passe":
            "a password",
        "un contact":
            "a contact",
        "non reconnu":
            "not recognised",
        "Bleu":
            "Blue",
        "Vert":
            "Green",
        "Jaune":
            "Yellow",
        "Orange":
            "Orange",
        "Rouge":
            "Red",
        "Violet":
            "Purple",
        "Rose":
            "Pink",
        "Turquoise":
            "Turquoise",
        "Gris":
            "Grey",
        "Marron":
            "Brown",
        "Banque":
            "Bank",
        "Administration":
            "Administration",
        "Santé":
            "Health",
        "Messagerie":
            "Email",
        "Achats":
            "Shopping",
        "Factures":
            "Bills",
        "Loisirs":
            "Leisure",
        "Famille":
            "Family",
        "Travail":
            "Work",
        "Clair":
            "Light",
        "Sombre":
            "Dark",
        "Contraste fort":
            "High contrast",
        "Sépia doux":
            "Soft sepia",
        "Autres":
            "Other",
        "À propos":
            "About",
        "Pocket Book {version} — fonctionne entièrement sans internet : rien ne quitte cet ordinateur.":
            "Pocket Book {version} — works entirely without internet: nothing leaves this computer.",
        "Vos données sont ici :":
            "Your data is here:",
        "Ouvrir le dossier des données":
            "Open the data folder",
        "Désinstaller…":
            "Uninstall…",
    },
    "es": {
        "(aucune)":
            "(ninguna)",
        "Toutes":
            "Todas",
        "Pocket Book a été désinstallé.":
            "Pocket Book se ha desinstalado.",
        "Type de fichier non pris en charge":
            "Tipo de archivo no compatible",
        "Ce fichier est réécrit à chaque changement : modifiez la fiche dans le carnet.":
            "Este archivo se reescribe con cada cambio: modifique la ficha en el cuaderno.",
        "Supprimer la catégorie « {nom} » ?":
            "¿Eliminar la categoría «{nom}»?",
        "Couleur de la catégorie":
            "Color de la categoría",
        "Quel genre de document ?":
            "¿Qué tipo de documento?",
        "Installation de Pocket Book":
            "Instalación de Pocket Book",
        "Désinstaller Pocket Book":
            "Desinstalar Pocket Book",
        "Sans nom":
            "Sin nombre",
        "Nouveau contact":
            "Nuevo contacto",
        "Nouvelle fiche":
            "Nueva ficha",
        "%d/%m/%Y à %H:%M":
            "%d/%m/%Y a las %H:%M",
        "Notes":
            "Notas",
        "Copie automatique faite par Pocket Book (fiche modifiée le {date}).":
            "Copia automática hecha por Pocket Book (ficha modificada el {date}).",
        "Copie automatique faite par Pocket Book.":
            "Copia automática hecha por Pocket Book.",
        "Nom":
            "Nombre",
        "Copier":
            "Copiar",
        "✎  Modifier à la main":
            "✎  Modificar a mano",
        "Ajouter un champ":
            "Añadir un campo",
        "Catégories":
            "Categorías",
        "Les catégories servent à trier les fiches. Chacune a sa couleur, qui apparaît dans la liste des fiches.":
            "Las categorías sirven para ordenar las fichas. Cada una tiene su color, que aparece en la lista de fichas.",
        "Langue":
            "Idioma",
        "Couleurs de l'écran":
            "Colores de la pantalla",
        "Choisissez ce qui est le plus agréable à lire.":
            "Elija lo que le resulte más cómodo de leer.",
        "Copie des fiches en .txt":
            "Copia de las fichas en .txt",
        "Chaque fiche est recopiée dans un fichier .txt, mis à jour tout seul. Les changements se font dans le carnet, pas dans les .txt.":
            "Cada ficha se copia en un archivo .txt que se actualiza solo. Los cambios se hacen en el cuaderno, no en los .txt.",
        "Nouvelle catégorie":
            "Nueva categoría",
        "Nom de la nouvelle catégorie :":
            "Nombre de la nueva categoría:",
        "Renommer la catégorie":
            "Cambiar el nombre de la categoría",
        "Nouveau nom :":
            "Nuevo nombre:",
        "＋  Créer une fiche avec ce document":
            "＋  Crear una ficha con este documento",
        "{n} contact":
            "{n} contacto",
        "{n} contacts":
            "{n} contactos",
        "{n} fiche":
            "{n} ficha",
        "{n} fiches":
            "{n} fichas",
        "Voulez-vous vraiment supprimer le contact « {nom} » ?":
            "¿Seguro que quiere eliminar el contacto «{nom}»?",
        "Voulez-vous vraiment supprimer la fiche « {nom} » ?":
            "¿Seguro que quiere eliminar la ficha «{nom}»?",
        "Ancien mot de passe (remplacé le {date}) : {ancien}":
            "Contraseña anterior (cambiada el {date}): {ancien}",
        "Aucun dossier choisi.":
            "Ninguna carpeta elegida.",
        "Ce document contenait {n} contacts : ils ont tous été créés.":
            "Este documento contenía {n} contactos: se han creado todos.",
        "La fiche a été remplie à partir du document.":
            "La ficha se ha rellenado a partir del documento.",
        "Vérifiez que chaque information est au bon endroit.":
            "Compruebe que cada dato está en su sitio.",
        "Fiche créée":
            "Ficha creada",
        "C'est rangé !":
            "¡Todo ordenado!",
        "{n} fiche créée.":
            "{n} ficha creada.",
        "{n} fiches créées.":
            "{n} fichas creadas.",
        "Créer un nouveau mot de passe":
            "Crear una contraseña nueva",
        "Une nouvelle version de Pocket Book va remplacer l'ancienne.\nVos fiches ne sont pas touchées.":
            "Una nueva versión de Pocket Book va a sustituir a la anterior.\nSus fichas no se tocan.",
        "Pour l'ouvrir, double-cliquez sur l'icône « Pocket Book » du Bureau\n(ou cherchez « Pocket Book » dans le menu des applications).":
            "Para abrirlo, haga doble clic en el icono «Pocket Book» del Escritorio\n(o busque «Pocket Book» en el menú de aplicaciones).",
        "Pour l'ouvrir, cherchez « Pocket Book » dans le menu des applications.":
            "Para abrirlo, busque «Pocket Book» en el menú de aplicaciones.",
        "Le carnet était abîmé et aucune sauvegarde n'a pu être lue. Une copie a été gardée : {fichier}":
            "El cuaderno estaba dañado y no se pudo leer ninguna copia de seguridad. Se ha guardado una copia: {fichier}",
        "Mes mots de passe":
            "Mis contraseñas",
        "Mes contacts":
            "Mis contactos",
        "Mes documents":
            "Mis documentos",
        "Cliquez d'abord sur une catégorie dans la liste.":
            "Primero haga clic en una categoría de la lista.",
        "La catégorie « {nom} » existe déjà.":
            "La categoría «{nom}» ya existe.",
        "{n} fiche n'aura plus de catégorie (la fiche elle-même n'est pas supprimée).":
            "{n} ficha se quedará sin categoría (la ficha no se elimina).",
        "{n} fiches n'auront plus de catégorie (les fiches elles-mêmes ne sont pas supprimées).":
            "{n} fichas se quedarán sin categoría (las fichas no se eliminan).",
        "Supprimer la catégorie ?":
            "¿Eliminar la categoría?",
        "↻  Synchroniser maintenant":
            "↻  Sincronizar ahora",
        "Choisir le dossier…":
            "Elegir la carpeta…",
        "Importer des fichiers…":
            "Importar archivos…",
        "À ranger":
            "Por ordenar",
        "Tout":
            "Todo",
        "Mots de passe":
            "Contraseñas",
        "Contacts":
            "Contactos",
        "Non reconnus":
            "No reconocidos",
        "Choisissez un document dans la liste.":
            "Elija un documento de la lista.",
        "Ce document n'est jamais modifié par le carnet.":
            "El cuaderno nunca modifica este documento.",
        "{n} contact trouvé":
            "{n} contacto encontrado",
        "{n} contacts trouvés":
            "{n} contactos encontrados",
        "{n} fiche trouvée":
            "{n} ficha encontrada",
        "{n} fiches trouvées":
            "{n} fichas encontradas",
        ", de A à Z":
            ", de la A a la Z",
        " à la lettre {lettre}":
            " con la letra {lettre}",
        "Supprimer ?":
            "¿Eliminar?",
        "Site internet":
            "Sitio web",
        "Aucune adresse de site n'est notée sur cette fiche.":
            "Esta ficha no tiene ninguna dirección de sitio web.",
        "%d/%m/%Y":
            "%d/%m/%Y",
        "✎ Modification en cours…":
            "✎ Modificando…",
        "Dans quel dossier ranger la copie .txt des fiches ?":
            "¿En qué carpeta guardar la copia .txt de las fichas?",
        "Choisissez un autre dossier que celui des documents d'origine\n(par exemple un sous-dossier « Fiches en texte »).":
            "Elija una carpeta distinta de la de los documentos originales\n(por ejemplo una subcarpeta «Fichas en texto»).",
        "\n\nL'ancien dossier n'a pas été modifié.":
            "\n\nLa carpeta anterior no se ha modificado.",
        "Ce fichier n'existe pas (ou plus) sur l'ordinateur.":
            "Este archivo no existe (o ya no existe) en el ordenador.",
        "Où sont rangés vos documents ?":
            "¿Dónde están guardados sus documentos?",
        "Choisissez d'abord le dossier où sont rangés vos documents.":
            "Primero elija la carpeta donde están guardados sus documentos.",
        "Lecture des documents…":
            "Leyendo los documentos…",
        "{n} fiche créée":
            "{n} ficha creada",
        "{n} fiches créées":
            "{n} fichas creadas",
        "{n} mise à jour":
            "{n} actualizada",
        "{n} mises à jour":
            "{n} actualizadas",
        "{n} à vérifier (⚠ dans les notes)":
            "{n} por revisar (⚠ en las notas)",
        "Synchronisation":
            "Sincronización",
        "{n} document":
            "{n} documento",
        "{n} documents":
            "{n} documentos",
        "✔ = déjà rangé dans le carnet":
            "✔ = ya ordenado en el cuaderno",
        "Reconnu comme : {genre}   —   ce document n'est jamais modifié.":
            "Reconocido como: {genre}   —   este documento nunca se modifica.",
        "(Document vide)":
            "(Documento vacío)",
        "Déjà rangé dans le carnet :":
            "Ya ordenado en el cuaderno:",
        "Ce que le carnet a compris :":
            "Lo que el cuaderno ha entendido:",
        "Choisissez d'abord un document dans la liste.":
            "Primero elija un documento de la lista.",
        "Choisissez les documents à ranger (plusieurs à la fois possible)":
            "Elija los documentos que quiere ordenar (puede elegir varios)",
        "{n} document déjà rangé : ignoré.":
            "{n} documento ya ordenado: omitido.",
        "{n} documents déjà rangés : ignorés.":
            "{n} documentos ya ordenados: omitidos.",
        "{n} ancien fichier .doc non lu (à enregistrer en .docx avec Word).":
            "{n} archivo .doc antiguo sin leer (guárdelo como .docx con Word).",
        "{n} anciens fichiers .doc non lus (à enregistrer en .docx avec Word).":
            "{n} archivos .doc antiguos sin leer (guárdelos como .docx con Word).",
        "{n} fichier d'un autre type ignoré.":
            "{n} archivo de otro tipo omitido.",
        "{n} fichiers d'un autre type ignorés.":
            "{n} archivos de otro tipo omitidos.",
        "{n} document non reconnu : {noms}":
            "{n} documento no reconocido: {noms}",
        "{n} documents non reconnus : {noms}":
            "{n} documentos no reconocidos: {noms}",
        "Documents non reconnus":
            "Documentos no reconocidos",
        "Annuler":
            "Cancelar",
        "✔  Valider":
            "✔  Aceptar",
        "Un mot de passe":
            "Una contraseña",
        "Un contact":
            "Un contacto",
        "Facile à lire (des mots)":
            "Fácil de leer (palabras)",
        "Très solide (lettres et signes)":
            "Muy segura (letras y símbolos)",
        "mots":
            "palabras",
        "Mots de passe et contacts, sans internet":
            "Contraseñas y contactos, sin internet",
        "Pocket Book est sans doute encore ouvert.\nFermez-le, puis cliquez à nouveau sur « Installer ».":
            "Pocket Book probablemente sigue abierto.\nCiérrelo y vuelva a hacer clic en «Instalar».",
        "Vos fiches sont toujours dans :":
            "Sus fichas siguen en:",
        "Pocket Book va être installé sur cet ordinateur.\nIl fonctionne sans internet : rien ne quitte l'ordinateur.\nVos fiches seront rangées dans :":
            "Pocket Book se va a instalar en este ordenador.\nFunciona sin internet: nada sale del ordenador.\nSus fichas se guardarán en:",
        "Fiches en texte":
            "Fichas en texto",
        "⚠ Le document « {nom} » a changé le {date} : vérifiez cette fiche (elle n'a pas été remplacée).":
            "⚠ El documento «{nom}» cambió el {date}: revise esta ficha (no se ha sustituido).",
        "Impossible de lire ce document ({erreur}).":
            "No se pudo leer este documento ({erreur}).",
        "Réglages":
            "Ajustes",
        "A":
            "A",
        "Enregistrer maintenant":
            "Guardar ahora",
        "Champ":
            "Campo",
        "＋  Ajouter un champ":
            "＋  Añadir un campo",
        "La copie .txt":
            "La copia .txt",
        "Le dossier":
            "La carpeta",
        "↻  Créer un nouveau mot de passe":
            "↻  Crear una contraseña nueva",
        "＋  Ajouter ce champ":
            "＋  Añadir este campo",
        "Retirer le champ ?":
            "¿Quitar el campo?",
        "＋  Nouvelle":
            "＋  Nueva",
        "Renommer":
            "Cambiar nombre",
        "Couleur…":
            "Color…",
        "Supprimer":
            "Eliminar",
        "Changer de dossier…":
            "Cambiar de carpeta…",
        "Ouvrir le dossier":
            "Abrir la carpeta",
        "Ouvrir dans Word":
            "Abrir en Word",
        "Une copie reste dans les sauvegardes du jour.":
            "Queda una copia en las copias de seguridad del día.",
        "Changer le mot de passe ?":
            "¿Cambiar la contraseña?",
        "Voulez-vous vraiment changer le mot de passe de « {nom} » ?\n\nAttention : cela change seulement le carnet. Il faudra aussi le changer sur le site lui-même, sinon vous ne pourrez plus vous connecter.\n\n(L'ancien mot de passe sera gardé dans les notes.)":
            "¿Seguro que quiere cambiar la contraseña de «{nom}»?\n\nAtención: esto solo cambia el cuaderno. También hay que cambiarla en el propio sitio web; si no, ya no podrá conectarse.\n\n(La contraseña anterior se guardará en las notas.)",
        "Problème d'enregistrement":
            "Problema al guardar",
        "✔ Tout est enregistré (à {heure})":
            "✔ Todo está guardado ({heure})",
        "✔ Enregistré (à {heure}) — ⚠ copie .txt impossible":
            "✔ Guardado ({heure}) — ⚠ copia .txt imposible",
        "Fermer quand même ?":
            "¿Cerrar de todos modos?",
        "Le carnet n'a pas pu être enregistré.\nFermer quand même ?":
            "No se pudo guardar el cuaderno.\n¿Cerrar de todos modos?",
        "✔ Tout est enregistré":
            "✔ Todo está guardado",
        "Copie des fiches en .txt : désactivée.":
            "Copia de las fichas en .txt: desactivada.",
        "La copie .txt des fiches est maintenant dans :\n":
            "La copia .txt de las fichas está ahora en:\n",
        "Aucun dossier choisi. Cliquez sur « Choisir le dossier… ».":
            "Ninguna carpeta elegida. Haga clic en «Elegir la carpeta…».",
        "Tout est déjà à jour : aucune fiche à créer ou à modifier.":
            "Todo está al día: ninguna ficha que crear o modificar.",
        "{n} document à ranger (sur {total})":
            "{n} documento por ordenar (de {total})",
        "{n} documents à ranger (sur {total})":
            "{n} documentos por ordenar (de {total})",
        "✔ Tout est rangé ({total} documents).\nCliquez sur « Tout » pour les revoir.":
            "✔ Todo está ordenado ({total} documentos).\nHaga clic en «Todo» para volver a verlos.",
        "{n} document trouvé":
            "{n} documento encontrado",
        "{n} documents trouvés":
            "{n} documentos encontrados",
        "⚠ {n} ancien fichier .doc non lu\n   (à enregistrer en .docx avec Word)":
            "⚠ {n} archivo .doc antiguo sin leer\n   (guárdelo como .docx con Word)",
        "⚠ {n} anciens fichiers .doc non lus\n   (à enregistrer en .docx avec Word)":
            "⚠ {n} archivos .doc antiguos sin leer\n   (guárdelos como .docx con Word)",
        "→  Voir la fiche":
            "→  Ver la ficha",
        "« {nom} » est déjà rangé dans le carnet.\nEn créer une autre fiche quand même ?":
            "«{nom}» ya está ordenado en el cuaderno.\n¿Crear otra ficha de todos modos?",
        "Rien de nouveau à ranger.\n\n":
            "Nada nuevo que ordenar.\n\n",
        "Ranger ces documents ?":
            "¿Ordenar estos documentos?",
        "Les ranger quand même dans « Mes mots de passe » ?\n(leur texte ira dans les Notes de la fiche)":
            "¿Ordenarlos de todos modos en «Mis contraseñas»?\n(su texto irá a las Notas de la ficha)",
        "Couleur pour « {nom} » :":
            "Color para «{nom}»:",
        "↻  Un autre":
            "↻  Otra",
        "✔  Utiliser ce mot de passe":
            "✔  Usar esta contraseña",
        "Fermer":
            "Cerrar",
        "Ouvrir Pocket Book":
            "Abrir Pocket Book",
        "Désinstaller Pocket Book ?":
            "¿Desinstalar Pocket Book?",
        "Supprimer aussi toutes mes fiches et leurs sauvegardes":
            "Eliminar también todas mis fichas y sus copias de seguridad",
        "Supprimer les fiches ?":
            "¿Eliminar las fichas?",
        "Désinstaller":
            "Desinstalar",
        "Le carnet était abîmé. La sauvegarde du {date} a été reprise.":
            "El cuaderno estaba dañado. Se ha recuperado la copia de seguridad del {date}.",
        "Texte":
            "Texto",
        "Catégorie :":
            "Categoría:",
        "Ouvrir sur l'ordinateur :":
            "Abrir en el ordenador:",
        "Le document d'origine":
            "El documento original",
        "Supprimer ce contact":
            "Eliminar este contacto",
        "Supprimer cette fiche":
            "Eliminar esta ficha",
        "Mot de passe":
            "Contraseña",
        "✔  Terminé":
            "✔  Hecho",
        "Quel champ ajouter à cette fiche ?":
            "¿Qué campo añadir a esta ficha?",
        "Ou un autre champ, à nommer (ex. : Numéro client, Question secrète) :":
            "U otro campo, con el nombre que quiera (p. ej.: Número de cliente, Pregunta secreta):",
        "Ranger tout seul les documents de ce dossier (nouveaux et modifiés), à chaque ouverture et toutes les minutes":
            "Ordenar solos los documentos de esta carpeta (nuevos y modificados), al abrir y cada minuto",
        "Montrer :":
            "Mostrar:",
        "Chercher dans les documents":
            "Buscar en los documentos",
        "Texte du document :":
            "Texto del documento:",
        "✔ Copié":
            "✔ Copiado",
        "⚠ Impossible d'enregistrer !":
            "⚠ ¡No se pudo guardar!",
        "Le carnet n'a pas pu être enregistré.\n\n":
            "No se pudo guardar el cuaderno.\n\n",
        "Le carnet est bien enregistré, mais la copie des fiches en .txt n'a pas pu être faite.\n\nLe dossier est peut-être débranché (clé USB, disque réseau).\n\n":
            "El cuaderno está guardado, pero no se pudo hacer la copia .txt de las fichas.\n\nQuizás la carpeta esté desconectada (memoria USB, disco de red).\n\n",
        "Copie de chaque fiche en .txt, mise à jour toute seule, dans :\n":
            "Copia de cada ficha en .txt, actualizada sola, en:\n",
        "Le fichier n'a pas pu être ouvert.\n\n":
            "No se pudo abrir el archivo.\n\n",
        "Le dossier n'a pas pu être ouvert.\n\n":
            "No se pudo abrir la carpeta.\n\n",
        "Dossier des documents :\n":
            "Carpeta de los documentos:\n",
        "↻ Documents synchronisés à {heure} : ":
            "↻ Documentos sincronizados a las {heure}: ",
        "Depuis les documents :\n\n   • ":
            "A partir de los documentos:\n\n   • ",
        "Le document n'a pas pu être ouvert.\n\n":
            "No se pudo abrir el documento.\n\n",
        "Documents Word et texte":
            "Documentos de Word y de texto",
        "Tous les fichiers":
            "Todos los archivos",
        "Les documents eux-mêmes ne sont pas modifiés. Continuer ?":
            "Los documentos en sí no se modifican. ¿Continuar?",
        "{n} document ne ressemble ni à un mot de passe ni à un contact.":
            "{n} documento no parece ni una contraseña ni un contacto.",
        "{n} documents ne ressemblent ni à un mot de passe ni à un contact.":
            "{n} documentos no parecen ni una contraseña ni un contacto.",
        "Que contient ce document ?":
            "¿Qué contiene este documento?",
        "Longueur :":
            "Longitud:",
        "L'ancien mot de passe sera gardé dans les notes de la fiche.":
            "La contraseña anterior se guardará en las notas de la ficha.",
        "caractères":
            "caracteres",
        "La copie du programme a échoué.":
            "No se pudo copiar el programa.",
        "Mettre une icône « Pocket Book » sur le Bureau":
            "Poner un icono «Pocket Book» en el Escritorio",
        "Mettre à jour":
            "Actualizar",
        "Installer":
            "Instalar",
        "Installation en cours…":
            "Instalando…",
        "Réessayer":
            "Reintentar",
        "Le programme et ses icônes vont être retirés de cet ordinateur.\nVos fiches sont gardées, dans :":
            "El programa y sus iconos se quitarán de este ordenador.\nSus fichas se conservan, en:",
        "Continuer ?":
            "¿Continuar?",
        "Fiches supprimées":
            "Fichas eliminadas",
        "fiche":
            "ficha",
        "Retirer « {champ} » de cette fiche ?\n\nCe qui est écrit dedans sera effacé :":
            "¿Quitar «{champ}» de esta ficha?\n\nLo que tiene escrito se borrará:",
        "Chercher un contact":
            "Buscar un contacto",
        "Chercher une fiche":
            "Buscar una ficha",
        "＋  Nouveau contact":
            "＋  Nuevo contacto",
        "＋  Nouvelle fiche":
            "＋  Nueva ficha",
        "\n\nAstuce : glissez des fichiers .docx ou .txt (ou tout un dossier)\ndepuis l'Explorateur sur cette fenêtre pour les ranger d'un coup.":
            "\n\nConsejo: arrastre archivos .docx o .txt (o una carpeta entera)\ndesde el explorador a esta ventana para ordenarlos de una vez.",
        "Lecture des documents : {i} sur {n}…":
            "Leyendo los documentos: {i} de {n}…",
        "… et {n} autres contacts":
            "… y {n} contactos más",
        "Mettre à jour Pocket Book":
            "Actualizar Pocket Book",
        "Installer Pocket Book":
            "Instalar Pocket Book",
        "L'installation n'a pas pu se faire":
            "No se pudo realizar la instalación",
        "Pocket Book est installé":
            "Pocket Book está instalado",
        "Ce fichier d'installation peut maintenant être rangé ou supprimé.":
            "Este archivo de instalación ya se puede guardar o eliminar.",
        "Toutes les fiches, les sauvegardes et les copies .txt de ce dossier seront effacées définitivement :":
            "Todas las fichas, copias de seguridad y copias .txt de esta carpeta se borrarán definitivamente:",
        "Ouvrir":
            "Abrir",
        "Venu du document : ":
            "Procede del documento: ",
        "Le carnet n'a pas reconnu ce document. Vous pouvez quand même créer une fiche : il vous demandera s'il s'agit d'un mot de passe ou d'un contact.":
            "El cuaderno no ha reconocido este documento. Aun así puede crear una ficha: le preguntará si es una contraseña o un contacto.",
        "• Cliquez sur un nom dans la liste à gauche,\n":
            "• Haga clic en un nombre de la lista de la izquierda,\n",
        "• ou sur « Nouveau contact » pour en créer un.":
            "• o en «Nuevo contacto» para crear uno.",
        "• ou sur « Nouvelle fiche » pour en créer une.":
            "• o en «Nueva ficha» para crear una.",
        "La lecture a échoué.":
            "La lectura ha fallado.",
        "Les documents n'ont pas pu être lus.\n\n":
            "No se pudieron leer los documentos.\n\n",
        "{n} contact  →  « Mes contacts »":
            "{n} contacto  →  «Mis contactos»",
        "{n} contacts  →  « Mes contacts »":
            "{n} contactos  →  «Mis contactos»",
        "Aucun contact n'est choisi.\n\n":
            "No hay ningún contacto elegido.\n\n",
        "Aucune fiche n'est choisie.\n\n":
            "No hay ninguna ficha elegida.\n\n",
        "{n} mot de passe  →  « Mes mots de passe »":
            "{n} contraseña  →  «Mis contraseñas»",
        "{n} mots de passe  →  « Mes mots de passe »":
            "{n} contraseñas  →  «Mis contraseñas»",
        "Le carnet va ranger :":
            "El cuaderno va a ordenar:",
        "Catégorie":
            "Categoría",
        "Identifiant":
            "Usuario",
        "Adresse e-mail":
            "Correo electrónico",
        "Portable":
            "Móvil",
        "Téléphone fixe":
            "Teléfono fijo",
        "Adresse":
            "Dirección",
        "Anniversaire":
            "Cumpleaños",
        "Contact":
            "Contacto",
        "?":
            "?",
        "un mot de passe":
            "una contraseña",
        "un contact":
            "un contacto",
        "non reconnu":
            "no reconocido",
        "Bleu":
            "Azul",
        "Vert":
            "Verde",
        "Jaune":
            "Amarillo",
        "Orange":
            "Naranja",
        "Rouge":
            "Rojo",
        "Violet":
            "Morado",
        "Rose":
            "Rosa",
        "Turquoise":
            "Turquesa",
        "Gris":
            "Gris",
        "Marron":
            "Marrón",
        "Banque":
            "Banco",
        "Administration":
            "Administración",
        "Santé":
            "Salud",
        "Messagerie":
            "Correo",
        "Achats":
            "Compras",
        "Factures":
            "Facturas",
        "Loisirs":
            "Ocio",
        "Famille":
            "Familia",
        "Travail":
            "Trabajo",
        "Clair":
            "Claro",
        "Sombre":
            "Oscuro",
        "Contraste fort":
            "Alto contraste",
        "Sépia doux":
            "Sepia suave",
        "Autres":
            "Otros",
        "À propos":
            "Acerca de",
        "Pocket Book {version} — fonctionne entièrement sans internet : rien ne quitte cet ordinateur.":
            "Pocket Book {version} — funciona totalmente sin internet: nada sale de este ordenador.",
        "Vos données sont ici :":
            "Sus datos están aquí:",
        "Ouvrir le dossier des données":
            "Abrir la carpeta de datos",
        "Désinstaller…":
            "Desinstalar…",
    },
    "de": {
        "(aucune)":
            "(keine)",
        "Toutes":
            "Alle",
        "Pocket Book a été désinstallé.":
            "Pocket Book wurde deinstalliert.",
        "Type de fichier non pris en charge":
            "Dateityp wird nicht unterstützt",
        "Ce fichier est réécrit à chaque changement : modifiez la fiche dans le carnet.":
            "Diese Datei wird bei jeder Änderung neu geschrieben: Bearbeiten Sie die Karte im Notizbuch.",
        "Supprimer la catégorie « {nom} » ?":
            "Kategorie „{nom}“ löschen?",
        "Couleur de la catégorie":
            "Farbe der Kategorie",
        "Quel genre de document ?":
            "Was für ein Dokument ist das?",
        "Installation de Pocket Book":
            "Installation von Pocket Book",
        "Désinstaller Pocket Book":
            "Pocket Book deinstallieren",
        "Sans nom":
            "Ohne Namen",
        "Nouveau contact":
            "Neuer Kontakt",
        "Nouvelle fiche":
            "Neue Karte",
        "%d/%m/%Y à %H:%M":
            "%d.%m.%Y um %H:%M",
        "Notes":
            "Notizen",
        "Copie automatique faite par Pocket Book (fiche modifiée le {date}).":
            "Automatische Kopie von Pocket Book (Karte geändert am {date}).",
        "Copie automatique faite par Pocket Book.":
            "Automatische Kopie von Pocket Book.",
        "Nom":
            "Name",
        "Copier":
            "Kopieren",
        "✎  Modifier à la main":
            "✎  Von Hand ändern",
        "Ajouter un champ":
            "Feld hinzufügen",
        "Catégories":
            "Kategorien",
        "Les catégories servent à trier les fiches. Chacune a sa couleur, qui apparaît dans la liste des fiches.":
            "Kategorien dienen zum Sortieren der Karten. Jede hat ihre eigene Farbe, die in der Kartenliste erscheint.",
        "Langue":
            "Sprache",
        "Couleurs de l'écran":
            "Bildschirmfarben",
        "Choisissez ce qui est le plus agréable à lire.":
            "Wählen Sie, was sich am angenehmsten lesen lässt.",
        "Copie des fiches en .txt":
            "Kopie der Karten als .txt",
        "Chaque fiche est recopiée dans un fichier .txt, mis à jour tout seul. Les changements se font dans le carnet, pas dans les .txt.":
            "Jede Karte wird in eine .txt-Datei kopiert, die sich selbst aktualisiert. Änderungen macht man im Notizbuch, nicht in den .txt-Dateien.",
        "Nouvelle catégorie":
            "Neue Kategorie",
        "Nom de la nouvelle catégorie :":
            "Name der neuen Kategorie:",
        "Renommer la catégorie":
            "Kategorie umbenennen",
        "Nouveau nom :":
            "Neuer Name:",
        "＋  Créer une fiche avec ce document":
            "＋  Karte aus diesem Dokument erstellen",
        "{n} contact":
            "{n} Kontakt",
        "{n} contacts":
            "{n} Kontakte",
        "{n} fiche":
            "{n} Karte",
        "{n} fiches":
            "{n} Karten",
        "Voulez-vous vraiment supprimer le contact « {nom} » ?":
            "Möchten Sie den Kontakt „{nom}“ wirklich löschen?",
        "Voulez-vous vraiment supprimer la fiche « {nom} » ?":
            "Möchten Sie die Karte „{nom}“ wirklich löschen?",
        "Ancien mot de passe (remplacé le {date}) : {ancien}":
            "Altes Passwort (ersetzt am {date}): {ancien}",
        "Aucun dossier choisi.":
            "Kein Ordner gewählt.",
        "Ce document contenait {n} contacts : ils ont tous été créés.":
            "Dieses Dokument enthielt {n} Kontakte: Alle wurden erstellt.",
        "La fiche a été remplie à partir du document.":
            "Die Karte wurde aus dem Dokument ausgefüllt.",
        "Vérifiez que chaque information est au bon endroit.":
            "Prüfen Sie, ob jede Angabe an der richtigen Stelle steht.",
        "Fiche créée":
            "Karte erstellt",
        "C'est rangé !":
            "Alles eingeordnet!",
        "{n} fiche créée.":
            "{n} Karte erstellt.",
        "{n} fiches créées.":
            "{n} Karten erstellt.",
        "Créer un nouveau mot de passe":
            "Neues Passwort erstellen",
        "Une nouvelle version de Pocket Book va remplacer l'ancienne.\nVos fiches ne sont pas touchées.":
            "Eine neue Version von Pocket Book ersetzt die alte.\nIhre Karten bleiben unberührt.",
        "Pour l'ouvrir, double-cliquez sur l'icône « Pocket Book » du Bureau\n(ou cherchez « Pocket Book » dans le menu des applications).":
            "Zum Öffnen doppelklicken Sie auf das Symbol „Pocket Book“ auf dem Desktop\n(oder suchen Sie „Pocket Book“ im Anwendungsmenü).",
        "Pour l'ouvrir, cherchez « Pocket Book » dans le menu des applications.":
            "Zum Öffnen suchen Sie „Pocket Book“ im Anwendungsmenü.",
        "Le carnet était abîmé et aucune sauvegarde n'a pu être lue. Une copie a été gardée : {fichier}":
            "Das Notizbuch war beschädigt und keine Sicherung konnte gelesen werden. Eine Kopie wurde aufbewahrt: {fichier}",
        "Mes mots de passe":
            "Meine Passwörter",
        "Mes contacts":
            "Meine Kontakte",
        "Mes documents":
            "Meine Dokumente",
        "Cliquez d'abord sur une catégorie dans la liste.":
            "Klicken Sie zuerst auf eine Kategorie in der Liste.",
        "La catégorie « {nom} » existe déjà.":
            "Die Kategorie „{nom}“ gibt es schon.",
        "{n} fiche n'aura plus de catégorie (la fiche elle-même n'est pas supprimée).":
            "{n} Karte hat dann keine Kategorie mehr (die Karte selbst wird nicht gelöscht).",
        "{n} fiches n'auront plus de catégorie (les fiches elles-mêmes ne sont pas supprimées).":
            "{n} Karten haben dann keine Kategorie mehr (die Karten selbst werden nicht gelöscht).",
        "Supprimer la catégorie ?":
            "Kategorie löschen?",
        "↻  Synchroniser maintenant":
            "↻  Jetzt abgleichen",
        "Choisir le dossier…":
            "Ordner wählen…",
        "Importer des fichiers…":
            "Dateien importieren…",
        "À ranger":
            "Einzuordnen",
        "Tout":
            "Alle",
        "Mots de passe":
            "Passwörter",
        "Contacts":
            "Kontakte",
        "Non reconnus":
            "Nicht erkannt",
        "Choisissez un document dans la liste.":
            "Wählen Sie ein Dokument in der Liste.",
        "Ce document n'est jamais modifié par le carnet.":
            "Dieses Dokument wird vom Notizbuch nie verändert.",
        "{n} contact trouvé":
            "{n} Kontakt gefunden",
        "{n} contacts trouvés":
            "{n} Kontakte gefunden",
        "{n} fiche trouvée":
            "{n} Karte gefunden",
        "{n} fiches trouvées":
            "{n} Karten gefunden",
        ", de A à Z":
            ", von A bis Z",
        " à la lettre {lettre}":
            " mit dem Buchstaben {lettre}",
        "Supprimer ?":
            "Löschen?",
        "Site internet":
            "Webseite",
        "Aucune adresse de site n'est notée sur cette fiche.":
            "Auf dieser Karte ist keine Webseite eingetragen.",
        "%d/%m/%Y":
            "%d.%m.%Y",
        "✎ Modification en cours…":
            "✎ Wird geändert…",
        "Dans quel dossier ranger la copie .txt des fiches ?":
            "In welchem Ordner soll die .txt-Kopie der Karten liegen?",
        "Choisissez un autre dossier que celui des documents d'origine\n(par exemple un sous-dossier « Fiches en texte »).":
            "Wählen Sie einen anderen Ordner als den der Originaldokumente\n(zum Beispiel einen Unterordner „Karten als Text“).",
        "\n\nL'ancien dossier n'a pas été modifié.":
            "\n\nDer alte Ordner wurde nicht verändert.",
        "Ce fichier n'existe pas (ou plus) sur l'ordinateur.":
            "Diese Datei existiert (nicht mehr) auf dem Computer.",
        "Où sont rangés vos documents ?":
            "Wo sind Ihre Dokumente gespeichert?",
        "Choisissez d'abord le dossier où sont rangés vos documents.":
            "Wählen Sie zuerst den Ordner, in dem Ihre Dokumente liegen.",
        "Lecture des documents…":
            "Dokumente werden gelesen…",
        "{n} fiche créée":
            "{n} Karte erstellt",
        "{n} fiches créées":
            "{n} Karten erstellt",
        "{n} mise à jour":
            "{n} aktualisiert",
        "{n} mises à jour":
            "{n} aktualisiert",
        "{n} à vérifier (⚠ dans les notes)":
            "{n} zu prüfen (⚠ in den Notizen)",
        "Synchronisation":
            "Abgleich",
        "{n} document":
            "{n} Dokument",
        "{n} documents":
            "{n} Dokumente",
        "✔ = déjà rangé dans le carnet":
            "✔ = schon im Notizbuch eingeordnet",
        "Reconnu comme : {genre}   —   ce document n'est jamais modifié.":
            "Erkannt als: {genre}   —   dieses Dokument wird nie verändert.",
        "(Document vide)":
            "(Leeres Dokument)",
        "Déjà rangé dans le carnet :":
            "Schon im Notizbuch eingeordnet:",
        "Ce que le carnet a compris :":
            "Was das Notizbuch verstanden hat:",
        "Choisissez d'abord un document dans la liste.":
            "Wählen Sie zuerst ein Dokument in der Liste.",
        "Choisissez les documents à ranger (plusieurs à la fois possible)":
            "Wählen Sie die einzuordnenden Dokumente (mehrere auf einmal möglich)",
        "{n} document déjà rangé : ignoré.":
            "{n} Dokument schon eingeordnet: übersprungen.",
        "{n} documents déjà rangés : ignorés.":
            "{n} Dokumente schon eingeordnet: übersprungen.",
        "{n} ancien fichier .doc non lu (à enregistrer en .docx avec Word).":
            "{n} alte .doc-Datei nicht gelesen (in Word als .docx speichern).",
        "{n} anciens fichiers .doc non lus (à enregistrer en .docx avec Word).":
            "{n} alte .doc-Dateien nicht gelesen (in Word als .docx speichern).",
        "{n} fichier d'un autre type ignoré.":
            "{n} Datei anderen Typs übersprungen.",
        "{n} fichiers d'un autre type ignorés.":
            "{n} Dateien anderen Typs übersprungen.",
        "{n} document non reconnu : {noms}":
            "{n} Dokument nicht erkannt: {noms}",
        "{n} documents non reconnus : {noms}":
            "{n} Dokumente nicht erkannt: {noms}",
        "Documents non reconnus":
            "Nicht erkannte Dokumente",
        "Annuler":
            "Abbrechen",
        "✔  Valider":
            "✔  OK",
        "Un mot de passe":
            "Ein Passwort",
        "Un contact":
            "Ein Kontakt",
        "Facile à lire (des mots)":
            "Leicht zu lesen (Wörter)",
        "Très solide (lettres et signes)":
            "Sehr sicher (Buchstaben und Zeichen)",
        "mots":
            "Wörter",
        "Mots de passe et contacts, sans internet":
            "Passwörter und Kontakte, ohne Internet",
        "Pocket Book est sans doute encore ouvert.\nFermez-le, puis cliquez à nouveau sur « Installer ».":
            "Pocket Book ist wahrscheinlich noch geöffnet.\nSchließen Sie es und klicken Sie erneut auf „Installieren“.",
        "Vos fiches sont toujours dans :":
            "Ihre Karten befinden sich weiterhin in:",
        "Pocket Book va être installé sur cet ordinateur.\nIl fonctionne sans internet : rien ne quitte l'ordinateur.\nVos fiches seront rangées dans :":
            "Pocket Book wird auf diesem Computer installiert.\nEs funktioniert ohne Internet: Nichts verlässt den Computer.\nIhre Karten werden gespeichert in:",
        "Fiches en texte":
            "Karten als Text",
        "⚠ Le document « {nom} » a changé le {date} : vérifiez cette fiche (elle n'a pas été remplacée).":
            "⚠ Das Dokument „{nom}“ hat sich am {date} geändert: Prüfen Sie diese Karte (sie wurde nicht ersetzt).",
        "Impossible de lire ce document ({erreur}).":
            "Dieses Dokument konnte nicht gelesen werden ({erreur}).",
        "Réglages":
            "Einstellungen",
        "A":
            "A",
        "Enregistrer maintenant":
            "Jetzt speichern",
        "Champ":
            "Feld",
        "＋  Ajouter un champ":
            "＋  Feld hinzufügen",
        "La copie .txt":
            "Die .txt-Kopie",
        "Le dossier":
            "Den Ordner",
        "↻  Créer un nouveau mot de passe":
            "↻  Neues Passwort erstellen",
        "＋  Ajouter ce champ":
            "＋  Dieses Feld hinzufügen",
        "Retirer le champ ?":
            "Feld entfernen?",
        "＋  Nouvelle":
            "＋  Neu",
        "Renommer":
            "Umbenennen",
        "Couleur…":
            "Farbe…",
        "Supprimer":
            "Löschen",
        "Changer de dossier…":
            "Ordner ändern…",
        "Ouvrir le dossier":
            "Ordner öffnen",
        "Ouvrir dans Word":
            "In Word öffnen",
        "Une copie reste dans les sauvegardes du jour.":
            "Eine Kopie bleibt in den heutigen Sicherungen.",
        "Changer le mot de passe ?":
            "Passwort ändern?",
        "Voulez-vous vraiment changer le mot de passe de « {nom} » ?\n\nAttention : cela change seulement le carnet. Il faudra aussi le changer sur le site lui-même, sinon vous ne pourrez plus vous connecter.\n\n(L'ancien mot de passe sera gardé dans les notes.)":
            "Möchten Sie das Passwort für „{nom}“ wirklich ändern?\n\nAchtung: Das ändert nur das Notizbuch. Sie müssen es auch auf der Webseite selbst ändern, sonst können Sie sich nicht mehr anmelden.\n\n(Das alte Passwort wird in den Notizen aufbewahrt.)",
        "Problème d'enregistrement":
            "Problem beim Speichern",
        "✔ Tout est enregistré (à {heure})":
            "✔ Alles gespeichert ({heure})",
        "✔ Enregistré (à {heure}) — ⚠ copie .txt impossible":
            "✔ Gespeichert ({heure}) — ⚠ .txt-Kopie fehlgeschlagen",
        "Fermer quand même ?":
            "Trotzdem schließen?",
        "Le carnet n'a pas pu être enregistré.\nFermer quand même ?":
            "Das Notizbuch konnte nicht gespeichert werden.\nTrotzdem schließen?",
        "✔ Tout est enregistré":
            "✔ Alles gespeichert",
        "Copie des fiches en .txt : désactivée.":
            "Kopie der Karten als .txt: ausgeschaltet.",
        "La copie .txt des fiches est maintenant dans :\n":
            "Die .txt-Kopie der Karten liegt jetzt in:\n",
        "Aucun dossier choisi. Cliquez sur « Choisir le dossier… ».":
            "Kein Ordner gewählt. Klicken Sie auf „Ordner wählen…“.",
        "Tout est déjà à jour : aucune fiche à créer ou à modifier.":
            "Alles ist aktuell: keine Karte zu erstellen oder zu ändern.",
        "{n} document à ranger (sur {total})":
            "{n} Dokument einzuordnen (von {total})",
        "{n} documents à ranger (sur {total})":
            "{n} Dokumente einzuordnen (von {total})",
        "✔ Tout est rangé ({total} documents).\nCliquez sur « Tout » pour les revoir.":
            "✔ Alles eingeordnet ({total} Dokumente).\nKlicken Sie auf „Alle“, um sie wieder zu sehen.",
        "{n} document trouvé":
            "{n} Dokument gefunden",
        "{n} documents trouvés":
            "{n} Dokumente gefunden",
        "⚠ {n} ancien fichier .doc non lu\n   (à enregistrer en .docx avec Word)":
            "⚠ {n} alte .doc-Datei nicht gelesen\n   (in Word als .docx speichern)",
        "⚠ {n} anciens fichiers .doc non lus\n   (à enregistrer en .docx avec Word)":
            "⚠ {n} alte .doc-Dateien nicht gelesen\n   (in Word als .docx speichern)",
        "→  Voir la fiche":
            "→  Karte ansehen",
        "« {nom} » est déjà rangé dans le carnet.\nEn créer une autre fiche quand même ?":
            "„{nom}“ ist schon im Notizbuch eingeordnet.\nTrotzdem eine weitere Karte erstellen?",
        "Rien de nouveau à ranger.\n\n":
            "Nichts Neues einzuordnen.\n\n",
        "Ranger ces documents ?":
            "Diese Dokumente einordnen?",
        "Les ranger quand même dans « Mes mots de passe » ?\n(leur texte ira dans les Notes de la fiche)":
            "Trotzdem unter „Meine Passwörter“ einordnen?\n(ihr Text kommt in die Notizen der Karte)",
        "Couleur pour « {nom} » :":
            "Farbe für „{nom}“:",
        "↻  Un autre":
            "↻  Ein anderes",
        "✔  Utiliser ce mot de passe":
            "✔  Dieses Passwort verwenden",
        "Fermer":
            "Schließen",
        "Ouvrir Pocket Book":
            "Pocket Book öffnen",
        "Désinstaller Pocket Book ?":
            "Pocket Book deinstallieren?",
        "Supprimer aussi toutes mes fiches et leurs sauvegardes":
            "Auch alle meine Karten und ihre Sicherungen löschen",
        "Supprimer les fiches ?":
            "Karten löschen?",
        "Désinstaller":
            "Deinstallieren",
        "Le carnet était abîmé. La sauvegarde du {date} a été reprise.":
            "Das Notizbuch war beschädigt. Die Sicherung vom {date} wurde wiederhergestellt.",
        "Texte":
            "Text",
        "Catégorie :":
            "Kategorie:",
        "Ouvrir sur l'ordinateur :":
            "Auf dem Computer öffnen:",
        "Le document d'origine":
            "Das Originaldokument",
        "Supprimer ce contact":
            "Diesen Kontakt löschen",
        "Supprimer cette fiche":
            "Diese Karte löschen",
        "Mot de passe":
            "Passwort",
        "✔  Terminé":
            "✔  Fertig",
        "Quel champ ajouter à cette fiche ?":
            "Welches Feld soll zu dieser Karte hinzugefügt werden?",
        "Ou un autre champ, à nommer (ex. : Numéro client, Question secrète) :":
            "Oder ein anderes Feld mit eigenem Namen (z. B. Kundennummer, Sicherheitsfrage):",
        "Ranger tout seul les documents de ce dossier (nouveaux et modifiés), à chaque ouverture et toutes les minutes":
            "Dokumente dieses Ordners automatisch einordnen (neue und geänderte), bei jedem Start und jede Minute",
        "Montrer :":
            "Zeigen:",
        "Chercher dans les documents":
            "In den Dokumenten suchen",
        "Texte du document :":
            "Text des Dokuments:",
        "✔ Copié":
            "✔ Kopiert",
        "⚠ Impossible d'enregistrer !":
            "⚠ Speichern nicht möglich!",
        "Le carnet n'a pas pu être enregistré.\n\n":
            "Das Notizbuch konnte nicht gespeichert werden.\n\n",
        "Le carnet est bien enregistré, mais la copie des fiches en .txt n'a pas pu être faite.\n\nLe dossier est peut-être débranché (clé USB, disque réseau).\n\n":
            "Das Notizbuch ist gespeichert, aber die .txt-Kopie der Karten konnte nicht erstellt werden.\n\nDer Ordner ist vielleicht nicht verbunden (USB-Stick, Netzlaufwerk).\n\n",
        "Copie de chaque fiche en .txt, mise à jour toute seule, dans :\n":
            "Kopie jeder Karte als .txt, automatisch aktualisiert, in:\n",
        "Le fichier n'a pas pu être ouvert.\n\n":
            "Die Datei konnte nicht geöffnet werden.\n\n",
        "Le dossier n'a pas pu être ouvert.\n\n":
            "Der Ordner konnte nicht geöffnet werden.\n\n",
        "Dossier des documents :\n":
            "Dokumentenordner:\n",
        "↻ Documents synchronisés à {heure} : ":
            "↻ Dokumente abgeglichen um {heure}: ",
        "Depuis les documents :\n\n   • ":
            "Aus den Dokumenten:\n\n   • ",
        "Le document n'a pas pu être ouvert.\n\n":
            "Das Dokument konnte nicht geöffnet werden.\n\n",
        "Documents Word et texte":
            "Word- und Textdokumente",
        "Tous les fichiers":
            "Alle Dateien",
        "Les documents eux-mêmes ne sont pas modifiés. Continuer ?":
            "Die Dokumente selbst werden nicht verändert. Fortfahren?",
        "{n} document ne ressemble ni à un mot de passe ni à un contact.":
            "{n} Dokument sieht weder wie ein Passwort noch wie ein Kontakt aus.",
        "{n} documents ne ressemblent ni à un mot de passe ni à un contact.":
            "{n} Dokumente sehen weder wie ein Passwort noch wie ein Kontakt aus.",
        "Que contient ce document ?":
            "Was enthält dieses Dokument?",
        "Longueur :":
            "Länge:",
        "L'ancien mot de passe sera gardé dans les notes de la fiche.":
            "Das alte Passwort wird in den Notizen der Karte aufbewahrt.",
        "caractères":
            "Zeichen",
        "La copie du programme a échoué.":
            "Das Kopieren des Programms ist fehlgeschlagen.",
        "Mettre une icône « Pocket Book » sur le Bureau":
            "Ein Symbol „Pocket Book“ auf den Desktop legen",
        "Mettre à jour":
            "Aktualisieren",
        "Installer":
            "Installieren",
        "Installation en cours…":
            "Wird installiert…",
        "Réessayer":
            "Erneut versuchen",
        "Le programme et ses icônes vont être retirés de cet ordinateur.\nVos fiches sont gardées, dans :":
            "Das Programm und seine Symbole werden von diesem Computer entfernt.\nIhre Karten bleiben erhalten, in:",
        "Continuer ?":
            "Fortfahren?",
        "Fiches supprimées":
            "Gelöschte Karten",
        "fiche":
            "Karte",
        "Retirer « {champ} » de cette fiche ?\n\nCe qui est écrit dedans sera effacé :":
            "„{champ}“ von dieser Karte entfernen?\n\nWas darin steht, wird gelöscht:",
        "Chercher un contact":
            "Einen Kontakt suchen",
        "Chercher une fiche":
            "Eine Karte suchen",
        "＋  Nouveau contact":
            "＋  Neuer Kontakt",
        "＋  Nouvelle fiche":
            "＋  Neue Karte",
        "\n\nAstuce : glissez des fichiers .docx ou .txt (ou tout un dossier)\ndepuis l'Explorateur sur cette fenêtre pour les ranger d'un coup.":
            "\n\nTipp: Ziehen Sie .docx- oder .txt-Dateien (oder einen ganzen Ordner)\naus dem Datei-Explorer in dieses Fenster, um sie auf einmal einzuordnen.",
        "Lecture des documents : {i} sur {n}…":
            "Dokumente werden gelesen: {i} von {n}…",
        "… et {n} autres contacts":
            "… und {n} weitere Kontakte",
        "Mettre à jour Pocket Book":
            "Pocket Book aktualisieren",
        "Installer Pocket Book":
            "Pocket Book installieren",
        "L'installation n'a pas pu se faire":
            "Die Installation konnte nicht durchgeführt werden",
        "Pocket Book est installé":
            "Pocket Book ist installiert",
        "Ce fichier d'installation peut maintenant être rangé ou supprimé.":
            "Diese Installationsdatei kann jetzt weggelegt oder gelöscht werden.",
        "Toutes les fiches, les sauvegardes et les copies .txt de ce dossier seront effacées définitivement :":
            "Alle Karten, Sicherungen und .txt-Kopien in diesem Ordner werden endgültig gelöscht:",
        "Ouvrir":
            "Öffnen",
        "Venu du document : ":
            "Aus dem Dokument: ",
        "Le carnet n'a pas reconnu ce document. Vous pouvez quand même créer une fiche : il vous demandera s'il s'agit d'un mot de passe ou d'un contact.":
            "Das Notizbuch hat dieses Dokument nicht erkannt. Sie können trotzdem eine Karte erstellen: Es fragt Sie, ob es ein Passwort oder ein Kontakt ist.",
        "• Cliquez sur un nom dans la liste à gauche,\n":
            "• Klicken Sie links in der Liste auf einen Namen,\n",
        "• ou sur « Nouveau contact » pour en créer un.":
            "• oder auf „Neuer Kontakt“, um einen anzulegen.",
        "• ou sur « Nouvelle fiche » pour en créer une.":
            "• oder auf „Neue Karte“, um eine anzulegen.",
        "La lecture a échoué.":
            "Das Lesen ist fehlgeschlagen.",
        "Les documents n'ont pas pu être lus.\n\n":
            "Die Dokumente konnten nicht gelesen werden.\n\n",
        "{n} contact  →  « Mes contacts »":
            "{n} Kontakt  →  „Meine Kontakte“",
        "{n} contacts  →  « Mes contacts »":
            "{n} Kontakte  →  „Meine Kontakte“",
        "Aucun contact n'est choisi.\n\n":
            "Kein Kontakt ausgewählt.\n\n",
        "Aucune fiche n'est choisie.\n\n":
            "Keine Karte ausgewählt.\n\n",
        "{n} mot de passe  →  « Mes mots de passe »":
            "{n} Passwort  →  „Meine Passwörter“",
        "{n} mots de passe  →  « Mes mots de passe »":
            "{n} Passwörter  →  „Meine Passwörter“",
        "Le carnet va ranger :":
            "Das Notizbuch ordnet ein:",
        "Catégorie":
            "Kategorie",
        "Identifiant":
            "Benutzername",
        "Adresse e-mail":
            "E-Mail-Adresse",
        "Portable":
            "Handy",
        "Téléphone fixe":
            "Festnetz",
        "Adresse":
            "Adresse",
        "Anniversaire":
            "Geburtstag",
        "Contact":
            "Kontakt",
        "?":
            "?",
        "un mot de passe":
            "ein Passwort",
        "un contact":
            "ein Kontakt",
        "non reconnu":
            "nicht erkannt",
        "Bleu":
            "Blau",
        "Vert":
            "Grün",
        "Jaune":
            "Gelb",
        "Orange":
            "Orange",
        "Rouge":
            "Rot",
        "Violet":
            "Violett",
        "Rose":
            "Rosa",
        "Turquoise":
            "Türkis",
        "Gris":
            "Grau",
        "Marron":
            "Braun",
        "Banque":
            "Bank",
        "Administration":
            "Behörden",
        "Santé":
            "Gesundheit",
        "Messagerie":
            "E-Mail",
        "Achats":
            "Einkäufe",
        "Factures":
            "Rechnungen",
        "Loisirs":
            "Freizeit",
        "Famille":
            "Familie",
        "Travail":
            "Arbeit",
        "Clair":
            "Hell",
        "Sombre":
            "Dunkel",
        "Contraste fort":
            "Hoher Kontrast",
        "Sépia doux":
            "Sanftes Sepia",
        "Autres":
            "Sonstige",
        "À propos":
            "Über",
        "Pocket Book {version} — fonctionne entièrement sans internet : rien ne quitte cet ordinateur.":
            "Pocket Book {version} — funktioniert komplett ohne Internet: Nichts verlässt diesen Computer.",
        "Vos données sont ici :":
            "Ihre Daten liegen hier:",
        "Ouvrir le dossier des données":
            "Datenordner öffnen",
        "Désinstaller…":
            "Deinstallieren…",
    },
    "it": {
        "(aucune)":
            "(nessuna)",
        "Toutes":
            "Tutte",
        "Pocket Book a été désinstallé.":
            "Pocket Book è stato disinstallato.",
        "Type de fichier non pris en charge":
            "Tipo di file non supportato",
        "Ce fichier est réécrit à chaque changement : modifiez la fiche dans le carnet.":
            "Questo file viene riscritto a ogni modifica: modificate la scheda nel quaderno.",
        "Supprimer la catégorie « {nom} » ?":
            "Eliminare la categoria «{nom}»?",
        "Couleur de la catégorie":
            "Colore della categoria",
        "Quel genre de document ?":
            "Che tipo di documento è?",
        "Installation de Pocket Book":
            "Installazione di Pocket Book",
        "Désinstaller Pocket Book":
            "Disinstalla Pocket Book",
        "Sans nom":
            "Senza nome",
        "Nouveau contact":
            "Nuovo contatto",
        "Nouvelle fiche":
            "Nuova scheda",
        "%d/%m/%Y à %H:%M":
            "%d/%m/%Y alle %H:%M",
        "Notes":
            "Note",
        "Copie automatique faite par Pocket Book (fiche modifiée le {date}).":
            "Copia automatica fatta da Pocket Book (scheda modificata il {date}).",
        "Copie automatique faite par Pocket Book.":
            "Copia automatica fatta da Pocket Book.",
        "Nom":
            "Nome",
        "Copier":
            "Copia",
        "✎  Modifier à la main":
            "✎  Modifica a mano",
        "Ajouter un champ":
            "Aggiungi un campo",
        "Catégories":
            "Categorie",
        "Les catégories servent à trier les fiches. Chacune a sa couleur, qui apparaît dans la liste des fiches.":
            "Le categorie servono a ordinare le schede. Ognuna ha il suo colore, che appare nell'elenco delle schede.",
        "Langue":
            "Lingua",
        "Couleurs de l'écran":
            "Colori dello schermo",
        "Choisissez ce qui est le plus agréable à lire.":
            "Scegliete ciò che è più comodo da leggere.",
        "Copie des fiches en .txt":
            "Copia delle schede in .txt",
        "Chaque fiche est recopiée dans un fichier .txt, mis à jour tout seul. Les changements se font dans le carnet, pas dans les .txt.":
            "Ogni scheda viene copiata in un file .txt che si aggiorna da solo. Le modifiche si fanno nel quaderno, non nei .txt.",
        "Nouvelle catégorie":
            "Nuova categoria",
        "Nom de la nouvelle catégorie :":
            "Nome della nuova categoria:",
        "Renommer la catégorie":
            "Rinomina la categoria",
        "Nouveau nom :":
            "Nuovo nome:",
        "＋  Créer une fiche avec ce document":
            "＋  Crea una scheda da questo documento",
        "{n} contact":
            "{n} contatto",
        "{n} contacts":
            "{n} contatti",
        "{n} fiche":
            "{n} scheda",
        "{n} fiches":
            "{n} schede",
        "Voulez-vous vraiment supprimer le contact « {nom} » ?":
            "Volete davvero eliminare il contatto «{nom}»?",
        "Voulez-vous vraiment supprimer la fiche « {nom} » ?":
            "Volete davvero eliminare la scheda «{nom}»?",
        "Ancien mot de passe (remplacé le {date}) : {ancien}":
            "Vecchia password (sostituita il {date}): {ancien}",
        "Aucun dossier choisi.":
            "Nessuna cartella scelta.",
        "Ce document contenait {n} contacts : ils ont tous été créés.":
            "Questo documento conteneva {n} contatti: sono stati creati tutti.",
        "La fiche a été remplie à partir du document.":
            "La scheda è stata compilata a partire dal documento.",
        "Vérifiez que chaque information est au bon endroit.":
            "Controllate che ogni informazione sia al posto giusto.",
        "Fiche créée":
            "Scheda creata",
        "C'est rangé !":
            "Tutto sistemato!",
        "{n} fiche créée.":
            "{n} scheda creata.",
        "{n} fiches créées.":
            "{n} schede create.",
        "Créer un nouveau mot de passe":
            "Crea una nuova password",
        "Une nouvelle version de Pocket Book va remplacer l'ancienne.\nVos fiches ne sont pas touchées.":
            "Una nuova versione di Pocket Book sostituirà quella vecchia.\nLe vostre schede non vengono toccate.",
        "Pour l'ouvrir, double-cliquez sur l'icône « Pocket Book » du Bureau\n(ou cherchez « Pocket Book » dans le menu des applications).":
            "Per aprirlo, fate doppio clic sull'icona «Pocket Book» sul Desktop\n(oppure cercate «Pocket Book» nel menu delle applicazioni).",
        "Pour l'ouvrir, cherchez « Pocket Book » dans le menu des applications.":
            "Per aprirlo, cercate «Pocket Book» nel menu delle applicazioni.",
        "Le carnet était abîmé et aucune sauvegarde n'a pu être lue. Une copie a été gardée : {fichier}":
            "Il quaderno era danneggiato e nessun backup ha potuto essere letto. È stata conservata una copia: {fichier}",
        "Mes mots de passe":
            "Le mie password",
        "Mes contacts":
            "I miei contatti",
        "Mes documents":
            "I miei documenti",
        "Cliquez d'abord sur une catégorie dans la liste.":
            "Prima fate clic su una categoria nell'elenco.",
        "La catégorie « {nom} » existe déjà.":
            "La categoria «{nom}» esiste già.",
        "{n} fiche n'aura plus de catégorie (la fiche elle-même n'est pas supprimée).":
            "{n} scheda non avrà più una categoria (la scheda stessa non viene eliminata).",
        "{n} fiches n'auront plus de catégorie (les fiches elles-mêmes ne sont pas supprimées).":
            "{n} schede non avranno più una categoria (le schede stesse non vengono eliminate).",
        "Supprimer la catégorie ?":
            "Eliminare la categoria?",
        "↻  Synchroniser maintenant":
            "↻  Sincronizza ora",
        "Choisir le dossier…":
            "Scegli la cartella…",
        "Importer des fichiers…":
            "Importa file…",
        "À ranger":
            "Da sistemare",
        "Tout":
            "Tutto",
        "Mots de passe":
            "Password",
        "Contacts":
            "Contatti",
        "Non reconnus":
            "Non riconosciuti",
        "Choisissez un document dans la liste.":
            "Scegliete un documento nell'elenco.",
        "Ce document n'est jamais modifié par le carnet.":
            "Questo documento non viene mai modificato dal quaderno.",
        "{n} contact trouvé":
            "{n} contatto trovato",
        "{n} contacts trouvés":
            "{n} contatti trovati",
        "{n} fiche trouvée":
            "{n} scheda trovata",
        "{n} fiches trouvées":
            "{n} schede trovate",
        ", de A à Z":
            ", dalla A alla Z",
        " à la lettre {lettre}":
            " con la lettera {lettre}",
        "Supprimer ?":
            "Eliminare?",
        "Site internet":
            "Sito web",
        "Aucune adresse de site n'est notée sur cette fiche.":
            "Su questa scheda non è indicato nessun sito web.",
        "%d/%m/%Y":
            "%d/%m/%Y",
        "✎ Modification en cours…":
            "✎ Modifica in corso…",
        "Dans quel dossier ranger la copie .txt des fiches ?":
            "In quale cartella mettere la copia .txt delle schede?",
        "Choisissez un autre dossier que celui des documents d'origine\n(par exemple un sous-dossier « Fiches en texte »).":
            "Scegliete una cartella diversa da quella dei documenti originali\n(per esempio una sottocartella «Schede in testo»).",
        "\n\nL'ancien dossier n'a pas été modifié.":
            "\n\nLa vecchia cartella non è stata modificata.",
        "Ce fichier n'existe pas (ou plus) sur l'ordinateur.":
            "Questo file non esiste (o non esiste più) sul computer.",
        "Où sont rangés vos documents ?":
            "Dove sono conservati i vostri documenti?",
        "Choisissez d'abord le dossier où sont rangés vos documents.":
            "Prima scegliete la cartella dove sono conservati i vostri documenti.",
        "Lecture des documents…":
            "Lettura dei documenti…",
        "{n} fiche créée":
            "{n} scheda creata",
        "{n} fiches créées":
            "{n} schede create",
        "{n} mise à jour":
            "{n} aggiornata",
        "{n} mises à jour":
            "{n} aggiornate",
        "{n} à vérifier (⚠ dans les notes)":
            "{n} da controllare (⚠ nelle note)",
        "Synchronisation":
            "Sincronizzazione",
        "{n} document":
            "{n} documento",
        "{n} documents":
            "{n} documenti",
        "✔ = déjà rangé dans le carnet":
            "✔ = già sistemato nel quaderno",
        "Reconnu comme : {genre}   —   ce document n'est jamais modifié.":
            "Riconosciuto come: {genre}   —   questo documento non viene mai modificato.",
        "(Document vide)":
            "(Documento vuoto)",
        "Déjà rangé dans le carnet :":
            "Già sistemato nel quaderno:",
        "Ce que le carnet a compris :":
            "Ciò che il quaderno ha capito:",
        "Choisissez d'abord un document dans la liste.":
            "Prima scegliete un documento nell'elenco.",
        "Choisissez les documents à ranger (plusieurs à la fois possible)":
            "Scegliete i documenti da sistemare (anche più di uno)",
        "{n} document déjà rangé : ignoré.":
            "{n} documento già sistemato: saltato.",
        "{n} documents déjà rangés : ignorés.":
            "{n} documenti già sistemati: saltati.",
        "{n} ancien fichier .doc non lu (à enregistrer en .docx avec Word).":
            "{n} vecchio file .doc non letto (salvatelo in .docx con Word).",
        "{n} anciens fichiers .doc non lus (à enregistrer en .docx avec Word).":
            "{n} vecchi file .doc non letti (salvateli in .docx con Word).",
        "{n} fichier d'un autre type ignoré.":
            "{n} file di altro tipo saltato.",
        "{n} fichiers d'un autre type ignorés.":
            "{n} file di altro tipo saltati.",
        "{n} document non reconnu : {noms}":
            "{n} documento non riconosciuto: {noms}",
        "{n} documents non reconnus : {noms}":
            "{n} documenti non riconosciuti: {noms}",
        "Documents non reconnus":
            "Documenti non riconosciuti",
        "Annuler":
            "Annulla",
        "✔  Valider":
            "✔  Conferma",
        "Un mot de passe":
            "Una password",
        "Un contact":
            "Un contatto",
        "Facile à lire (des mots)":
            "Facile da leggere (parole)",
        "Très solide (lettres et signes)":
            "Molto sicura (lettere e simboli)",
        "mots":
            "parole",
        "Mots de passe et contacts, sans internet":
            "Password e contatti, senza internet",
        "Pocket Book est sans doute encore ouvert.\nFermez-le, puis cliquez à nouveau sur « Installer ».":
            "Pocket Book è probabilmente ancora aperto.\nChiudetelo, poi fate di nuovo clic su «Installa».",
        "Vos fiches sont toujours dans :":
            "Le vostre schede sono sempre in:",
        "Pocket Book va être installé sur cet ordinateur.\nIl fonctionne sans internet : rien ne quitte l'ordinateur.\nVos fiches seront rangées dans :":
            "Pocket Book sarà installato su questo computer.\nFunziona senza internet: niente lascia il computer.\nLe vostre schede saranno conservate in:",
        "Fiches en texte":
            "Schede in testo",
        "⚠ Le document « {nom} » a changé le {date} : vérifiez cette fiche (elle n'a pas été remplacée).":
            "⚠ Il documento «{nom}» è cambiato il {date}: controllate questa scheda (non è stata sostituita).",
        "Impossible de lire ce document ({erreur}).":
            "Impossibile leggere questo documento ({erreur}).",
        "Réglages":
            "Impostazioni",
        "A":
            "A",
        "Enregistrer maintenant":
            "Salva ora",
        "Champ":
            "Campo",
        "＋  Ajouter un champ":
            "＋  Aggiungi un campo",
        "La copie .txt":
            "La copia .txt",
        "Le dossier":
            "La cartella",
        "↻  Créer un nouveau mot de passe":
            "↻  Crea una nuova password",
        "＋  Ajouter ce champ":
            "＋  Aggiungi questo campo",
        "Retirer le champ ?":
            "Togliere il campo?",
        "＋  Nouvelle":
            "＋  Nuova",
        "Renommer":
            "Rinomina",
        "Couleur…":
            "Colore…",
        "Supprimer":
            "Elimina",
        "Changer de dossier…":
            "Cambia cartella…",
        "Ouvrir le dossier":
            "Apri la cartella",
        "Ouvrir dans Word":
            "Apri in Word",
        "Une copie reste dans les sauvegardes du jour.":
            "Una copia resta nei backup di oggi.",
        "Changer le mot de passe ?":
            "Cambiare la password?",
        "Voulez-vous vraiment changer le mot de passe de « {nom} » ?\n\nAttention : cela change seulement le carnet. Il faudra aussi le changer sur le site lui-même, sinon vous ne pourrez plus vous connecter.\n\n(L'ancien mot de passe sera gardé dans les notes.)":
            "Volete davvero cambiare la password di «{nom}»?\n\nAttenzione: questo cambia solo il quaderno. Bisogna cambiarla anche sul sito stesso, altrimenti non potrete più accedere.\n\n(La vecchia password sarà conservata nelle note.)",
        "Problème d'enregistrement":
            "Problema di salvataggio",
        "✔ Tout est enregistré (à {heure})":
            "✔ Tutto è salvato ({heure})",
        "✔ Enregistré (à {heure}) — ⚠ copie .txt impossible":
            "✔ Salvato ({heure}) — ⚠ copia .txt impossibile",
        "Fermer quand même ?":
            "Chiudere comunque?",
        "Le carnet n'a pas pu être enregistré.\nFermer quand même ?":
            "Il quaderno non è stato salvato.\nChiudere comunque?",
        "✔ Tout est enregistré":
            "✔ Tutto è salvato",
        "Copie des fiches en .txt : désactivée.":
            "Copia delle schede in .txt: disattivata.",
        "La copie .txt des fiches est maintenant dans :\n":
            "La copia .txt delle schede ora è in:\n",
        "Aucun dossier choisi. Cliquez sur « Choisir le dossier… ».":
            "Nessuna cartella scelta. Fate clic su «Scegli la cartella…».",
        "Tout est déjà à jour : aucune fiche à créer ou à modifier.":
            "Tutto è già aggiornato: nessuna scheda da creare o modificare.",
        "{n} document à ranger (sur {total})":
            "{n} documento da sistemare (su {total})",
        "{n} documents à ranger (sur {total})":
            "{n} documenti da sistemare (su {total})",
        "✔ Tout est rangé ({total} documents).\nCliquez sur « Tout » pour les revoir.":
            "✔ Tutto è sistemato ({total} documenti).\nFate clic su «Tutto» per rivederli.",
        "{n} document trouvé":
            "{n} documento trovato",
        "{n} documents trouvés":
            "{n} documenti trovati",
        "⚠ {n} ancien fichier .doc non lu\n   (à enregistrer en .docx avec Word)":
            "⚠ {n} vecchio file .doc non letto\n   (salvatelo in .docx con Word)",
        "⚠ {n} anciens fichiers .doc non lus\n   (à enregistrer en .docx avec Word)":
            "⚠ {n} vecchi file .doc non letti\n   (salvateli in .docx con Word)",
        "→  Voir la fiche":
            "→  Vedi la scheda",
        "« {nom} » est déjà rangé dans le carnet.\nEn créer une autre fiche quand même ?":
            "«{nom}» è già sistemato nel quaderno.\nCreare comunque un'altra scheda?",
        "Rien de nouveau à ranger.\n\n":
            "Niente di nuovo da sistemare.\n\n",
        "Ranger ces documents ?":
            "Sistemare questi documenti?",
        "Les ranger quand même dans « Mes mots de passe » ?\n(leur texte ira dans les Notes de la fiche)":
            "Sistemarli comunque in «Le mie password»?\n(il loro testo andrà nelle Note della scheda)",
        "Couleur pour « {nom} » :":
            "Colore per «{nom}»:",
        "↻  Un autre":
            "↻  Un'altra",
        "✔  Utiliser ce mot de passe":
            "✔  Usa questa password",
        "Fermer":
            "Chiudi",
        "Ouvrir Pocket Book":
            "Apri Pocket Book",
        "Désinstaller Pocket Book ?":
            "Disinstallare Pocket Book?",
        "Supprimer aussi toutes mes fiches et leurs sauvegardes":
            "Elimina anche tutte le mie schede e i loro backup",
        "Supprimer les fiches ?":
            "Eliminare le schede?",
        "Désinstaller":
            "Disinstalla",
        "Le carnet était abîmé. La sauvegarde du {date} a été reprise.":
            "Il quaderno era danneggiato. È stato ripristinato il backup del {date}.",
        "Texte":
            "Testo",
        "Catégorie :":
            "Categoria:",
        "Ouvrir sur l'ordinateur :":
            "Apri sul computer:",
        "Le document d'origine":
            "Il documento originale",
        "Supprimer ce contact":
            "Elimina questo contatto",
        "Supprimer cette fiche":
            "Elimina questa scheda",
        "Mot de passe":
            "Password",
        "✔  Terminé":
            "✔  Fatto",
        "Quel champ ajouter à cette fiche ?":
            "Quale campo aggiungere a questa scheda?",
        "Ou un autre champ, à nommer (ex. : Numéro client, Question secrète) :":
            "Oppure un altro campo, con il nome che volete (es.: Codice cliente, Domanda segreta):",
        "Ranger tout seul les documents de ce dossier (nouveaux et modifiés), à chaque ouverture et toutes les minutes":
            "Sistema da solo i documenti di questa cartella (nuovi e modificati), a ogni apertura e ogni minuto",
        "Montrer :":
            "Mostra:",
        "Chercher dans les documents":
            "Cerca nei documenti",
        "Texte du document :":
            "Testo del documento:",
        "✔ Copié":
            "✔ Copiato",
        "⚠ Impossible d'enregistrer !":
            "⚠ Salvataggio impossibile!",
        "Le carnet n'a pas pu être enregistré.\n\n":
            "Il quaderno non è stato salvato.\n\n",
        "Le carnet est bien enregistré, mais la copie des fiches en .txt n'a pas pu être faite.\n\nLe dossier est peut-être débranché (clé USB, disque réseau).\n\n":
            "Il quaderno è salvato, ma la copia .txt delle schede non è stata fatta.\n\nForse la cartella è scollegata (chiavetta USB, disco di rete).\n\n",
        "Copie de chaque fiche en .txt, mise à jour toute seule, dans :\n":
            "Copia di ogni scheda in .txt, aggiornata da sola, in:\n",
        "Le fichier n'a pas pu être ouvert.\n\n":
            "Impossibile aprire il file.\n\n",
        "Le dossier n'a pas pu être ouvert.\n\n":
            "Impossibile aprire la cartella.\n\n",
        "Dossier des documents :\n":
            "Cartella dei documenti:\n",
        "↻ Documents synchronisés à {heure} : ":
            "↻ Documenti sincronizzati alle {heure}: ",
        "Depuis les documents :\n\n   • ":
            "Dai documenti:\n\n   • ",
        "Le document n'a pas pu être ouvert.\n\n":
            "Impossibile aprire il documento.\n\n",
        "Documents Word et texte":
            "Documenti Word e di testo",
        "Tous les fichiers":
            "Tutti i file",
        "Les documents eux-mêmes ne sont pas modifiés. Continuer ?":
            "I documenti stessi non vengono modificati. Continuare?",
        "{n} document ne ressemble ni à un mot de passe ni à un contact.":
            "{n} documento non sembra né una password né un contatto.",
        "{n} documents ne ressemblent ni à un mot de passe ni à un contact.":
            "{n} documenti non sembrano né una password né un contatto.",
        "Que contient ce document ?":
            "Cosa contiene questo documento?",
        "Longueur :":
            "Lunghezza:",
        "L'ancien mot de passe sera gardé dans les notes de la fiche.":
            "La vecchia password sarà conservata nelle note della scheda.",
        "caractères":
            "caratteri",
        "La copie du programme a échoué.":
            "La copia del programma non è riuscita.",
        "Mettre une icône « Pocket Book » sur le Bureau":
            "Metti un'icona «Pocket Book» sul Desktop",
        "Mettre à jour":
            "Aggiorna",
        "Installer":
            "Installa",
        "Installation en cours…":
            "Installazione in corso…",
        "Réessayer":
            "Riprova",
        "Le programme et ses icônes vont être retirés de cet ordinateur.\nVos fiches sont gardées, dans :":
            "Il programma e le sue icone saranno tolti da questo computer.\nLe vostre schede vengono conservate, in:",
        "Continuer ?":
            "Continuare?",
        "Fiches supprimées":
            "Schede eliminate",
        "fiche":
            "scheda",
        "Retirer « {champ} » de cette fiche ?\n\nCe qui est écrit dedans sera effacé :":
            "Togliere «{champ}» da questa scheda?\n\nCiò che vi è scritto sarà cancellato:",
        "Chercher un contact":
            "Cerca un contatto",
        "Chercher une fiche":
            "Cerca una scheda",
        "＋  Nouveau contact":
            "＋  Nuovo contatto",
        "＋  Nouvelle fiche":
            "＋  Nuova scheda",
        "\n\nAstuce : glissez des fichiers .docx ou .txt (ou tout un dossier)\ndepuis l'Explorateur sur cette fenêtre pour les ranger d'un coup.":
            "\n\nSuggerimento: trascinate file .docx o .txt (o un'intera cartella)\ndal gestore dei file su questa finestra per sistemarli tutti insieme.",
        "Lecture des documents : {i} sur {n}…":
            "Lettura dei documenti: {i} di {n}…",
        "… et {n} autres contacts":
            "… e altri {n} contatti",
        "Mettre à jour Pocket Book":
            "Aggiorna Pocket Book",
        "Installer Pocket Book":
            "Installa Pocket Book",
        "L'installation n'a pas pu se faire":
            "Non è stato possibile completare l'installazione",
        "Pocket Book est installé":
            "Pocket Book è installato",
        "Ce fichier d'installation peut maintenant être rangé ou supprimé.":
            "Questo file di installazione ora può essere messo via o eliminato.",
        "Toutes les fiches, les sauvegardes et les copies .txt de ce dossier seront effacées définitivement :":
            "Tutte le schede, i backup e le copie .txt di questa cartella saranno cancellati definitivamente:",
        "Ouvrir":
            "Apri",
        "Venu du document : ":
            "Dal documento: ",
        "Le carnet n'a pas reconnu ce document. Vous pouvez quand même créer une fiche : il vous demandera s'il s'agit d'un mot de passe ou d'un contact.":
            "Il quaderno non ha riconosciuto questo documento. Potete comunque creare una scheda: vi chiederà se si tratta di una password o di un contatto.",
        "• Cliquez sur un nom dans la liste à gauche,\n":
            "• Fate clic su un nome nell'elenco a sinistra,\n",
        "• ou sur « Nouveau contact » pour en créer un.":
            "• oppure su «Nuovo contatto» per crearne uno.",
        "• ou sur « Nouvelle fiche » pour en créer une.":
            "• oppure su «Nuova scheda» per crearne una.",
        "La lecture a échoué.":
            "La lettura non è riuscita.",
        "Les documents n'ont pas pu être lus.\n\n":
            "Non è stato possibile leggere i documenti.\n\n",
        "{n} contact  →  « Mes contacts »":
            "{n} contatto  →  «I miei contatti»",
        "{n} contacts  →  « Mes contacts »":
            "{n} contatti  →  «I miei contatti»",
        "Aucun contact n'est choisi.\n\n":
            "Nessun contatto selezionato.\n\n",
        "Aucune fiche n'est choisie.\n\n":
            "Nessuna scheda selezionata.\n\n",
        "{n} mot de passe  →  « Mes mots de passe »":
            "{n} password  →  «Le mie password»",
        "{n} mots de passe  →  « Mes mots de passe »":
            "{n} password  →  «Le mie password»",
        "Le carnet va ranger :":
            "Il quaderno sistemerà:",
        "Catégorie":
            "Categoria",
        "Identifiant":
            "Nome utente",
        "Adresse e-mail":
            "Indirizzo e-mail",
        "Portable":
            "Cellulare",
        "Téléphone fixe":
            "Telefono fisso",
        "Adresse":
            "Indirizzo",
        "Anniversaire":
            "Compleanno",
        "Contact":
            "Contatto",
        "?":
            "?",
        "un mot de passe":
            "una password",
        "un contact":
            "un contatto",
        "non reconnu":
            "non riconosciuto",
        "Bleu":
            "Blu",
        "Vert":
            "Verde",
        "Jaune":
            "Giallo",
        "Orange":
            "Arancione",
        "Rouge":
            "Rosso",
        "Violet":
            "Viola",
        "Rose":
            "Rosa",
        "Turquoise":
            "Turchese",
        "Gris":
            "Grigio",
        "Marron":
            "Marrone",
        "Banque":
            "Banca",
        "Administration":
            "Amministrazione",
        "Santé":
            "Salute",
        "Messagerie":
            "Posta",
        "Achats":
            "Acquisti",
        "Factures":
            "Bollette",
        "Loisirs":
            "Tempo libero",
        "Famille":
            "Famiglia",
        "Travail":
            "Lavoro",
        "Clair":
            "Chiaro",
        "Sombre":
            "Scuro",
        "Contraste fort":
            "Contrasto elevato",
        "Sépia doux":
            "Seppia tenue",
        "Autres":
            "Altro",
        "À propos":
            "Informazioni",
        "Pocket Book {version} — fonctionne entièrement sans internet : rien ne quitte cet ordinateur.":
            "Pocket Book {version} — funziona interamente senza internet: niente lascia questo computer.",
        "Vos données sont ici :":
            "I vostri dati sono qui:",
        "Ouvrir le dossier des données":
            "Apri la cartella dei dati",
        "Désinstaller…":
            "Disinstalla…",
    },
}
