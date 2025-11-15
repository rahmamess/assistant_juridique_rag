import os
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm

# Paths robustes
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Charger les fichiers
constitution = load_json("constitution.json")
statut_personnel = load_json("statut_personnel_simplifie.json")

df = pd.concat([
    pd.DataFrame(constitution),
    pd.DataFrame(statut_personnel)
], ignore_index=True)

print("📘 Base juridique fusionnée :", df.shape)

# Encoder HF
encoder = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

print("⚙️ Génération embeddings...")
embeddings = encoder.encode(df["text"].tolist(),
                            batch_size=16,
                            show_progress_bar=True)

df["embedding"] = embeddings.tolist()

# Sauvegarde parquet
out_path = os.path.join(DATA_DIR, "base_juridique_finale.parquet")
pq.write_table(pa.Table.from_pandas(df), out_path)

print("🎉 Parquet créé :", out_path)
