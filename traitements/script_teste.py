
from traitements import Traitement


class testTraitement(Traitement):
    
    nom = "Mon traitement"
    
    def appliquer(self, image, params):
        return image
    
traitement = testTraitement()
print(traitement.nom)