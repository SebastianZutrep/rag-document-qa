import chromadb
 
# Cliente persistente (API moderna de ChromaDB)
client = chromadb.PersistentClient(path="chroma_db")
 
# Crear o recuperar la colección
collection = client.get_or_create_collection(name="documents")
 
# =========================
# LIMPIAR EMBEDDINGS DEL USUARIO
# =========================
def clear_user_embeddings(user_id):
    print(f"Limpiando embeddings para user_id: {user_id}")
    try:
        results = collection.get(where={"user_id": user_id})
        if results and results["ids"]:
            collection.delete(ids=results["ids"])
            print(f"Eliminados {len(results['ids'])} chunks anteriores.")
        else:
            print("No había embeddings previos.")
    except Exception as e:
        print(f"Error al limpiar embeddings: {e}")
 
# =========================
# VERIFICAR SI EL USUARIO TIENE DOCUMENTOS
# =========================
def user_has_documents(user_id):
    try:
        results = collection.get(where={"user_id": user_id})
        return bool(results and results["ids"])
    except Exception as e:
        print(f"Error verificando documentos: {e}")
        return False
 
# =========================
# GUARDAR EMBEDDINGS
# =========================
def store_embeddings(chunks, embeddings, user_id, document_id):
    print(f"Guardando {len(chunks)} chunks para user_id: {user_id}, document_id: {document_id}")
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        doc_id = f"{user_id}_{document_id}_{i}"
        collection.add(
            documents=[chunk],
            embeddings=[emb],
            ids=[doc_id],
            metadatas=[{"user_id": user_id, "document_id": document_id}]
        )
        print(f"Chunk almacenado ID: {doc_id}")
 
# =========================
# CONSULTAR EMBEDDINGS (filtrado por user_id)
# =========================
def query_embeddings(query_embedding, user_id, n_results=3):
    print(f"Consultando embeddings para user_id: {user_id}")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"user_id": user_id}
    )
    if not results or "documents" not in results or not results["documents"]:
        return []
    return results["documents"][0]
