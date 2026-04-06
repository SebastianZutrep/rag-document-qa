# 🤖 RAG AI - Document Question Answering System

A web application that allows users to upload PDF documents and ask questions about their content using a **RAG (Retrieval-Augmented Generation)** pipeline powered by AI.

---

## 🚀 Features

* 📄 Upload PDF documents
* 🧠 Automatic text processing and embeddings generation
* 🔍 Semantic search using ChromaDB
* 💬 Chat interface (ChatGPT-style)
* 🔐 User authentication (register & login)
* ⚡ FastAPI backend
* 🎨 Modern frontend with HTML, CSS, and JavaScript

---

## 🧱 Architecture

```
Frontend (HTML/CSS/JS)
        ↓
FastAPI Backend (Python)
        ↓
RAG Pipeline
        ↓
ChromaDB (Vector Store)
        ↓
AI Model (Gemini / embeddings)
```

---

## 📁 Project Structure

```
rag-document-qa/
│
├── frontend/
│   ├── index.html
│   ├── register.html
│   ├── chat.html
│   ├── styles.css
│   ├── auth.js
│   ├── chat.js
│
├── src/
│   ├── auth.py
│   ├── db.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── rag_pipeline.py
│   ├── text_splitter.py
│   ├── vector_store.py
│
├── data/
│   └── documents/   # (do NOT upload to GitHub)
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd rag-document-qa
```

---

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Environment variables

Create a `.env` file:

```env
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
GEMINI_API_KEY=your_api_key
```

---

## ▶️ Run the Application

### Backend (FastAPI)

```bash
uvicorn app:app --reload
```

Available at:

```
http://127.0.0.1:8000
```

---

### Frontend

```bash
cd frontend
python -m http.server 5500
```

Open in browser:

```
http://localhost:5500
```

---

## 🧪 Usage

1. Register an account
2. Log in
3. Upload a PDF document
4. Ask questions about the document

---

## 🧠 How RAG Works

1. Upload a PDF document
2. Split text into chunks
3. Generate embeddings
4. Store them in ChromaDB
5. When a question is asked:

   * Convert question into embedding
   * Retrieve relevant chunks
   * Generate a contextual answer

---

## ⚠️ Important Notes

Do NOT upload:

* `venv/`
* `.env`
* `data/documents/`
* `chroma/`

Make sure to correctly handle `user_id` to avoid mixing user data.

---

## 🛠 Tech Stack

* Python
* FastAPI
* ChromaDB
* Supabase
* HTML / CSS / JavaScript
* Gemini API (Google AI)

---

## 📈 Future Improvements

* Chat history
* Multi-document support
* Fully ChatGPT-like UI
* Cloud deployment
* Streaming responses

---

## 👨‍💻 Author

Sebastián Pertuz

---

## ⭐ Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📄 License

This project is licensed under the MIT License.

