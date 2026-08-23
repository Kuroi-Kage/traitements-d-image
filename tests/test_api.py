import io

import cv2
import numpy as np

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def creer_image_test():
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    image[25:75, 25:75] = [255, 255, 255]

    succes, buffer = cv2.imencode(".png", image)

    assert succes

    return buffer.tobytes()


def test_importer_image():

    contenu = creer_image_test()

    reponse = client.post(
        "/api/images",
        files={
            "fichier": (
                "test.png",
                io.BytesIO(contenu),
                "image/png",
            )
        },
    )

    assert reponse.status_code == 200

    donnees = reponse.json()

    assert "session_id" in donnees
    assert "image" in donnees

    assert donnees["session_id"]
    assert donnees["image"]


def test_appliquer_traitement():

    contenu = creer_image_test()

    # 1. Importer l'image
    reponse_import = client.post(
        "/api/images",
        files={
            "fichier": (
                "test.png",
                io.BytesIO(contenu),
                "image/png",
            )
        },
    )

    assert reponse_import.status_code == 200

    session_id = reponse_import.json()["session_id"]

    # 2. Appliquer le traitement
    reponse_traitement = client.post(
        f"/api/images/{session_id}/traitements/niveau_de_gris"
    )

    assert reponse_traitement.status_code == 200

    donnees = reponse_traitement.json()

    assert "image" in donnees
    assert donnees["image"]
    
    
def test_annuler_traitement():

    contenu = creer_image_test()

    reponse_import = client.post(
        "/api/images",
        files={
            "fichier": (
                "test.png",
                io.BytesIO(contenu),
                "image/png",
            )
        },
    )

    assert reponse_import.status_code == 200

    session_id = reponse_import.json()["session_id"]

    reponse_traitement = client.post(
        f"/api/images/{session_id}/traitements/niveau_de_gris"
    )

    assert reponse_traitement.status_code == 200

    reponse_annulation = client.post(
        f"/api/images/{session_id}/annuler"
    )

    assert reponse_annulation.status_code == 200

    donnees = reponse_annulation.json()

    assert donnees["annule"] is True
    assert donnees["image"]
    
def test_histogramme():

    contenu = creer_image_test()

    reponse_import = client.post(
        "/api/images",
        files={
            "fichier": (
                "test.png",
                io.BytesIO(contenu),
                "image/png",
            )
        },
    )

    assert reponse_import.status_code == 200

    session_id = reponse_import.json()["session_id"]

    reponse = client.get(
        f"/api/images/{session_id}/histogramme"
    )

    assert reponse.status_code == 200

    donnees = reponse.json()

    assert "canaux" in donnees
    assert len(donnees["canaux"]) == 3

def test_configurer_parametre():

    contenu = creer_image_test()

    reponse_import = client.post(
        "/api/images",
        files={
            "fichier": (
                "test.png",
                io.BytesIO(contenu),
                "image/png",
            )
        },
    )

    assert reponse_import.status_code == 200

    session_id = reponse_import.json()["session_id"]

    reponse = client.post(
        f"/api/images/{session_id}/parametres",
        json={
            "cle": "taille_noyau_filtre",
            "valeur": 7,
        },
    )

    assert reponse.status_code == 200
    assert reponse.json()["ok"] is True

def test_exporter_image():

    contenu = creer_image_test()

    reponse_import = client.post(
        "/api/images",
        files={
            "fichier": (
                "test.png",
                io.BytesIO(contenu),
                "image/png",
            )
        },
    )

    assert reponse_import.status_code == 200

    session_id = reponse_import.json()["session_id"]

    reponse = client.get(
        f"/api/images/{session_id}/export"
    )

    assert reponse.status_code == 200
    assert reponse.headers["content-type"] == "image/png"
    assert reponse.content.startswith(b"\x89PNG")