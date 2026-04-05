from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from src.rag_pipeline import ask_question, process_document

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

# =========================
# PREGUNTAR (FUNCIONA SEGURO)
# =========================
@app.post("/ask")
def ask(q: Query):
    answer, _ = ask_question(q.question, user_id="demo_user")
    return {"answer": answer}

# =========================
# SUBIR PDF (FUNCIONA SEGURO)
# =========================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        os.makedirs("data/documents", exist_ok=True)

        file_path = f"data/documents/{file.filename}"

        with open(file_path, "wb") as f:
            f.write(await file.read())

        process_document(file_path, user_id="demo_user")

        return {"message": "Documento procesado correctamente"}

    except Exception as e:
        return {"message": f"Error: {str(e)}"}