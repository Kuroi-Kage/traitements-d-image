import numpy as np

from services.histogramme import Histogramme


def test_histogramme_image_couleur():
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    generateur = Histogramme()

    histogrammes = generateur.calcule(image)

    assert len(histogrammes) == 3

    for histogramme in histogrammes:
        assert len(histogramme) == 256


def test_histogramme_image_grise():
    image = np.zeros((100, 100), dtype=np.uint8)

    generateur = Histogramme()

    histogrammes = generateur.calcule(image)

    assert len(histogrammes) == 1
    assert len(histogrammes[0]) == 256


def test_histogramme_total_pixels():
    image = np.zeros((100, 100), dtype=np.uint8)

    generateur = Histogramme()

    histogrammes = generateur.calcule(image)

    assert sum(histogrammes[0]) == 10000
