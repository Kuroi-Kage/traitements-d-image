import cv2

class Histogramme:
    """Calcule des données d'histogramme
    """
    
    def calcule(self, image):
        """Retoune une liste d'histogrammes, (un par canal)
        Args:
            image (_type_): _description_
        """
        if len(image.shape) == 2:
            canaux = [0]
        else:
            canaux = range(image.shape[2])
            
        return [
            cv2.calcHist([image], [canal], None, [256], [0, 256]).flatten().tolist()
            for canal in canaux
        ]