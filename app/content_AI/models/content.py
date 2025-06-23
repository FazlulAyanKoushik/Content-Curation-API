# models/content.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, nullable=True)
    raw_text = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="contents")
    ai_analysis = relationship("AIAnalysis", back_populates="content", uselist=False, cascade="all, delete-orphan")

class AIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"))
    summary = Column(Text)
    sentiment = Column(String)  # "positive", "negative", "neutral"
    topics = Column(String)  # Comma-separated topics
    created_at = Column(DateTime, default=datetime.utcnow)

    content = relationship("Content", back_populates="ai_analysis")