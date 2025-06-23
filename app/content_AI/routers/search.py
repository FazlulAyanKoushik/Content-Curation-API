# routers/search.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.search_service import SearchService, RecommendationService
from ...accounts.models.user import User
from ...accounts.permissions import get_current_user
from ...config.database import get_db

search_router = APIRouter(prefix="/search", tags=["search"])
search_service = SearchService()
recommendation_service = RecommendationService()

@search_router.get("/public")
async def search_public_content(
    query: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db)
):
    return await search_service.search_public_content(query, db)

@search_router.get("/user")
async def search_user_content(
    query: str = Query(..., min_length=2),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await search_service.search_user_content(query, current_user.id, db)

@search_router.get("/recommend/{content_id}")
async def get_recommendations(
    content_id: int,
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    return await recommendation_service.get_recommendations(content_id, limit, db)