import json
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- Modelo de lenguaje ---
model_name_llm = "microsoft/Phi-2"
cache_dir = "./model_cache"

print("Cargando tokenizador y modelo de lenguaje...")
tokenizer = AutoTokenizer.from_pretrained(model_name_llm, cache_dir=cache_dir)
model_llm = AutoModelForCausalLM.from_pretrained(model_name_llm, cache_dir=cache_dir)


# --- Modelo de embeddings ---
print("Cargando modelo de embeddings...")
model_emb = SentenceTransformer("all-mpnet-base-v2")

print("¡Modelos listos!")

ruta_json = "documentos.json"   # Cambia por la ruta de tu archivo

with open(ruta_json, "r", encoding="utf-8") as f:
    datos = json.load(f)

# Extraemos los textos: si es un dict, tomamos los valores; si es lista, tomamos el campo "texto"
if isinstance(datos, dict):
    documentos = list(datos.values())
    ids = list(datos.keys())
else:
    # Suponemos que cada elemento tiene un campo "texto"
    documentos = [item["texto"] for item in datos]
    ids = [item.get("id", str(i)) for i, item in enumerate(datos)]

print(f"Se cargaron {len(documentos)} documentos.")
print("Algunos documentos:", documentos[0:5], "")