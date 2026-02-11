import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from qdrant_client import QdrantClient


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Nincs beallitva az OPENAI_API_KEY.")

qdrant_client = QdrantClient(url="http://localhost:7000")

EMBED_MODEL = "text-embedding-3-large"
GPT_MODEL = "gpt-5"
COLLECTION = "eszkoz_lista_text_embedding_3_large_all_columns"

embeddings = OpenAIEmbeddings(model=EMBED_MODEL, api_key=api_key)
chat_model = ChatOpenAI(model=GPT_MODEL, api_key=api_key)


@lru_cache(maxsize=128)
def get_embedding(text: str):
    return embeddings.embed_query(text)


def answer_question(question: str, top_k: int = 5) -> str:
    embedding = get_embedding(question)

    search_results = qdrant_client.query_points(
        collection_name=COLLECTION,
        query=embedding,
        limit=top_k,
        search_params={"hnsw_ef": 128},
    )

    context_chunks = []
    for hit in search_results.points:
        payload = hit.payload
        formatted = "\n".join(f"{k}: {v}" for k, v in payload.items())
        context_chunks.append(f"### Eszkoz\n{formatted}\n")

    context_text = "\n".join(context_chunks).strip() or "Nincs relevans adat."

    system_prompt = (
        "You are an inventory lookup assistant.\n"
        "You MUST answer ONLY using the information in the 'Relevant data' section.\n"
        "If the information is not present, reply exactly with:\n"
        '"Nincs talalat az adatbazisban."\n\n'
        "Do NOT invent objects, do NOT guess, do NOT recommend external sources.\n"
        "Stick strictly to the retrieved records."
    )

    user_prompt = f"Kerdes: {question}\n\nRelevant data:\n{context_text}"
    response = chat_model.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    )
    return response.content if isinstance(response.content, str) else str(response.content)
