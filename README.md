# AI Workforce Assistant — Neon PostgreSQL + pgvector CRUD Data Viewer

Full-stack AI Workforce platform with Streamlit, FastAPI, Neon PostgreSQL, pgvector, Groq, JWT authentication and RAG.

## Architecture

```text
Streamlit
   |
   | REST + JWT
   v
FastAPI
   |
   +--> Neon PostgreSQL
   |      +--> users / documents / recommendations / chats
   |      +--> datasets
   |      +--> dataset_rows
   |      +--> pgvector embeddings
   |
   +--> Sentence Transformers
   |      +--> all-MiniLM-L6-v2 (384 dimensions)
   |
   +--> Groq LLM
```

## 1. Clone / enter project

```powershell
git clone https://github.com/Yakaanil2006/Updated-AI-Workforce.git
cd Updated-AI-Workforce
```

If you are using the supplied ZIP instead, extract it and open PowerShell in the extracted project folder.

## 2. Create Neon database

Create a database in Neon and copy its connection string.

Enable pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

The connection string should use psycopg 3:

```text
postgresql+psycopg://USER:PASSWORD@HOST/DB?sslmode=require
```

## 3. Backend setup — Windows PowerShell

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Edit `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DB?sslmode=require
GROQ_API_KEY=YOUR_GROQ_KEY
GROQ_MODEL=llama-3.3-70b-versatile
JWT_SECRET_KEY=YOUR_LONG_RANDOM_SECRET
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
TOP_K=5
CORS_ORIGINS=http://localhost:8501
POWERBI_EMBED_URL=
```

Run all migrations, including the new dataset/pgvector schema:

```powershell
alembic upgrade head
```

Verify the migration state:

```powershell
alembic current
```

Create the first admin user:

```powershell
python scripts/create_admin.py
```

Start FastAPI:

```powershell
uvicorn app.main:app --reload --port 8000
```

Backend URLs:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 4. Frontend setup

Open a second PowerShell terminal:

```powershell
cd frontend
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

`frontend/.env`:

```env
API_BASE_URL=http://127.0.0.1:8000
```

Start Streamlit:

```powershell
streamlit run app.py
```

Open:

```text
http://localhost:8501
```