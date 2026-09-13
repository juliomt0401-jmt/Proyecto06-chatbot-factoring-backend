import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

store = client.file_search_stores.create(
    config={
        "display_name": "factoring",
        "embedding_model": "models/gemini-embedding-2"
    }
)

if not store.name:
    raise RuntimeError("No se obtuvo el nombre del File Search Store")

operation = client.file_search_stores.upload_to_file_search_store(
    file="rag/Base_conocimiento_Factoring_RAG_Integrada.md",
    file_search_store_name=store.name,
    config={
        "display_name": "Base conocimiento Factoring"
    }
)

while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)

print("STORE CREADO:")
print(store.name)