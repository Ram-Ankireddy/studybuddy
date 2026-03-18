# 📄 StudyBuddy — AI Document Q&A App

> Got bored reading lengthy documents? Want to directly find the info needed?

StudyBuddy lets you upload any PDF and instantly ask questions about it. No more scrolling through pages — just ask and get answers grounded in your document.

## 🚀 Live Demo
[Try it here](https://studybuddy-mnpwe6jranznzt5xzp8dxg.streamlit.app/)

![StudyBuddy Screenshot](https://github.com/user-attachments/assets/7114befd-b322-4d21-8fe4-2bbe05080433)

## 🧠 How It Works
1. Upload a PDF document
2. The app chunks the text and creates vector embeddings
3. Your question is matched against the most relevant chunks
4. A language model generates an answer based only on your document

This architecture is called **RAG (Retrieval-Augmented Generation)** — the same approach used in production AI systems like enterprise search and document intelligence tools.

## 🛠️ Tech Stack
| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Embeddings | Google Gemini (`gemini-embedding-001`) |
| Vector Store | ChromaDB (local) |
| LLM | Groq (`llama-3.1-8b-instant`) |
| PDF Processing | PyMuPDF |
| Orchestration | LangChain |

## ✨ Features
- Upload any PDF and start asking questions immediately
- Answers are grounded strictly in your document — no hallucination from outside knowledge
- Chat history maintained within session
- Automatically clears previous document on new upload
- Fast responses via Groq's free inference API

## ⚙️ Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Ram-Ankireddy/studybuddy.git
cd studybuddy
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

**5. Run the app**
```bash
streamlit run app.py
```

## 📌 Known Limitations
- Best suited for conceptual and analytical questions
- Very short metadata (titles, author names) may not retrieve accurately
- Summaries are based on retrieved chunks, not the full document
- Uploaded documents are not persisted between sessions

## 🔮 Planned Improvements
- Multi-document support with source attribution
- Persistent vector storage across sessions
- FastAPI backend for REST API access
- Document summarization mode

## 👤 Author
Built by Ram Ankireddy — Master's student in Computer Science
