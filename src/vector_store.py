import chromadb
from chromadb.config import Settings

# Persistent ChromaDB client
client = chromadb.Client(Settings(persist_directory="chroma_db"))

# Create or get collection
collection = client.get_or_create_collection(name="documents")

# =========================
# GUARDAR EMBEDDINGS
# =========================
def store_embeddings(chunks, embeddings, user_id):
    print(f"Guardando embeddings para user_id: {user_id}")
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        doc_id = f"{user_id}_{i}"
        collection.add(
            documents=[chunk],
            embeddings=[emb],
            ids=[doc_id],
            metadatas=[{"user_id": user_id}]
        )
        print(f"Chunk almacenado: {chunk[:50]}... | Embedding: {emb[:5]}... | ID: {doc_id}")

# =========================
# CONSULTAR EMBEDDINGS
# =========================
def query_embeddings(query_embedding, user_id, n_results=3):
    print(f"Consultando embeddings para user_id: {user_id}")
    print(f"Embedding de consulta: {query_embedding[:5]}...")

    # Query without user_id filter for debugging
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    # Debug raw results
    print(f"Resultados crudos de la consulta: {results}")

    # Handle empty results
    if not results or "documents" not in results or not results["documents"]:
        print("No se encontraron resultados para el user_id proporcionado.")
        return []

    print(f"Se encontraron {len(results['documents'][0])} documentos relevantes para user_id: {user_id}")
    return results["documents"][0]

# =========================
# DEBUG: QUERY SIN FILTRO
# =========================
def debug_query_all():
    print("Consultando todos los documentos sin filtro...")
    results = collection.query(
        query_embeddings=[[0] * 768],  # Dummy embedding
        n_results=10
    )
    print(f"Resultados sin filtro: {results}")