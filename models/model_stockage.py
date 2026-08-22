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