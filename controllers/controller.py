import cv2

from models.model_stockage import ImageModel
from services.exporter import ImageExporter
from services.histogramme import Histogramme
from parametres.parametres_traitements import ParametresTraitement


class ImageController:
    def __init__(self):
        self.modele = ImageModel()
        self.parametre = ParametresTraitement()
        self.histogram = Histogramme()
        self.img_exporter = ImageExporter()
        
    def importer(self, chemin):
        """Charge une image depuis les disque"""
        image = cv2.imread(chemin)
        if image is None:
            raise IOError(f"Impossible de lire l'image : {chemin}")
        self.modele.charger_image(image)
        return image
    
    def applique_traitement(self, traitement):
        """"Applique un traitemnt (instance de traitement) à l'image courante"""
    
        if not self.modele.a_une_image():
            raise ValueError("Aucune image chargée")
        self.modele.sauvegarder_etat()
        resultat = traitement.appliquer(self.modele.image_courante, self.parametre)
        self.modele.image_courante = resultat
        return resultat
    
    def annuler_traitement(self):
        """Annuler le dernier traitement"""
        
        return self.modele.annuler_traitement()
    
    def calcule_histogramme(self):
        return self.histogram.calcule(self.modele.image_courante)
    
    def exporter(self, chemin):
        return self.img_exporter.exporter(self.modele.image_courante, chemin)
    
    def config_parametre(self, cle, valeur):
        self.parametre.set_valeur(cle, valeur)
        
        
