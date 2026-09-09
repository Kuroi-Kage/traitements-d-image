import cv2
from .traitements_image import EgalisationHistogramme

image = cv2.imread("img_teste/zenitsu-agatsuma-5120x2880-22696.png")



if image is None:
    print("Erreur: impossible de charge l'image")
    exit()
    
print("Image chargée:", image.shape)

traitement = EgalisationHistogramme()
print("classe EgalisationhISTOGRAMME CREEE")
print("Nom du traitement:", traitement.nom)

resultat = traitement.appliquer(image, {})
print("Méthode appliquer() executée")

if resultat is None:
    print("Le traitement retourne une image")
    exit()
    
hauteur_max = 700
largeur_max = 1000

def redimensionner_pour_affichage(image):
    hauteur, largeur = image.shape[:2]

    ratio = min(largeur_max / largeur, hauteur_max / hauteur)

    nouvelle_largeur = int(largeur * ratio)
    nouvelle_hauteur = int(hauteur * ratio)

    return cv2.resize(
        image,
        (nouvelle_largeur, nouvelle_hauteur),
        interpolation=cv2.INTER_AREA
    )


image_affichage = redimensionner_pour_affichage(image)
resultat_affichage = redimensionner_pour_affichage(resultat)

print("✅ Le traitement retourne une image")
print("Taille originale :", image.shape)
print("Taille résultat   :", resultat.shape)

cv2.imshow("Originale", image_affichage)
cv2.imshow("Egalisee", resultat_affichage)

cv2.waitKey(0)
cv2.destroyAllWindows()
