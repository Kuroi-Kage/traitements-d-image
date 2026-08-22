from abc import ABC, abstractmethod

class Traitement(ABC):
    """Classe de base abstraite pour tous les  traitements d'image."""
    
    nom = "Traitement"
    
    @abstractmethod
    def appliquer(self, image, params):
        """Applique le traitement à `image` et retourne la nouvelle image.
        
        :param image: image au format numpy array (OpenCV, BGR ou gris)
        :param params: instance de ParametresTraitement
        :return: nouvelle image traitée
        """
        raise NotImplemented