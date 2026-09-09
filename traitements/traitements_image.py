import cv2
import numpy as np
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
    
    
class Rotation(Traitement):
    nom = "Rotation"
    
    def appliquer(self, image, params):
        angle = params.get_valeur("angle_rotation", 0)
        hauteur, largeur = image.shape[:2]
        centre = (largeur // 2, hauteur // 2)
        matrice = cv2.getRotationMatrix2D(centre, angle, 1.0)
        return cv2.warpAffine(image, matrice, (largeur, hauteur))
    
class Redimensionnement(Traitement):
    nom = "Redimensionnement"
    
    def appliquer(self, image, params):
        largeur = params.get_valeur("nouvelle_largeur")
        hauteur = params.get_valeur("nouvelle_hauteur")
        if not largeur or not hauteur:
            raise ValueError("nouvelle_largeur et nouvelle_hauteur sont requis")
       
        return cv2.resize(image, (largeur, hauteur))
    
class Recadrage(Traitement):
    nom = "Recadrage"
    
    def appliquer(self, image, params):
        hauteur_image, largeur_image = image.shape[:2]
        x = params.get_valeur("crop_x", 0)
        y = params.get_valeur("crop_y", 0)
        largeur = params.get_valeur("crop_largeur") or largeur_image
        hauteur = params.get_valeur("crop_hauteur") or hauteur_image
        return image[y:y + hauteur, x:x + largeur]
    

class Effacement(Traitement):
    nom = "Effacement"
    
    def appliquer(self, image, params):
        x = params.get_valeur("crop_x", 0)
        y = params.get_valeur("crop_y",0)
        largeur = params.get_valeur("crop_largeur") or 0
        hauteur = params.get_valeur("crop_hauteur") or 0
        
        resultat = image.copy()
        resultat[y:y + hauteur, x:x + largeur] = 255
        return resultat
    
class Amelioration(Traitement):
    nom = "Amelioration"
    
    def appliquer(self, image, params):
        resultat = image.copy().astype(np.float32)
        
        temperature = params.get_valeur("temperature", 0)
        if temperature != 0:
            resultat[:, :, 2] = np.clip(resultat[:, :, 2] + temperature, 0, 255)
            resultat[:, :, 0] = np.clip(resultat[:, :, 0] - temperature, 0, 255)
         
         
         #luminosite   
        luminosite = params.get_valeur("luminosite", 0)
        contraste = params.get_valeur("contraste", 0)
        facteur_contraste = 1 + (contraste / 100)
        resultat = np.clip(resultat * facteur_contraste + luminosite, 0, 255)
       
        #exposition
        exposition = params.get_valeur("exposition", 0)
        if exposition != 0:
            resultat = np.clip(resultat *(1 + exposition/ 100), 0, 255)
            
        resultat = resultat.astype(np.uint8)
        
        #saturation
        saturation = params.get_valeur("saturation", 0)
        teinte = params.get_valeur("teinte", 0)
        if saturation != 0 or teinte != 0:
            hsv = cv2.cvtColor(resultat, cv2.COLOR_BGR2HSV).astype(np.float32)
            if teinte != 0:
                hsv[:, :, 0] = (hsv[:, :, 0] + teinte / 2 ) % 180
            if saturation != 0:
                hsv[:, :, 1] = np.clip(hsv[:, :, 1] * (1 + saturation / 100), 0, 255)
            resultat = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
            
        #  Nettete
        nettete = params.get_valeur("nettete", 0)
        if nettete > 0:
            flou_gaussien = cv2.GaussianBlur(resultat, (0, 0), 3)
            resultat = cv2.addWeighted(
                resultat, 1 + nettete / 100, flou_gaussien, -(nettete / 100), 0
            )
            
        # Flou
        flou = params.get_valeur("flou", 0)
        if flou > 0:
            taille = flou if flou % 2 == 1 else flou + 1
            resultat = cv2.GaussianBlur(resultat, (taille, taille), 0)
            
        return resultat

    
    