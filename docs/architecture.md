# Architecture

## Frontend

Streamlit renders the public landing page, RAG assistant, Power BI dashboard, data viewer and admin control center.

## Backend

FastAPI exposes authenticated REST APIs. SQLAlchemy handles persistence and Alembic handles migrations.

## Database

Neon PostgreSQL stores application data. pgvector stores document embeddings in `document_chunks.embedding`.

## RAG

1. Admin uploads a document.
2. FastAPI extracts text.
3. Text is chunked.
4. sentence-transformers generates 384-dimensional embeddings.
5. Embeddings are stored in Neon PostgreSQL.
6. User question is embedded.
7. PostgreSQL performs cosine similarity search.
8. Top 5 chunks are placed into the prompt.
9. Groq generates a grounded answer.
10. Sources are returned to Streamlit.
