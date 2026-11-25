"""Copie .txt de chaque fiche : création, mise à jour, renommage, corbeille."""
from pocket_book import Carnet, nom_de_fichier


def carnet_avec_copie(tmp_path):
    carnet = Carnet(tmp_path / "pocketbook.json", tmp_path / "backups")
    carnet.reglages["dossier_txt"] = str(tmp_path / "copie")
    return carnet


def fichiers(tmp_path):
    return sorted(p.relative_to(tmp_path / "copie").as_posix() for p in (tmp_path / "copie").rglob("*.txt"))


def test_creation_mise_a_jour_renommage(tmp_path):
    carnet = carnet_avec_copie(tmp_path)
    fiche = carnet.nouvelle_fiche(nom="Amazon", mdp="un")
    assert carnet.synchroniser_txt()
    assert fichiers(tmp_path) == ["Mots de passe/Amazon.txt"]
    fiche["mdp"] = "deux"
    carnet.synchroniser_txt()
    assert "deux" in (tmp_path / "copie/Mots de passe/Amazon.txt").read_text(encoding="utf-8-sig")
    fiche["nom"] = "Amazon Prime"
    carnet.synchroniser_txt()
    assert fichiers(tmp_path) == ["Mots de passe/Amazon Prime.txt"]


def test_fiche_supprimee_va_dans_la_corbeille(tmp_path):
    carnet = carnet_avec_copie(tmp_path)
    fiche = carnet.nouvelle_fiche(type="contact", nom="Josette")
    carnet.synchroniser_txt()
    carnet.supprimer(fiche["id"])
    carnet.synchroniser_txt()
    assert fichiers(tmp_path) == ["Fiches supprimées/Josette.txt"]


def test_ne_jamais_ecraser_un_fichier_existant(tmp_path):
    carnet = carnet_avec_copie(tmp_path)
    perso = tmp_path / "copie/Mots de passe/Netflix.txt"
    perso.parent.mkdir(parents=True)
    perso.write_text("mon fichier", encoding="utf-8")
    carnet.nouvelle_fiche(nom="Netflix")
    carnet.synchroniser_txt()
    assert perso.read_text(encoding="utf-8") == "mon fichier"
    assert "Mots de passe/Netflix (2).txt" in fichiers(tmp_path)


def test_noms_de_fichiers_valides_sous_windows():
    assert nom_de_fichier('Josette / Durand?') == "Josette - Durand-"
    assert nom_de_fichier("CON") == "CON (fiche)"
    assert nom_de_fichier("") == "Sans nom"
