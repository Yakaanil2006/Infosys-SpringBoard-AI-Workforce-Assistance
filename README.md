# AI Workforce Assistant — Deployment & Setup Guide

A full-stack AI Workforce Assistant platform built with **Streamlit, FastAPI, Neon PostgreSQL, pgvector, Groq, JWT authentication, and RAG**.

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      Streamlit       │
                         │      Frontend        │
                         └──────────┬───────────┘
                                    │
                              REST + JWT
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       Backend        │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
   │ Neon PostgreSQL  │   │ Embedding Model  │   │    Groq LLM      │
   │                  │   │                  │   │                  │
   │ users            │   │ all-MiniLM-L6-v2 │   │ GPT-OSS 120B     │
   │ documents        │   │ 384 dimensions   │   │                  │
   │ recommendations  │   │                  │   │ RAG Generation   │
   │ chats            │   └──────────────────┘   └──────────────────┘
   │ datasets         │
   │ dataset_rows     │
   │ pgvector         │
   └──────────────────┘
```

---

# 🚀 1. Clone the Repository

```powershell
git clone https://github.com/Yakaanil2006/AI-Workforce-Assistant-Platform.git
cd AI-Workforce-Assistant-Platform
```

If you are using the project ZIP:

1. Extract the ZIP.
2. Open PowerShell inside the extracted project folder.

---

# 🗄️ 2. Setup Neon PostgreSQL

Create a PostgreSQL database using Neon.

Copy the Neon database connection string.

The project uses **psycopg 3**, so the connection string should use:

```text
postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require
```

Example:

```text
postgresql+psycopg://USER:PASSWORD@HOST/neondb?sslmode=require
```

## Enable pgvector

Open the Neon SQL Editor and execute:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

# ⚙️ 3. Backend Setup

Open PowerShell:

```powershell
cd backend
```

## Create virtual environment

```powershell
python -m venv .venv
```

## Activate virtual environment

```powershell
.venv\Scripts\activate
```

## Upgrade pip

```powershell
python -m pip install --upgrade pip
```

## Install dependencies

```powershell
pip install -r requirements.txt
```

## Create environment file

```powershell
copy .env.example .env
```

---

# 🔐 4. Configure Backend `.env`

Open:

```text
backend/.env
```

Add your actual credentials:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require

GROQ_API_KEY=YOUR_GROQ_API_KEY
GROQ_MODEL=openai/gpt-oss-120b

JWT_SECRET_KEY=YOUR_LONG_RANDOM_SECRET
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
TOP_K=5

CORS_ORIGINS=http://localhost:8501

POWERBI_EMBED_URL=

HF_API_KEY=YOUR_HUGGINGFACE_API_KEY
```

> **Important:** Never commit `backend/.env` to GitHub.

---

# 🔒 5. Protect Environment Variables

Your `.gitignore` should contain:

```gitignore
.env
*.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
.streamlit/secrets.toml
```

Your GitHub repository should contain:

```text
backend/.env.example
```

but **not**:

```text
backend/.env
```

The `.env.example` file should contain placeholders:

```env
DATABASE_URL=your_database_url
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
JWT_SECRET_KEY=your_long_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
TOP_K=5
CORS_ORIGINS=http://localhost:8501
POWERBI_EMBED_URL=
HF_API_KEY=your_huggingface_api_key
```

---

# 🗃️ 6. Run Database Migrations

From the `backend` directory:

```powershell
alembic upgrade head
```

Check the current migration:

```powershell
alembic current
```

The database should now contain the required tables and pgvector schema.

---

# 👤 7. Create Admin User

Run:

```powershell
python scripts/create_admin.py
```

Follow the prompts to create the first administrator account.

---

# 🧪 8. Test Groq API

Before starting the complete application, verify that your Groq API key can access the selected model.

Run:

```powershell
python -c "from groq import Groq; import os; c=Groq(api_key=os.getenv('GROQ_API_KEY')); print([m.id for m in c.models.list().data if m.active])"
```

Make sure your selected model appears:

```text
openai/gpt-oss-120b
```

Test the model directly:

```powershell
python -c "from groq import Groq; import os; c=Groq(api_key=os.getenv('GROQ_API_KEY')); r=c.chat.completions.create(model='openai/gpt-oss-120b',messages=[{'role':'user','content':'Say hello'}]); print(r.choices[0].message.content)"
```

If successful, Groq is ready.

---

# 🖥️ 9. Start FastAPI Backend

From the `backend` directory:

```powershell
uvicorn app.main:app --reload --port 8000
```

The backend runs at:

```text
http://127.0.0.1:8000
```

## Health Check

Open:

```text
http://127.0.0.1:8000/health
```

## Swagger API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

You should see:

```text
Application startup complete.
```

---

# 🔑 10. Test Authentication

Use the frontend or Swagger UI.

Test:

```text
POST /api/auth/login
```

Then:

```text
GET /api/auth/me
```

Expected result:

```text
POST /api/auth/login    → 200 OK
GET  /api/auth/me       → 200 OK
```

---

# 🧠 11. Test RAG Pipeline

The RAG workflow is:

```text
PDF / Document
      │
      ▼
Document Loader
      │
      ▼
Text Extraction
      │
      ▼
Chunking
      │
      ▼
Embedding Generation
      │
      ▼
384-Dimensional Vector
      │
      ▼
Neon PostgreSQL + pgvector
      │
      │
User Question
      │
      ▼
Question Embedding
      │
      ▼
Vector Similarity Search
      │
      ▼
Top-K Relevant Chunks
      │
      ▼
Context
      │
      ▼
Groq LLM
      │
      ▼
AI Answer + Sources
```

Default configuration:

```env
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
TOP_K=5
```

---

# 📄 12. Test Document Upload

After the backend starts:

1. Login as administrator.
2. Open the Documents section.
3. Upload a small PDF.
4. Allow the backend to process the document.
5. Verify that embeddings are created.
6. Ask a question related to the uploaded document.

Expected backend request:

```text
POST /api/assistant/chat    200 OK
```

---

# 🎨 13. Frontend Setup

Open a **second PowerShell terminal**.

From the project root:

```powershell
cd frontend
```

Create the virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create `.env`:

```powershell
copy .env.example .env
```

---

# 🔗 14. Configure Frontend `.env`

Open:

```text
frontend/.env
```

Set:

```env
API_BASE_URL=http://127.0.0.1:8000
```

This connects Streamlit to FastAPI.

---

# ▶️ 15. Start Streamlit

From the `frontend` directory:

```powershell
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 🔄 16. Complete Local Startup

You need **two terminals**.

## Terminal 1 — FastAPI

```powershell
cd C:\AI-Workforce-Assistant-Platform\backend
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

## Terminal 2 — Streamlit

```powershell
cd C:\AI-Workforce-Assistant-Platform\frontend
.venv\Scripts\activate
streamlit run app.py
```

Application:

```text
http://localhost:8501
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 🧪 17. Complete Testing Order

Test the application in this order:

```text
1. Start Neon PostgreSQL
       ↓
2. Run migrations
       ↓
3. Start FastAPI
       ↓
4. Test /health
       ↓
5. Create admin
       ↓
6. Test login
       ↓
7. Start Streamlit
       ↓
8. Login from frontend
       ↓
9. Test Team
       ↓
10. Upload Document
       ↓
11. Verify Embeddings
       ↓
12. Test RAG Assistant
       ↓
13. Test Dataset CRUD
       ↓
14. Test Recommendations
       ↓
15. Test Power BI
```

---

# 🧩 18. Troubleshooting

## Backend cannot start

Activate the environment:

```powershell
.venv\Scripts\activate
```

Install dependencies again:

```powershell
pip install -r requirements.txt
```

Start:

```powershell
uvicorn app.main:app --reload --port 8000
```

---

## Frontend cannot connect to backend

Check FastAPI:

```text
http://127.0.0.1:8000/health
```

Check:

```env
API_BASE_URL=http://127.0.0.1:8000
```

Make sure both applications are running.

---

## Groq `model_not_found`

Check models available to your API key:

```powershell
python -c "from groq import Groq; import os; c=Groq(api_key=os.getenv('GROQ_API_KEY')); print([m.id for m in c.models.list().data if m.active])"
```

Choose an available model:

```env
GROQ_MODEL=MODEL_ID
```

Restart FastAPI:

```powershell
uvicorn app.main:app --reload --port 8000
```

---

## Database connection error

Check:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require
```

Then:

```powershell
alembic current
```

If required:

```powershell
alembic upgrade head
```

---

## pgvector error

Run in Neon SQL Editor:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Then:

```powershell
alembic upgrade head
```

---

# 🌐 19. Deployment Order

For production deployment, deploy the **backend first**.

```text
                    GitHub
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   FastAPI Backend          Streamlit Frontend
          │                       │
          │                       │
          ▼                       │
   Neon PostgreSQL ◄──────────────┘
       + pgvector
          │
          ├──────────► Groq
          │
          └──────────► Hugging Face
```

## Recommended deployment sequence

```text
1. Push clean code to GitHub
        ↓
2. Create Neon PostgreSQL
        ↓
3. Enable pgvector
        ↓
4. Deploy FastAPI backend
        ↓
5. Add backend environment variables
        ↓
6. Run migrations
        ↓
7. Test /health
        ↓
8. Test /docs
        ↓
9. Test authentication
        ↓
10. Test RAG
        ↓
11. Deploy Streamlit frontend
        ↓
12. Set API_BASE_URL to backend URL
        ↓
13. Update CORS_ORIGINS
        ↓
14. Test complete application
```

---

# 🔐 20. Production Environment Variables

For production, configure environment variables through the hosting provider.

### Backend

```env
DATABASE_URL=YOUR_NEON_DATABASE_URL
GROQ_API_KEY=YOUR_GROQ_API_KEY
GROQ_MODEL=openai/gpt-oss-120b
JWT_SECRET_KEY=YOUR_LONG_RANDOM_SECRET
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
TOP_K=5
CORS_ORIGINS=YOUR_FRONTEND_URL
POWERBI_EMBED_URL=
HF_API_KEY=YOUR_HUGGINGFACE_API_KEY
```

### Frontend

```env
API_BASE_URL=YOUR_DEPLOYED_BACKEND_URL
```

Do **not** use:

```env
API_BASE_URL=http://127.0.0.1:8000
```

in production.

---

# 📁 21. Project Structure

```text
AI-Workforce-Assistant-Platform/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── rag/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── migrations/
│   ├── scripts/
│   ├── .env.example
│   ├── alembic.ini
│   └── requirements.txt
│
├── frontend/
│   ├── services/
│   ├── ui_pages/
│   │   ├── admin/
│   │   └── ...
│   ├── utils/
│   ├── .env.example
│   ├── app.py
│   └── requirements.txt
│
├── data/
│   └── sample.csv
│
├── docs/
│   └── architecture.md
│
├── .gitignore
└── README.md
```

---

# 🛠️ 22. Technology Stack

## Frontend

* Python
* Streamlit
* REST API
* JWT

## Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic
* Pydantic
* psycopg 3

## Database

* Neon PostgreSQL
* pgvector

## AI / RAG

* Groq
* GPT-OSS 120B
* Sentence Transformers
* all-MiniLM-L6-v2
* Vector similarity search
* Retrieval-Augmented Generation

## Authentication

* JWT
* bcrypt

## Integrations

* Hugging Face
* Power BI

---

# 🔒 23. Security Checklist

Before pushing to GitHub:

```powershell
git status
```

Check for exposed secrets:

```powershell
git grep -n "gsk_"
git grep -n "hf_"
git grep -n "npg_"
```

These commands should return no real credentials.

Never commit:

```text
.env
*.env
.venv/
__pycache__/
```

If credentials are accidentally exposed:

1. Rotate the Groq API key.
2. Rotate the Hugging Face token.
3. Change the Neon database password.
4. Generate a new JWT secret.
5. Update the deployment environment variables.

---

# 📌 24. Git Workflow

After making changes:

```powershell
git status
```

Add changes:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Update AI Workforce Assistant"
```

Push:

```powershell
git push origin main
```

Before pushing, always verify that secrets are not tracked.

---

# ⚡ 25. Quick Start

## Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
python scripts/create_admin.py
uvicorn app.main:app --reload --port 8000
```

## Frontend

Open another terminal:

```powershell
cd frontend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 📜 License

This project is intended for educational, research, portfolio, and demonstration purposes.
