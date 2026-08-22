import cv2
from traitements.traitements import Traitement

class EgalisationHistogramme(Traitement):
    nom = "Égaliser l'histogramme"
    
    def appliquer(self, image, params):
        if len(image.shape) == 3:
            ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
            return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
        return cv2.equalizeHist(image)
    
class Filtrage(Traitement):
    nom = "Filtrer /débruiter"
    
    def appliquer(self, image, params):
        taille = params.get_valeur("taille_noyau_filtre", 3)
        taille = taille if taille % 2 == 1 else taille + 1 
        return cv2.GaussianBlur(image, (taille, taille), 0)
    
    
class DetectionContours(Traitement):
    nom = "Détecter les contours"
        
    def appliquer(self, image, params):
        gris = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        bas = params.get_valeur("seuil_bas_contours", 100)
        haut = params.get_valeur("seuil_haut_contours", 200)
        return cv2.Canny(gris, bas, haut)
    
class Binarisation(Traitement):
    nom = "Binariser (seuillage)"
    
    def appliquer(self, image, params):
        gris = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        seuil = params.get_valeur("seuil_binarisation", 127)
        _, resultat = cv2.threshold(gris, seuil, 255, cv2.THRESH_BINARY)
        return resultat
    
class ConversionNiveauGris(Traitement):
    nom = "Convertir en niveau de gris"
    
    def appliquer(self, image, params):
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    