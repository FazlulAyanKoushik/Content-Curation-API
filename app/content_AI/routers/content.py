# routers/content.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.accounts.models.user import User
from app.accounts.permissions import get_current_user
from app.config.database import get_db
from app.content_AI.models.content import Content, AIAnalysis
from app.content_AI.schemas.content import (
    ContentCreate,
    ContentOut,
    ContentUpdate,
    ContentPublicSummary,
    ContentWithAnalysis
)
from app.content_AI.services.ai_service import AIService

content_router = APIRouter(prefix="/content", tags=["content"])
ai_service = AIService()


@content_router.post("/", response_model=ContentWithAnalysis)
async def create_content(
        content_data: ContentCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Create content
    db_content = Content(
        title=content_data.title,
        url=str(content_data.url) if content_data.url else None,
        raw_text=content_data.raw_text,
        user_id=current_user.id,
        is_public=content_data.is_public
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)

    # Automatically analyze content if text is provided
    if db_content.raw_text:
        analysis_result = await ai_service.analyze_content(db_content.raw_text)

        db_analysis = AIAnalysis(
            content_id=db_content.id,
            summary=analysis_result["summary"],
            sentiment=analysis_result["sentiment"],
            topics=analysis_result["topics"]
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_content)

    return db_content


@content_router.get("/public", response_model=List[ContentPublicSummary])
def get_public_contents(db: Session = Depends(get_db)):
    """Get public content with just summary info"""
    return (
        db.query(Content, AIAnalysis)
        .join(AIAnalysis)
        .filter(Content.is_public == True)
        .all()
    )


@content_router.get("/{content_id}", response_model=ContentWithAnalysis)
def get_content(
        content_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    content = (
        db.query(Content)
        .options(joinedload(Content.ai_analysis))
        .filter(Content.id == content_id)
        .first()
    )
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Check access
    if not content.is_public and content.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this content"
        )

    return content


@content_router.put("/{content_id}", response_model=ContentWithAnalysis)
async def update_content(
        content_id: int,
        content_data: ContentUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_content = (
        db.query(Content)
        .options(joinedload(Content.ai_analysis))
        .filter(Content.id == content_id)
        .first()
    )
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")

    if db_content.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this content"
        )

    # Update fields if provided
    if content_data.title is not None:
        db_content.title = content_data.title
    if content_data.url is not None:
        db_content.url = str(content_data.url) if content_data.url else None
    if content_data.raw_text is not None:
        db_content.raw_text = content_data.raw_text
    if content_data.is_public is not None:
        db_content.is_public = content_data.is_public

    # Re-analyze if raw_text was updated
    if content_data.raw_text is not None and db_content.raw_text:
        analysis_result = await ai_service.analyze_content(db_content.raw_text)

        if db_content.ai_analysis:
            # Update existing analysis
            db_content.ai_analysis.summary = analysis_result["summary"]
            db_content.ai_analysis.sentiment = analysis_result["sentiment"]
            db_content.ai_analysis.topics = analysis_result["topics"]
        else:
            # Create new analysis
            db_analysis = AIAnalysis(
                content_id=db_content.id,
                summary=analysis_result["summary"],
                sentiment=analysis_result["sentiment"],
                topics=analysis_result["topics"]
            )
            db.add(db_analysis)

    db.commit()
    db.refresh(db_content)
    return db_content