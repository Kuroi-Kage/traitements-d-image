import numpy as np

from models.model_stockage import ImageModel


def test_charger_image():
    modele = ImageModel()

    image = np.zeros((100, 100, 3), dtype=np.uint8)

    modele.charger_image(image)

    assert modele.a_une_image()
    assert modele.image_originale is image
    assert modele.image_courante is image


def test_annuler_traitement():
    modele = ImageModel()

    image_originale = np.zeros((100, 100, 3), dtype=np.uint8)
    image_modifiee = np.ones((100, 100, 3), dtype=np.uint8)

    modele.charger_image(image_originale)

    modele.sauvegarder_etat()
    modele.image_courante = image_modifiee

    assert modele.annuler_traitement()

    assert np.array_equal(
        modele.image_courante,
        image_originale
    )


def test_annuler_sans_historique():
    modele = ImageModel()

    assert not modele.annuler_traitement()


def test_reinitialiser():
    modele = ImageModel()

    image_originale = np.zeros((100, 100, 3), dtype=np.uint8)
    image_modifiee = np.ones((100, 100, 3), dtype=np.uint8)

    modele.charger_image(image_originale)

    modele.sauvegarder_etat()
    modele.image_courante = image_modifiee

    modele.reinitialiser()

    assert modele.image_courante is image_originale
    assert modele._historique == []


def test_aucune_image():
    modele = ImageModel()

    assert not modele.a_une_image()



