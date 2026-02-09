# backend/answer.py

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from openai import OpenAI

# ------------------------
# ENV betöltés
# ------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ Nincs beállítva az OPENAI_API_KEY!")

client_openai = OpenAI(api_key=api_key)

# ------------------------
# Qdrant beállítás
# ------------------------
qdrant_client = QdrantClient(url="http://localhost:7000")

EMBED_MODEL = "text-embedding-3-large"
GPT_MODEL = "gpt-5"
COLLECTION = "eszkoz_lista_text_embedding_3_large_all_columns"



# ------------------------
# VÁLASZFGV

def answer_question(question: str, top_k: int = 5) -> str:
    """
    RAG pipeline:
    1) Embedding
    2) Qdrant keresés
    3) Kontextus összeállítása
    4) GPT válasz generálása
    """

    # --- 1) Embedding ---
    embedding = client_openai.embeddings.create(
        model=EMBED_MODEL,
        input=question
    ).data[0].embedding

    # --- 2) Qdrant keresés  ---
    search_results = qdrant_client.query_points(
        collection_name=COLLECTION,
        query=embedding,
        limit=top_k,
        search_params={"hnsw_ef": 128}
    )

    # --- 3) Kontextus összeállítása ---
    context_chunks = []
    for hit in search_results.points:
        payload = hit.payload
        formatted = "\n".join(f"{k}: {v}" for k, v in payload.items())
        context_chunks.append(f"### Eszköz\n{formatted}\n")

    context_text = "\n".join(context_chunks)

    if not context_text.strip():
        context_text = "Nincs releváns adat."

    # --- 4) GPT válasz ---
    messages = [
        {
            "role": "system",
            "content": """
You are an inventory lookup assistant.
You MUST answer ONLY using the information in the 'Relevant data' section.
If the information is not present, reply exactly with:
"Nincs találat az adatbázisban."

Do NOT invent objects, do NOT guess, do NOT recommend external sources.
Stick strictly to the retrieved records.
            """
        },
        {
            "role": "user",
            "content": f"Kérdés: {question}\n\nRelevant data:\n{context_text}"
        }
    ]

    answer = client_openai.chat.completions.create(
        model=GPT_MODEL,
        messages=messages
    ).choices[0].message.content

    return answer

#%%
