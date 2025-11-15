import os
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv

# =====================================================
# 0) CHEMINS ROBUSTES (Adaptés au nouveau projet)
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

PARQUET_PATH = os.path.join(DATA_DIR, "base_juridique_finale.parquet")
FAISS_PATH = os.path.join(DATA_DIR, "faiss_index.bin")

print("📂 DATA_DIR =", DATA_DIR)
print("📄 Parquet =", PARQUET_PATH)
print("📄 FAISS =", FAISS_PATH)

# =====================================================
# 1) Charger parquet + FAISS
# =====================================================

df = pd.read_parquet(PARQUET_PATH)
index = faiss.read_index(FAISS_PATH)

print("📘 Base juridique chargée :", df.shape)
print("🔍 Index FAISS prêt :", index.ntotal, "articles\n")

# =====================================================
# 2) HuggingFace Encoder (Retriever)
# =====================================================

encoder = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

# =====================================================
# 3) GPT (GitHub Models)
# =====================================================

load_dotenv()  # charge .env à la racine du projet
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise ValueError("❌ ERREUR : GITHUB_TOKEN introuvable dans .env à la racine du projet.")

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=TOKEN
)

# =====================================================
# 4) Retrieve
# =====================================================

def retrieve(question, k=5):
    q_emb = encoder.encode([question]).astype("float32")
    D, I = index.search(q_emb, k)

    docs = df.iloc[I[0]]

    context = ""
    for _, row in docs.iterrows():
        context += f"[{row['type']} – {row['article_number']}] {row['text']}\n\n"

    return context, docs

# =====================================================
# 5) Generate with GPT
# =====================================================

def generate_answer(context, question):

    prompt = f"""
Tu es un assistant juridique tunisien.
Répond UNIQUEMENT à partir des articles ci-dessous.
Si le texte ne permet pas de répondre, répond : "Je ne sais pas".

Articles pertinents :
{context}

Question : {question}

Réponse :
""".strip()

    rep = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    return rep.choices[0].message.content

# =====================================================
# 6) Pipeline RAG complet
# =====================================================

def ask(question, k=5):
    context, docs = retrieve(question, k)
    answer = generate_answer(context, question)

    # ajouter les sources
    sources = "\n".join(
        f"- {row['type']} (Art {row['article_number']})"
        for _, row in docs.iterrows()
    )

    answer += f"\n\n---\n📚 Sources utilisées :\n{sources}"

    return answer

# =====================================================
# 7) Test direct
# =====================================================

if __name__ == "__main__":
    q = "Quels sont les droits garantis aux femmes en Tunisie ?"
    print(f"❓ Question : {q}\n")
    rep = ask(q)
    print("\n🧠 Réponse du chatbot :\n")
    print(rep)
