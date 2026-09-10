""" Modele contenant l'état de l'image manipulée"""

import copy

class ImageModel:
    """
    Garde l'image originale, l'image courante et un histoorique
    permettant d'annuler les traitement appliqués
    """
    
    def __init__(self):
        self.image_originale = None
        self.image_courante = None
        self._historique = []
        self.calques = []
        
    def charger_image(self, image):
        """Définit une nouvelle image importée comme référence"""
        self.image_originale = image
        self.image_courante = image
        self._historique = []
        
    def sauvegarder_etat(self):
        """Empile l'etat courant avant d'applique un nouveau traitement """
        if self.image_courante is not None:
            self._historique.append(copy.deepcopy(self.image_courante))
            
    def annuler_traitement(self):
        """Restaure l'état précédant, si disponible
        """
        if self._historique:
            self.image_courante = self._historique.pop()
            return True
        return False
    
    def reinitialiser(self):
        """Revient à l'image original t vide  l'historique"""
        
        self.image_courante = self.image_originale
        self._historique = []
        
    def a_une_image(self):
        return self.image_courante is not None
    
    def ajouter_calque(self):
        from models.calque import Calque
        calque = Calque(self.image_courante.copy())
        self.calques.append(calque)
        return calque
    
    def supprimer_calque(self, calque_id):
        self.calques = [c for c in self.calques if c.id != calque_id]
        
    def obtenir_calque(self, calque_id):
        for c in self.calques:
            if c.id == calque_id:
                return c
        raise KeyError(f"Calque introuvable: {calque_id}")
    
    def fusionner_calques(self):
        from services.compositeur import composer
        if not self.calques:
            raise ValueError("Aucun calque à fusionner")
        hauteur, largeur = self.image_courante.shape[:2]
        self.sauvegarder_etat()
        self.image_courante = composer(self.calques, largeur, hauteur)
        self.calques = []
        return self.image_courante