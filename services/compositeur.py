import cv2
import numpy as np

def _appliquer_mode_fusion(base, calque_image, mode):
    base_f = base.astype(np.float32)
    calque_f = calque_image.astype(np.float32)
    
    
    if mode == "multiplier":
        return (base_f * calque_f) / 255.0
    if mode == "ecran":
        return 255.0 - ((255.0 - base_f) * (255.0 - calque_f)) / 255.0
    if mode == "supeposition":
        resultat = np.where(
            base_f < 128,
            (2 * base_f * calque_f) / 255.0,
            255.0 - (2 * (255.0- base_f) * (255.0 - calque_f)) / 255.0
        )
        return resultat
    return calque_f

def composer(calques, largeur, hauteur):
    # Fusionne les calque visible du bas vers le haut
    resultat = np.full((hauteur, largeur, 3), 255, dtype=np.float32)
    
    for calque in calques:
        if not calque.visible:
            continue
        
        image_redimensionnee = cv2.resize(calque.image, (largeur, hauteur)).astype(np.float32)
        fusionne = _appliquer_mode_fusion(resultat, image_redimensionnee, calque.mode_fusion)
        
        alpha = calque.opacite / 100
        resultat = resultat * (1 - alpha) + fusionne * alpha
        
    return np.clip(resultat, 0, 255).astype(np.uint8)
        