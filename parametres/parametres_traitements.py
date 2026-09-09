class ParametresTraitement:
    """Centraliser les régles ajustable  depuis l'interface
    (menu 'Configurer les paramètres' du cas d'utilisation)"""
    
    def __init__(self):
        self.seuil_bas_contours = 100
        self.seuil_haut_contours = 200
        self.taille_noyau_filtre = 3
        self.seuil_binarisation = 127
        
        self.angle_rotation = 0
        self.nouvelle_largeur = None
        self.nouvelle_hauteur = None
        self.crop_x = 0
        self.crop_y = 0
        self.crop_largeur = None
        self.crop_hauteur = None
        
        self.luminosite = 0
        self.contraste = 0
        self.saturation = 0
        self.exposition = 0
        self.temperature = 0
        self.teinte = 0
        self.nettete = 0
        self.flou = 0
        
    def get_valeur(self, cle, defaut=None):
        return getattr(self, cle, defaut)
    
    def set_valeur(self, cle, valeur):
        if not hasattr(self, cle):
            raise AttributeError(f'Paramètre inconnu : {cle}')
        setattr(self, cle, valeur)