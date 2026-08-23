import cv2
import numpy as np

from traitements.traitements_image import (
    EgalisationHistogramme,
    Filtrage,
    DetectionContours,
    Binarisation,
    ConversionNiveauGris,
)
from parametres.parametres_traitements import ParametresTraitement


def test_egalisation_histogramme():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image[:] = [100, 150, 200]

    traitement = EgalisationHistogramme()
    params = ParametresTraitement()

    resultat = traitement.appliquer(image, params)

    assert resultat.shape == image.shape
    assert resultat.dtype == image.dtype


def test_filtrage():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image[40:60, 40:60] = 255

    traitement = Filtrage()
    params = ParametresTraitement()
    params.set_valeur("taille_noyau_filtre", 9)

    resultat = traitement.appliquer(image, params)

    assert resultat.shape == image.shape
    assert resultat.dtype == image.dtype
    assert not np.array_equal(resultat, image)


def test_filtrage_taille_paire():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image[40:60, 40:60] = 255

    traitement = Filtrage()
    params = ParametresTraitement()
    params.set_valeur("taille_noyau_filtre", 10)

    resultat = traitement.appliquer(image, params)

    assert resultat.shape == image.shape
    assert not np.array_equal(resultat, image)


def test_detection_contours():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.rectangle(image, (20, 20), (80, 80), (255, 255, 255), 2)

    traitement = DetectionContours()
    params = ParametresTraitement()

    resultat = traitement.appliquer(image, params)

    assert len(resultat.shape) == 2
    assert resultat.dtype == np.uint8
    assert np.count_nonzero(resultat) > 0


def test_binarisation():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image[50:, :] = 255

    traitement = Binarisation()
    params = ParametresTraitement()

    resultat = traitement.appliquer(image, params)

    assert len(resultat.shape) == 2
    assert resultat.dtype == np.uint8
    assert set(np.unique(resultat)).issubset({0, 255})


def test_conversion_niveau_gris():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image[:] = [100, 150, 200]

    traitement = ConversionNiveauGris()
    params = ParametresTraitement()

    resultat = traitement.appliquer(image, params)

    assert len(resultat.shape) == 2
    assert resultat.dtype == np.uint8
    assert resultat.shape == image.shape[:2]


def test_conversion_image_deja_grise():
    image = np.zeros((100, 100), dtype=np.uint8)

    traitement = ConversionNiveauGris()
    params = ParametresTraitement()

    resultat = traitement.appliquer(image, params)

    assert resultat is image



