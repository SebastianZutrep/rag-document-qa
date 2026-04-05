import os
from dotenv import load_dotenv
from google import genai

from src.document_loader import load_pdf
from src.text_splitter import split_text
from src.embeddings import get_embeddings
from src.vector_store import store_embeddings, query_embeddings

# =========================
# CARGA DE VARIABLES
# =========================
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("No se encontró GOOGLE_API_KEY en el archivo .env")

client = genai.Client(api_key=api_key)

# =========================
# PROCESAR DOCUMENTO
# =========================
def process_document(file_path, user_id):
    try:
        if not user_id:
            raise ValueError("El user_id es requerido para procesar el documento.")

        # 1. Leer PDF
        text = load_pdf(file_path)

        # 2. Dividir en chunks
        chunks = split_text(text)

        if not chunks:
            raise ValueError("No se generaron chunks del documento.")

        # 3. Crear embeddings
        embeddings = get_embeddings(chunks)

        if not embeddings or len(embeddings) != len(chunks):
            raise ValueError("Error generando embeddings.")

        print(f"Embeddings generados: {len(embeddings)} para user_id: {user_id}")
        for i, emb in enumerate(embeddings):
            print(f"Embedding {i}: {emb[:5]}...")

        # 4. Guardar en vector DB
        print(f"Guardando {len(chunks)} chunks para user_id: {user_id}")
        store_embeddings(chunks, embeddings, user_id)

        return True

    except Exception as e:
        raise RuntimeError(f"Error en process_document: {e}")


# =========================
# GENERAR RESPUESTA (LLM)
# =========================
def generate_answer(context, question):

    prompt = f"""
Eres un asistente experto en análisis de documentos.

Instrucciones:
- Responde usando SOLO la información del contexto proporcionado.
- Integra la información de todos los fragmentos relevantes.
- No inventes información.
- Si la respuesta no está en el contexto, responde exactamente: "No se encontró información suficiente en el documento".
- Evita copiar texto literal; parafrasea y sintetiza.
- Si la información es insuficiente, indícalo claramente.
- Prioriza precisión sobre creatividad.
- Responde de forma clara, coherente y en español.

Contexto:
{context}

Pregunta:
{question}

Respuesta:
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            return "No se pudo generar una respuesta."

        return response.text.strip()

    except Exception as e:
        return f"Error generando respuesta: {e}"


# =========================
# PREGUNTAR AL SISTEMA
# =========================
def ask_question(question, user_id, top_k=3):
    try:
        if not user_id:
            raise ValueError("El user_id es requerido para realizar preguntas.")

        # 1. Embedding de la pregunta
        query_embedding = get_embeddings([question])[0]
        print(f"Embedding de la pregunta generado: {query_embedding[:5]}...")

        # 2. Buscar chunks relevantes
        relevant_chunks = query_embeddings(query_embedding, user_id, top_k)

        print(f"Se encontraron {len(relevant_chunks)} chunks para user_id: {user_id}")

        if not relevant_chunks:
            return "No se encontró información relevante en el documento.", []

        # 4. Limitar contexto
        context_chunks = relevant_chunks[:top_k]

        # 5. Construir contexto
        context = "\n\n".join(context_chunks)

        # 6. Generar respuesta
        answer = generate_answer(context, question)

        return answer, context_chunks

    except Exception as e:
        return f"Error en el sistema RAG: {e}", []