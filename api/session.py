"""GÈRE LES SESSIONS D'EDITION D'IMAGE CÔTÉ SERVEUR"""

import uuid
from controllers.controller import ImageController

class Session:
    def __init__(self):
        self._sessions: dict[str, ImageController] = {}
        
    def creer_session(self) -> tuple[str, ImageController]:
        session_id = str(uuid.uuid4())
        controlleur = ImageController()
        self._sessions[session_id] = controlleur
        return session_id, controlleur
    
    def obtenir(self, session_id:str) -> ImageController:
        controleur = self._sessions.get(session_id)
        if controleur is None:
            raise KeyError(f"Session inconnue : {session_id}")
        return controleur
    
    def supprimer(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

session = Session()