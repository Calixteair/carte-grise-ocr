from typing import Optional
import base64

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document
from app.schemas.common import Document as DocumentSchema
from app.worker.tasks import process_image_for_extraction
from app.services.image_processing import is_valid_image

from app.models.user import User
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/upload-and-extract/", response_model=DocumentSchema)
async def upload_image_for_extraction(
    file: UploadFile = File(...),
    country_code: str = Form(..., description="Country code (e.g., 'FR' for France, 'TN' for Tunisia)"),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only image files are allowed."
        )

    image_data = await file.read()

    if not is_valid_image(image_data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not process image. File might be corrupted or an unsupported format."
        )

    # Encode image to base64
    image_base64 = base64.b64encode(image_data).decode("utf-8")

    # Ensure a default user exists to prevent foreign key violations.
    default_user = db.query(User).filter(User.id == 1).first()
    if not default_user:
        default_user = User(
            id=1,
            email="default@example.com",
            hashed_password=get_password_hash("defaultpassword"),
            is_active=True
        )
        db.add(default_user)

    # Create a new document entry in the database
    db_document = Document(
        filename=file.filename,
        status="pending",
        owner_id=default_user.id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # Enqueue the extraction task
    process_image_for_extraction.delay(db_document.id, image_base64, country_code)

    return db_document

@router.get("/task-status/{document_id}", response_model=DocumentSchema)
async def get_extraction_task_status(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found."
        )
    return document
