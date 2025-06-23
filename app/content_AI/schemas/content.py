from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl

# Base schemas
class ContentBase(BaseModel):
    title: str
    url: Optional[HttpUrl] = None
    raw_text: Optional[str] = None
    is_public: bool = False

# Request schemas
class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[HttpUrl] = None
    raw_text: Optional[str] = None
    is_public: Optional[bool] = None

# Response schemas
class AIAnalysisBase(BaseModel):
    summary: str
    sentiment: str  # "positive", "negative", "neutral"
    topics: str     # Comma-separated topics
    created_at: datetime

    class Config:
        from_attributes = True

class ContentOut(ContentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    ai_analysis: Optional[AIAnalysisBase] = None

    class Config:
        from_attributes = True

# Specialized response schemas
class ContentPublicSummary(BaseModel):
    id: int
    title: str
    summary: str
    topics: str
    created_at: datetime

    class Config:
        from_attributes = True

class ContentWithAnalysis(ContentOut):
    ai_analysis: AIAnalysisBase

    class Config:
        from_attributes = True