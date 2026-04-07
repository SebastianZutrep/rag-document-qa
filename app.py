from fastapi import FastAPI, HTTPException, Request, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from src.auth import signup, login
from src.rag_pipeline import ask_question, process_document
import os
import uuid
 
app = FastAPI()
 
origins = [
    "http://localhost:5500",
]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
@app.post("/register")
async def register(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email y contraseña son requeridos")
        response = signup(email, password)
        return {"message": "Usuario registrado exitosamente", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar usuario: {str(e)}")
 
@app.post("/login")
async def login_user(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email y contraseña son requeridos")
        response = login(email, password)
        session = response.session
        user = response.user
        if not session or not user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        print(f"Login exitoso para user_id: {user.id}")
        return {"access_token": session.access_token, "user_id": user.id}
    except Exception as e:
        print(f"Error en el login: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {str(e)}")
 
@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        question = data.get("question")
        user_id = data.get("user_id")
        if not question:
            raise HTTPException(status_code=400, detail="La pregunta es requerida.")
        if not user_id:
            raise HTTPException(status_code=400, detail="El user_id es requerido.")
        print(f"Recibiendo pregunta para user_id: {user_id}")
        answer, context = ask_question(question, user_id)
        return {"answer": answer, "context": context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la pregunta: {str(e)}")
 
@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    user_id: str = Form(...),
):
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="El user_id es requerido.")
 
        file_path = f"data/documents/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
 
        print(f"Archivo recibido: {file.filename}, user_id: {user_id}")
 
        document_id = str(uuid.uuid4())
        process_document(file_path, user_id, document_id)
 
        return {"message": "Documento procesado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir el documento: {str(e)}")
