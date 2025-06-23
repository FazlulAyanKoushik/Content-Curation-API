# routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

from app.accounts.models.user import User
from app.accounts.permissions import admin_required
from app.config.database import get_db
from app.content_AI.models.content import Content
from app.content_AI.schemas.content import ContentOut

admin_content_router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(admin_required)])


@admin_content_router.get("/contents", response_model=List[ContentOut])
def get_all_contents(

        db: Session = Depends(get_db)
):
    """Admin can see all content regardless of privacy"""
    return db.query(Content).all()


@admin_content_router.delete("/content/{content_id}")
def admin_delete_content(
        content_id: int,
        db: Session = Depends(get_db)
):
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    db.delete(content)
    db.commit()
    return {"status": "success", "message": "Content deleted"}