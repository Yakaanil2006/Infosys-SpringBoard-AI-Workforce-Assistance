from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_admin
from app.models.document import Document
from app.models.user import User
from app.services.rag_service import ingest_document

router = APIRouter(prefix="/api/admin/documents", tags=["documents"])


@router.get("")
def list_documents(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    docs = db.execute(select(Document).order_by(Document.created_at.desc())).scalars().all()
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "file_type": d.file_type,
            "status": d.status,
            "chunk_count": d.chunk_count,
            "created_at": d.created_at,
        }
        for d in docs
    ]


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    allowed = {".pdf", ".docx", ".txt", ".csv"}
    suffix = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""

    if suffix not in allowed:
        raise HTTPException(status_code=400, detail="Supported formats: PDF, DOCX, TXT, CSV")

    content = await file.read()

    document = Document(
        filename=file.filename,
        file_type=suffix[1:],
        uploaded_by=user.id,
        status="processing",
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    try:
        ingest_document(db, content, file.filename, document)
    except Exception as exc:
        document.status = "failed"
        db.commit()
        raise HTTPException(status_code=400, detail=str(exc))

    return {
        "message": "Document indexed",
        "id": document.id,
        "filename": document.filename,
        "chunks": document.chunk_count,
    }


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    db.delete(document)
    db.commit()
    return {"message": "Document and vector chunks deleted"}
