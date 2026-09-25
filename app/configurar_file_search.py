import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def crear_storage():
    store = client.file_search_stores.create(
        config={
            "display_name": "factoring",
            "embedding_model": "models/gemini-embedding-2"
        }
    )

    if not store.name:
        raise RuntimeError("No se obtuvo el nombre del File Search Store")

    operation = client.file_search_stores.upload_to_file_search_store(
        file="rag/7. Base_conocimiento_Factoring_RAG_Integrada_v1.md",
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

def modificar_storage():
    store_name = os.getenv("GEMINI_FILE_SEARCH_STORE")
    if not store_name:
        raise RuntimeError("No existe GEMINI_FILE_SEARCH_STORE en el archivo .env")

    # 1. Eliminar los documentos actuales del store
    for document in client.file_search_stores.documents.list(parent=store_name):
        document_name = document.name
        if not document_name:
            continue
        print("Eliminando:", document_name)
        client.file_search_stores.documents.delete(
            name=document_name,
            config={"force": True}
        )


    # 2. Subir la nueva base integrada
    operation = client.file_search_stores.upload_to_file_search_store(
        file="rag/7. Base_conocimiento_Factoring_RAG_Integrada_v3.md",
        file_search_store_name=store_name,
        config={
            "display_name": "Base conocimiento Factoring"
        }
    )


    # 3. Esperar la indexación
    while not operation.done:
        time.sleep(5)
        operation = client.operations.get(operation)


    print("BASE DE CONOCIMIENTO ACTUALIZADA")
    print("STORE:", store_name)

if __name__ == "__main__":
    modificar_storage()