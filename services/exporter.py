import cv2

class ImageExporter:
    """Sauvegarde une image sur disque
    """
    
    def exporter(self, image, chemin):
        succes = cv2.imwrite(chemin, image)
        if not succes:
            raise IOError(F"Échec de l'ixport vers {chemin}")
        return chemin