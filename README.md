# Personal AI Assistant (RAG-based)

## Overview
A full-stack AI assistant that answers your questions using your personal data (Gmail, WhatsApp, Google Calendar) via Retrieval-Augmented Generation (RAG). The assistant ingests, embeds, and indexes your data, then uses an LLM (Groq, OpenAI, etc.) to answer questions with references.

---

## Features
- **Continuous ingestion** from Gmail, WhatsApp, and Google Calendar
- **Local embeddings** using open-source models
- **Vector search** for relevant context
- **RAG pipeline**: retrieves, augments, and generates answers
- **Role-based access** (simulate different user roles)
- **References** for every answer
- **Simple React chat UI**

---

## Tech Stack
- **Backend:** Python, FastAPI, ChromaDB, Sentence Transformers, Google API
- **Frontend:** React, Axios
- **LLM:** Groq API (Llama-3, Mixtral, etc.) or OpenAI (optional)

---

## Setup Instructions

### 1. Clone the Repo
```bash
git clone <your-repo-url>
cd personal-ai-assistant
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

- Place your `credentials.json` in `backend/app/` (from Google Cloud Console).
- Ensure `assistant.db` and `chroma_db/` are writable.

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm start
```

---

## Ingestion & Testing

### Gmail
```bash
curl -X POST "http://127.0.0.1:8000/ingest" -H "Content-Type: application/json" -d '{"source": "gmail"}'
```

### WhatsApp
- Place your exported chat as `backend/app/whatsapp_chat.txt`.
```bash
curl -X POST "http://127.0.0.1:8000/ingest" -H "Content-Type: application/json" -d '{"source": "whatsapp"}'
```

### Google Calendar
```bash
curl -X POST "http://127.0.0.1:8000/ingest" -H "Content-Type: application/json" -d '{"source": "calendar"}'
```

### Ask a Question
```bash
curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d '{"query": "What did I discuss with Alice?", "role": "me"}'
```

---

## Usage
- Open [http://localhost:3000](http://localhost:3000) in your browser.
- Select your role ("me", "teacher", etc.).
- Ask questions like:
  - "What did I discuss with Akki on WhatsApp?"
  - "Summarize my recent Gmail emails."
  - "What are my upcoming calendar events?"
- Answers include references to the source data.

---

## Workflow Diagram

```mermaid
graph TD
  subgraph Data Sources
    G[Gmail]
    W[WhatsApp]
    C[Google Calendar]
  end
  G --> I[Ingestion Layer]
  W --> I
  C --> I
  I --> E[Embeddings (Sentence Transformers)]
  E --> V[Vector DB (ChromaDB)]
  Q[User Query (Frontend)] --> RAG[RAG Pipeline (Backend)]
  V --> RAG
  RAG --> LLM[LLM (Groq/OpenAI)]
  LLM --> RAG
  RAG --> A[Answer + References]
  A --> Q
```

---

## Project Structure
```
personal-ai-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api.py
│   │   ├── rag.py
│   │   ├── db.py
│   │   ├── vector_store.py
│   │   ├── models.py
│   │   └── data_ingestion/
│   │       ├── base.py
│   │       ├── gmail_ingestor.py
│   │       ├── calendar_ingestor.py
│   │       └── whatsapp_imgestor.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── components/
│   │   │   ├── ChatWindow.js
│   │   │   ├── Message.js
│   │   │   └── RoleSelector.js
│   │   └── api/
│   │       └── api.js
│   ├── package.json
│   └── README.md
└── README.md
```

---

## Notes
- For production, restrict CORS and secure your API keys.
- You can add more data sources by creating new ingestors in `data_ingestion/`.
- The vector DB is persistent (see `vector_store.py`).
- For best results, ingest more data and use specific queries.

---

## License
MIT 