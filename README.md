AI Workforce Assistant

A full-stack AI Workforce Assistant platform built with Streamlit, FastAPI, Neon PostgreSQL, pgvector, Groq, JWT authentication, and RAG.

Architecture

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
    ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
    │ Neon PostgreSQL  │  │ Embedding Model  │  │    Groq LLM      │
    │                  │  │                  │  │                  │
    │ users            │  │ all-MiniLM-L6-v2 │  │ GPT-OSS 120B     │
    │ documents        │  │ 384 dimensions   │  │                  │
    │ recommendations  │  │                  │  │ RAG Generation   │
    │ chats            │  └──────────────────┘  └──────────────────┘
    │ datasets         │
    │ dataset_rows     │
    │ pgvector         │
    └──────────────────┘

Dataset and Recommendations Architecture

Data Viewer
     │
     │ Upload CSV
     ▼
Neon PostgreSQL
     │
     ├── datasets
     │
     └── dataset_rows
            │
            ▼
     Recommendations
            │
            ▼
      Python Analysis
            │
            ▼
           Groq
            │
            ▼
     recommendations

Technology Stack

Frontend

Python

Streamlit

REST API

JWT

Backend

Python

FastAPI

SQLAlchemy

Alembic

Pydantic

psycopg 3

Database

Neon PostgreSQL

pgvector

AI / RAG

Groq

GPT-OSS 120B

Sentence Transformers

all-MiniLM-L6-v2

Vector similarity search

Retrieval-Augmented Generation

Authentication

JWT

bcrypt

Integrations

Hugging Face

Power BI

Project Structure

AI-Workforce-Assistant-Platform/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── dataset.py
│   │   │   ├── recommendation.py
│   │   │   └── ...
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── datasets.py
│   │   │   ├── recommendations.py
│   │   │   └── ...
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── dataset.py
│   │   │   └── ...
│   │   │
│   │   ├── services/
│   │   │   ├── groq_service.py
│   │   │   ├── recommendation_service.py
│   │   │   └── ...
│   │   │
│   │   ├── rag/
│   │   │   ├── embeddings.py
│   │   │   └── ...
│   │   │
│   │   └── main.py
│   │
│   ├── migrations/
│   │   └── versions/
│   │
│   ├── scripts/
│   │   └── create_admin.py
│   │
│   ├── .env
│   ├── .env.example
│   ├── alembic.ini
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── services/
│   │   └── api.py
│   │
│   ├── ui_pages/
│   │   ├── admin/
│   │   │   └── ...
│   │   ├── data_viewer.py
│   │   ├── recommendations.py
│   │   └── ...
│   │
│   ├── utils/
│   │   └── ...
│   │
│   ├── app.py
│   ├── .env
│   ├── .env.example
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

Backend Structure

backend/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── dataset.py
│   │   └── recommendation.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── datasets.py
│   │   └── recommendations.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   └── dataset.py
│   │
│   ├── services/
│   │   ├── groq_service.py
│   │   └── recommendation_service.py
│   │
│   ├── rag/
│   │   └── embeddings.py
│   │
│   └── main.py
│
├── migrations/
├── scripts/
├── .env
├── .env.example
├── alembic.ini
└── requirements.txt

Frontend Structure

frontend/
│
├── services/
│   └── api.py
│
├── ui_pages/
│   ├── admin/
│   ├── data_viewer.py
│   ├── recommendations.py
│   └── ...
│
├── utils/
│   └── ...
│
├── app.py
├── .env
├── .env.example
└── requirements.txt

Database Structure

Neon PostgreSQL
│
├── users
├── datasets
├── dataset_rows
├── documents
├── document_chunks
├── chat_sessions
├── chat_messages
├── recommendations
├── team_members
└── powerbi_dashboards

Dataset Flow

Data Viewer
    │
    │ Upload CSV
    ▼
datasets
    │
    ▼
dataset_rows
    │
    ▼
Recommendations
    │
    ▼
Pandas DataFrame
    │
    ▼
Dataset Analysis
    │
    ▼
Groq
    │
    ▼
recommendations

RAG Flow

Document
    │
    ▼
Text Extraction
    │
    ▼
Chunking
    │
    ▼
Embeddings
    │
    ▼
pgvector
    │
    ▼
Similarity Search
    │
    ▼
Relevant Context
    │
    ▼
Groq
    │
    ▼
Answer

Application Flow

User
 │
 ▼
Streamlit
 │
 │ REST + JWT
 ▼
FastAPI
 │
 ├──────────────► Authentication
 │
 ├──────────────► Data Viewer
 │                    │
 │                    ▼
 │              PostgreSQL
 │
 ├──────────────► Recommendations
 │                    │
 │                    ▼
 │                   Groq
 │
 ├──────────────► RAG
 │                    │
 │                    ▼
 │                 pgvector
 │
 └──────────────► Power BI

Clone Repository

git clone https://github.com/Yakaanil2006/AI-Workforce-Assistant-Platform.git
cd AI-Workforce-Assistant-Platform

Neon PostgreSQL

Create a Neon PostgreSQL database.

Set:

postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require

Enable pgvector:

CREATE EXTENSION IF NOT EXISTS vector;

Backend Setup

cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env

Backend Environment

Configure backend/.env:

DATABASE_URL=YOUR_NEON_DATABASE_URL

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

Do not commit .env.

.gitignore

.env
*.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
.streamlit/secrets.toml

Keep:

backend/.env.example

Do not commit:

backend/.env

Database Migrations

cd backend
alembic upgrade head
alembic current

Create Administrator

python scripts/create_admin.py

Test Groq

python -c "from groq import Groq; import os; c=Groq(api_key=os.getenv('GROQ_API_KEY')); print([m.id for m in c.models.list().data if m.active])"

python -c "from groq import Groq; import os; c=Groq(api_key=os.getenv('GROQ_API_KEY')); r=c.chat.completions.create(model='openai/gpt-oss-120b',messages=[{'role':'user','content':'Say hello'}]); print(r.choices[0].message.content)"

Start FastAPI

cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

URLs:

http://127.0.0.1:8000
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs

Frontend Setup

Open another terminal:

cd frontend
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env

Configure frontend/.env:

API_BASE_URL=http://127.0.0.1:8000

Start Streamlit

cd frontend
.venv\Scripts\activate
streamlit run app.py

Open:

http://localhost:8501

Local Startup

Terminal 1 — Backend

cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

Terminal 2 — Frontend

cd frontend
.venv\Scripts\activate
streamlit run app.py

Authentication

POST /api/auth/login
GET  /api/auth/me

Data Viewer

Dataset upload flow:

Data Viewer
    ↓
Upload CSV
    ↓
datasets
    ↓
dataset_rows

The uploaded datasets are stored in PostgreSQL.

Recommendations use the same datasets and dataset_rows records.

Recommendations

Select Dataset
      ↓
Load Dataset + DatasetRow
      ↓
Build pandas DataFrame
      ↓
Analyze Dataset
      ↓
Groq
      ↓
Save Recommendations

Analysis includes:

Missing values

Duplicate rows

Numeric statistics

Categorical statistics

Outliers

Strong correlations

RAG Pipeline

PDF / Document
      ↓
Document Loader
      ↓
Text Extraction
      ↓
Chunking
      ↓
Embedding Generation
      ↓
384-Dimensional Vector
      ↓
Neon PostgreSQL + pgvector
      ↓
User Question
      ↓
Question Embedding
      ↓
Vector Similarity Search
      ↓
Top-K Relevant Chunks
      ↓
Context
      ↓
Groq LLM
      ↓
AI Answer + Sources

Default configuration:

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
TOP_K=5

Document Upload

POST /api/assistant/chat

CSV Upload Encoding

Supported encoding fallback:

utf-8
utf-8-sig
cp1252
latin1

Administrator Management

Administrators are deactivated instead of physically deleted when related records exist.

users.is_active = false

Inactive administrators:

Are excluded from the active administrator list.

Cannot log in.

Keep historical records.

Clear Application Data

Keep the users table.

Run in Neon SQL Editor:

BEGIN;

TRUNCATE TABLE
    chat_messages,
    chat_sessions,
    dataset_rows,
    datasets,
    document_chunks,
    documents,
    powerbi_dashboards,
    recommendations,
    team_members
RESTART IDENTITY CASCADE;

COMMIT;

Do not truncate:

users
alembic_version

Testing Order

1. Neon PostgreSQL
2. Database migrations
3. FastAPI
4. Health check
5. Authentication
6. Streamlit
7. Data Viewer
8. CSV upload
9. Dataset verification
10. Recommendations
11. RAG
12. Power BI

Troubleshooting

Backend

.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

Database

alembic current
alembic upgrade head

pgvector

CREATE EXTENSION IF NOT EXISTS vector;

CSV Encoding

utf-8
utf-8-sig
cp1252
latin1

Groq Model

python -c "from groq import Groq; import os; c=Groq(api_key=os.getenv('GROQ_API_KEY')); print([m.id for m in c.models.list().data if m.active])"

Update:

GROQ_MODEL=MODEL_ID

Restart:

uvicorn app.main:app --reload --port 8000

Frontend Connection

API_BASE_URL=http://127.0.0.1:8000

Production Deployment

GitHub
   ↓
FastAPI Backend
   ↓
Neon PostgreSQL + pgvector
   ↓
Streamlit Frontend
   ↓
Groq / Hugging Face

Deployment order:

1. Push code
2. Create Neon PostgreSQL
3. Enable pgvector
4. Deploy FastAPI
5. Configure backend environment variables
6. Run migrations
7. Test /health
8. Test /docs
9. Test authentication
10. Test RAG
11. Deploy Streamlit
12. Configure API_BASE_URL
13. Configure CORS_ORIGINS
14. Test application

Production Environment

Backend

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

Frontend

API_BASE_URL=YOUR_DEPLOYED_BACKEND_URL

Do not use:

API_BASE_URL=http://127.0.0.1:8000

in production.

Security

git status
git grep -n "gsk_"
git grep -n "hf_"
git grep -n "npg_"

Do not commit:

.env
*.env
.venv/
__pycache__/

If credentials are exposed:

Rotate Groq API key
Rotate Hugging Face token
Change Neon database password
Generate new JWT secret
Update deployment environment variables

Git Workflow

git status
git add .
git commit -m "Update AI Workforce Assistant"
git push origin main

Quick Start

Backend

cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
python scripts/create_admin.py
uvicorn app.main:app --reload --port 8000

Frontend

cd frontend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py

Frontend: http://localhost:8501
Backend:  http://127.0.0.1:8000
Swagger:  http://127.0.0.1:8000/docs

License

This project is intended for educational, research, portfolio, and demonstration purposes.
