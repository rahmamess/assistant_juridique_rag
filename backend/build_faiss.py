import os
import numpy as np
import faiss
import pandas as pd
import pyarrow.parquet as pq

# =====================================================
# Détection automatique du chemin du projet
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

parquet_path = os.path.join(DATA_DIR, "base_juridique_finale.parquet")
index_path = os.path.join(DATA_DIR, "faiss_index.bin")

# =====================================================
# Charger le parquet
# =====================================================
print("📄 Lecture du fichier :", parquet_path)

df = pq.read_table(parquet_path).to_pandas()

embeddings = np.vstack(df["embedding"].to_list()).astype("float32")

# =====================================================
# Construire l'index FAISS
# =====================================================
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, index_path)

print("🎉 Index FAISS créé :", index_path)
print("📏 Dimension :", embeddings.shape[1])
print("📦 Nombre de vecteurs :", index.ntotal)
