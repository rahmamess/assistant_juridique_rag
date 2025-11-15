from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys, os

# Ajouter le backend au PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
sys.path.append(BACKEND_DIR)

from rag_engine import ask

# =====================================================
# INITIALISATION API
# =====================================================

app = FastAPI(
    title="Assistant Juridique RAG API",
    description="API pour poser des questions juridiques tunisiennes (Constitution + Statut Personnel)",
    version="1.0.0"
)

# =====================================================
# ACTIVER CORS pour le frontend Streamlit
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # en production tu mettras un domaine spécifique
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# ROUTES API
# =====================================================

@app.get("/")
def welcome():
    return {"message": "Bienvenue dans l'API RAG Juridique Tunisienne 🇹🇳"}

@app.get("/ask")
def ask_question(q: str):
    """
    Exemple:
    /ask?q=Quels%20sont%20les%20droits%20des%20femmes%20en%20Tunisie
    """
    try:
        answer = ask(q)
        return {"question": q, "answer": answer}
    except Exception as e:
        return {"error": str(e)}
