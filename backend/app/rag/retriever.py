from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.document import DocumentChunk
from app.rag.embeddings import embed_query


def search_chunks(db: Session, question: str, top_k: int = 5):
    vector = embed_query(question)

    distance = DocumentChunk.embedding.cosine_distance(vector)

    stmt = (
        select(DocumentChunk)
        .where(DocumentChunk.embedding.is_not(None))
        .order_by(distance)
        .limit(top_k)
    )

    return db.execute(stmt).scalars().all()
