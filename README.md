# AI Customer Support Chatbot

Production-ready full-stack customer support chatbot with FastAPI, React, PostgreSQL, JWT auth, LangChain RAG, Hugging Face embeddings, optional ChromaDB/JSON vector persistence, and either Gemini API or a local Hugging Face language model.

This project intentionally does not use Ollama or Docker. For answer generation, set `GEMINI_API_KEY` to use Gemini API, or configure `LOCAL_LLM_MODEL` with a local model path/model already cached on the machine.

## Features

- Signup, login, JWT access tokens, refresh tokens, logout, and role-based access control.
- User chat with document-grounded RAG answers only.
- PDF, DOCX, and TXT uploads with background ingestion.
- Persistent vector store with ChromaDB when installed, or a JSON fallback for local Windows development.
- PostgreSQL metadata, users, sessions, chats, messages, documents, and feedback.
- Admin dashboard, users, documents, knowledge-base upload, and analytics.
- Structured logs, global exception handling, CORS, validation, and rate limiting.
- React frontend with protected routes, chat UI, document management, profile, history, and admin dashboard.

## Project Structure

```text
backend/
  alembic/                  Database migrations
  app/
    config/                 Environment settings
    controllers/            HTTP orchestration layer
    database/               SQLAlchemy async engine/session
    embeddings/             Hugging Face sentence-transformer embeddings
    middleware/             Auth, CORS, errors, rate limiting
    models/                 SQLAlchemy ORM models
    prompts/                RAG system prompts
    repositories/           Data access layer
    routers/                FastAPI route modules
    schemas/                Pydantic request/response models
    services/               Business logic, RAG, documents, auth
    utils/                  Security, logging, validators, helpers
    vectorstore/            Vector store adapter and retriever
frontend/
  src/
    api/                    Axios API client
    components/             Auth, chat, layout, common UI
    context/                Auth state
    hooks/                  Reusable React hooks
    pages/                  App pages
```

## Backend Setup

```powershell
cd "D:\AI Customer Support Chatbot\backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend\.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/chatbot_db
JWT_SECRET_KEY=change-this-long-random-secret
AI_PROVIDER=auto
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash
LOCAL_LLM_MODEL=C:\models\flan-t5-base
TRANSFORMERS_OFFLINE=True
```

Create the PostgreSQL database manually, then run migrations:

```powershell
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs are available at `http://localhost:8000/docs`.

## AI Provider

No Ollama is required. For Gemini, set:

```env
AI_PROVIDER=auto
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash
```

If `GEMINI_API_KEY` is blank, the backend falls back to the local Hugging Face LLM. The backend still uses:

- `EMBEDDING_MODEL` for sentence-transformer embeddings.
- `LOCAL_LLM_MODEL` for local answer generation.
- `CHROMA_PERSIST_DIR` for local vector persistence.

For fully offline mode, download/cache the embedding model and LLM before running the backend, or point both settings to local directories.

## Frontend Setup

```powershell
cd "D:\AI Customer Support Chatbot\frontend"
npm install
Copy-Item .env.example .env
npm run dev
```

Open `http://localhost:5173`.

## Core API Endpoints

- `POST /api/v1/signup`
- `POST /api/v1/login`
- `POST /api/v1/logout`
- `GET /api/v1/profile`
- `POST /api/v1/upload`
- `POST /api/v1/chat`
- `GET /api/v1/history`
- `DELETE /api/v1/delete-history`
- `POST /api/v1/feedback`
- `GET /api/v1/admin/users`
- `GET /api/v1/admin/documents`
- `GET /api/v1/admin/dashboard`

Namespaced endpoints such as `/api/v1/auth/login` and `/api/v1/documents/upload` are also available for frontend compatibility.

## Testing

```powershell
cd "D:\AI Customer Support Chatbot\backend"
pytest

cd "D:\AI Customer Support Chatbot\frontend"
npm run build
```
