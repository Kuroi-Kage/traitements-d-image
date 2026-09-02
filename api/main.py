import base64
import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.interpreteur import Interpreteur

from api.session import session
from traitements.traitements_image import (
    Binarisation, ConversionNiveauGris, DetectionContours, 
    EgalisationHistogramme, Filtrage,Rotation, Recadrage, Redimensionnement
)

app = FastAPI(title="API de traitement d'image")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "https://imatrixa.vercel.app",
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TRAITEMENTS = {
    "egalisation": EgalisationHistogramme,
    "niveaux_de_gris": ConversionNiveauGris,
    "binarisation": Binarisation,
    "filtrage": Filtrage,
    "contours": DetectionContours,
     "rotation": Rotation,
    "recadrage": Recadrage,
    "redimensionnement": Redimensionnement,
}

class ParametreRequete(BaseModel):
    cle: str
    valeur: int
    
class InstructionsRequete(BaseModel):
    instructions: str
    
def image_vers_base64(image: np.ndarray) -> str:
    succes, buffer = cv2.imencode(".png", image)
    if not succes:
        raise HTTPException(status_code=500, detail="Échec de l'encodage de l'image")
    return base64.b64encode(buffer).decode("utf-8")

@app.post("/api/images")
async def importer_image(fichier: UploadFile = File(...)):
    """Importer l'image"""
    contenu = await fichier.read()
    tableau = np.frombuffer(contenu, dtype=np.uint8)
    image = cv2.imdecode(tableau, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Fichier image invalide")
    
    session_id, controlleur = session.creer_session()
    controlleur.modele.charger_image(image)
    
    return {"session_id": session_id, "image": image_vers_base64(image)}

@app.post("/api/images/{session_id}/traitements/{nom_traitement}")
def applique_traitement(session_id: str, nom_traitement: str):
    classe_traitement = TRAITEMENTS.get(nom_traitement)
    if classe_traitement is None:
        raise HTTPException(status_code=404, detail=f"Traitement inconnu : {nom_traitement}")
    
    try:
        controlleur = session.obtenir(session_id)
        resultat = controlleur.applique_traitement(classe_traitement())
    except KeyError:
        raise HTTPException(status_code=404, detail="Session inconnue")
    except ValueError as erreur:
        raise HTTPException(status_code=400, detail=str(erreur))
    
    return {"image": image_vers_base64(resultat)}

@app.post("/api/images/{session_id}/instructions")
def appliquer_instructions(session_id: str, requete: InstructionsRequete):
    """Cas d'utilisation « Interpréter des instructions en langage naturel »."""
    try:
        controleur = session.obtenir(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session inconnue")

    try:
        interpreteur = Interpreteur()
        etapes = interpreteur.interpreter(requete.instructions)
    except Exception as erreur:
        raise HTTPException(status_code=502, detail=f"Erreur du service IA : {erreur}")
    
    if not etapes:
        raise HTTPException(
            status_code=422,
            detail="Aucun traitement reconnu dans cette instruction.",
        )

    labels_appliques = []
    try:
        for etape in etapes:
            nom = etape["traitement"]
            for cle, valeur in etape.get("parametres", {}).items():
                try:
                    controleur.config_parametre(cle, valeur)
                except AttributeError:
                    pass  

            classe_traitement = TRAITEMENTS[nom]
            controleur.applique_traitement(classe_traitement())
            labels_appliques.append(nom)
             
    except KeyError as erreur:
        raise HTTPException(status_code=422, detail=f"Traitement invalide proposé par l'IA : {erreur}")

    return {
        "image": image_vers_base64(controleur.modele.image_courante),
        "traitements_appliques": labels_appliques,
    }


@app.post("/api/images/{session_id}/annuler")
def annuler_traitement(session_id:str):
    try:
        controleur = session.obtenir(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session inconnue")
    
    annule = controleur.annuler_traitement()
    return {"annule": annule, "image": image_vers_base64(controleur.modele.image_courante)}

@app.get("/api/images/{session_id}/histogramme")
def obtenir_histogramme(session_id: str):
    try:
        controleur = session.obtenir(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session inconnue")
    
    return {"canaux": controleur.calcule_histogramme()}


@app.post("/api/images/{session_id}/parametres")
def config_parametre(session_id: str, requete: ParametreRequete):
    try:
        controleur = session.obtenir(session_id)
        controleur.config_parametre(requete.cle, requete.valeur)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session inconnue")
    except AttributeError as erreur:
        raise HTTPException(status_code=400, detail=str(erreur))
    
    return {"ok": True}


@app.get("/api/images/{session_id}/export")
def exporter_image(session_id: str):
    try:
        controleur = session.obtenir(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session inconnue")
    
    succes, buffer = cv2.imencode(".png", controleur.modele.image_courante)
    if not succes:
        raise HTTPException(status_code=500, detail="Échec de l'export")
    
    import io
    return StreamingResponse(
        io.BytesIO(buffer.tobytes()),
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=image_exportee.png"}
    )