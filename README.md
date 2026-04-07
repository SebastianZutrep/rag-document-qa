# 🤖 RAG AI - Document Question Answering System
A web application that allows users to upload documents and ask questions about their content using a **RAG (Retrieval-Augmented Generation)** pipeline powered by AI.

---

## 🚀 Features
* 📄 Upload documents (PDF, Word, Excel, CSV, Images)
* 🧠 Automatic text processing and embeddings generation
* 🔍 Semantic search using ChromaDB
* 👁️ OCR support for scanned documents and images
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
│   └── app.js
│
├── src/
│   ├── auth.py
│   ├── auth_middleware.py
│   ├── db.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── rag_pipeline.py
│   ├── text_splitter.py
│   └── vector_store.py
│
├── data/
│   └── documents/   # (do NOT upload to GitHub)
│
├── app.py
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

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR (required for image/scanned document support)
**Windows:** Download and install from https://github.com/UB-Mannheim/tesseract/wiki
Install to the default path: `C:\Program Files\Tesseract-OCR\`

**Mac:**
```bash
brew install tesseract
```
**Linux:**
```bash
sudo apt install tesseract-ocr
```

### 5. Environment variables
Create a `.env` file:
```env
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
GOOGLE_API_KEY=your_api_key
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
3. Upload a document
4. Ask questions about the document

---

## 📂 Supported File Formats
| Format | Extension | OCR Support |
|--------|-----------|-------------|
| PDF | `.pdf` | ✅ (text + scanned) |
| Word | `.docx`, `.doc` | ✅ (text + embedded images) |
| Excel | `.xlsx`, `.xls` | ❌ |
| CSV | `.csv` | ❌ |
| Images | `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`, `.webp` | ✅ |

---

## 🧠 How RAG Works
1. Upload a document
2. Extract text (with OCR if needed)
3. Split text into chunks
4. Generate embeddings
5. Store them in ChromaDB
6. When a question is asked:
   * Convert question into embedding
   * Retrieve relevant chunks filtered by user
   * Generate a contextual answer

---

## ⚠️ Important Notes
Do NOT upload:
* `venv/`
* `.env`
* `data/documents/`
* `chroma_db/`

Each user's documents are isolated — uploading a new document replaces the previous one for that user.

---

## 🛠 Tech Stack
* Python
* FastAPI
* ChromaDB
* Supabase
* HTML / CSS / JavaScript
* Gemini API (Google AI)
* Tesseract OCR
* PyMuPDF, python-docx, openpyxl

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
