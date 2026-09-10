from dotenv import load_dotenv
load_dotenv()

import json
import os

import google.generativeai as genai

NOMS_TRAITEMENTS_VALIDES = {
    "egalisation", "niveaux_de_gris", "binarisation", "filtrage", "contours" "rotation", "recadrage", "redimensionnement", "effacement", "amelioration"
}

PROMPT_SYSTEME = """Tu es un assistant qui traduit une demande de traitement
d'image en une liste d'actions précises. Les traitements disponibles sont
exactement : egalisation, niveaux_de_gris, binarisation, filtrage, contours.

Réponds UNIQUEMENT avec un tableau JSON, sans texte autour, au format :
[{"traitement": "filtrage", "parametres": {"taille_noyau_filtre": 5}}]

Les clés de paramètres possibles : seuil_binarisation, taille_noyau_filtre,
seuil_bas_contours, seuil_haut_contours. N'inclus une clé "parametres" que
si l'utilisateur donne une indication qui la justifie ; sinon, omets-la ou
laisse un objet vide.
"""


class Interpreteur:
    def __init__(self):
        cle_api = os.environ.get("GEMINI_API_KEY")
        if not cle_api:
            raise RuntimeError(
                "GEMINI_API_KEY n'est pas définie dans l'environnement"
            )
        genai.configure(api_key=cle_api)
        self.modele = genai.GenerativeModel("gemini-3.6-flash")

    def interpreter(self, instructions: str) -> list[dict]:
        """Retourne une liste d'étapes [{"traitement": ..., "parametres": {...}}]."""
        reponse = self.modele.generate_content(
            [PROMPT_SYSTEME, f"Demande de l'utilisateur : {instructions}"]
        )
        texte = reponse.text.strip()
        texte = texte.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        try:
            etapes = json.loads(texte)
        except json.JSONDecodeError as erreur:
            raise ValueError(f"Réponse du LLM non exploitable : {texte}") from erreur

        etapes_valides = [
            e for e in etapes
            if isinstance(e, dict) and e.get("traitement") in NOMS_TRAITEMENTS_VALIDES
        ]
        return etapes_valides