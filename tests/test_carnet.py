"""Saving, backups, recovery from a damaged file, categories."""
import json

from pocket_book import Carnet


def nouveau_carnet(tmp_path):
    return Carnet(tmp_path / "pocketbook.json", tmp_path / "backups")


def test_enregistrer_et_recharger(tmp_path):
    carnet = nouveau_carnet(tmp_path)
    carnet.nouvelle_fiche(nom="Banque", mdp="secret")
    carnet.nouvelle_fiche(type="contact", nom="Josette", portable="06 12 34 56 78")
    carnet.enregistrer()
    relu = nouveau_carnet(tmp_path)
    relu.charger()
    assert [(f["type"], f["nom"]) for f in relu.fiches] == [("compte", "Banque"), ("contact", "Josette")]


def test_fichier_abime_reprend_la_derniere_sauvegarde(tmp_path):
    carnet = nouveau_carnet(tmp_path)
    carnet.nouvelle_fiche(nom="Gardée")
    carnet.enregistrer()
    carnet.sauvegarde_du_jour(force=True)
    (tmp_path / "pocketbook.json").write_text("{abîmé", encoding="utf-8")
    relu = nouveau_carnet(tmp_path)
    relu.charger()
    assert [f["nom"] for f in relu.fiches] == ["Gardée"]
    assert relu.message_recuperation
    assert list(tmp_path.glob("pocketbook_illisible_*.json"))


def test_ecriture_sans_fichier_a_moitie_ecrit(tmp_path):
    carnet = nouveau_carnet(tmp_path)
    carnet.nouvelle_fiche(nom="A")
    carnet.enregistrer()
    assert not list(tmp_path.glob("*.tmp"))
    assert json.loads((tmp_path / "pocketbook.json").read_text(encoding="utf-8"))["fiches"]


def test_renommer_et_supprimer_une_categorie(tmp_path):
    carnet = nouveau_carnet(tmp_path)
    fiche = carnet.nouvelle_fiche(nom="BNP", categorie="Banque")
    assert carnet.renommer_categorie("Banque", "Mes banques")
    assert fiche["categorie"] == "Mes banques"
    carnet.supprimer_categorie("Mes banques")
    assert fiche["categorie"] == "" and "Mes banques" not in carnet.noms_categories()


def test_fiche_supprimee_n_est_pas_recreee_par_la_synchro(tmp_path):
    carnet = nouveau_carnet(tmp_path)
    source = str(tmp_path / "Amazon.txt")
    fiche = carnet.nouvelle_fiche(nom="Amazon", source=source)
    carnet.supprimer(fiche["id"])
    documents = {source: {"nom": "Amazon", "texte": "a@b.fr\n\nmdp", "genre": "compte",
                          "mtime": 1.0, "erreur": ""}}
    resume = carnet.synchroniser_documents(documents, lambda propositions: propositions)
    assert resume["crees"] == 0 and not carnet.fiches
