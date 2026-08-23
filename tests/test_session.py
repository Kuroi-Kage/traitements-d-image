import pytest

from api.session import Session


def test_creer_session():
    manager = Session()

    session_id, controleur = manager.creer_session()

    assert session_id is not None
    assert controleur is not None
    assert session_id in manager._sessions


def test_obtenir_session():
    manager = Session()

    session_id, controleur = manager.creer_session()

    resultat = manager.obtenir(session_id)

    assert resultat is controleur


def test_session_inconnue():
    manager = Session()

    with pytest.raises(KeyError):
        manager.obtenir("session-inexistante")


def test_sessions_independantes():
    manager = Session()

    id1, controleur1 = manager.creer_session()
    id2, controleur2 = manager.creer_session()

    assert id1 != id2
    assert controleur1 is not controleur2


def test_supprimer_session():
    manager = Session()

    session_id, _ = manager.creer_session()

    manager.supprimer(session_id)

    assert session_id not in manager._sessions

    with pytest.raises(KeyError):
        manager.obtenir(session_id)
