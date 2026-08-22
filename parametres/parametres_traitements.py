class ParametresTraitement:
    """Centraliser les régles ajustable  depuis l'interface
    (menu 'Configurer les paramètres' du cas d'utilisation)"""
    
    def __init__(self):
        self.seuil_bas_contours = 100
        self.seuil_haut_contours = 200
        self.taille_noyau_filtre = 3
        self.seuil_binarisation = 127
        
    def get_valeur(self, cle, defaut=None):
        return getattr(self, cle, defaut)
    
    def set_valeur(self, cle, valeur):
        if not hasattr(self, cle):
            raise AttributeError(f'Paramètre inconnu : {cle}')
        setattr(self, cle, valeur)