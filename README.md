# API de traitement d'image

Logiciel de traitement d'image pour des traitements classiques et
avancés, pilotable aussi en langage naturel via un LLM qui choisit et
enchaîne les traitements pertinents.

FastAPI + OpenCV. Pattern Strategy pour les traitements, sessions en mémoire.
Python 3.11+.

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "API_KEY=valeur_x_valeur" > .env
uvicorn api.main:app --reload
```

Docs interactives : `http://localhost:8000/docs`

## Tests

```bash
pytest -v
```

## Structure

```
api/            routes + gestion des sessions
controllers/    orchestration (traitements, historique, calques)
models/         état de l'image, calques
traitements/    classes de traitement (Strategy pattern)
services/       interprétation LLM, composition de calques
```

## Traitements

`egalisation`, `niveaux_de_gris`, `binarisation`, `filtrage`, `contours`,
`rotation`, `recadrage`, `redimensionnement`, `effacement`, `amelioration`

## Déploiement
