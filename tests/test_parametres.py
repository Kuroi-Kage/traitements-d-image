from parametres.parametres_traitements import ParametresTraitement


def test_valeurs_par_defaut():
    params = ParametresTraitement()

    assert params.get_valeur("seuil_bas_contours") == 100
    assert params.get_valeur("seuil_haut_contours") == 200
    assert params.get_valeur("taille_noyau_filtre") == 3


def test_modifier_parametre():
    params = ParametresTraitement()

    params.set_valeur("taille_noyau_filtre", 15)

    assert params.get_valeur("taille_noyau_filtre") == 15


def test_parametre_inconnu():
    params = ParametresTraitement()

    try:
        params.set_valeur("inexistant", 50)
    except AttributeError:
        pass
    else:
        assert False
