# services/search_service.py
from sqlalchemy import or_, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List

from app.content_AI.models.content import Content, AIAnalysis
from app.content_AI.schemas.content import ContentPublicSummary


class SearchService:
    async def search_public_content(
            self,
            query: str,
            db: AsyncSession
    ) -> List[ContentPublicSummary]:
        """Search only public content asynchronously"""
        search = f"%{query}%"

        stmt = (
            select(Content)
            .join(AIAnalysis)
            .where(
                and_(
                    Content.is_public == True,
                    or_(
                        Content.title.ilike(search),
                        AIAnalysis.summary.ilike(search),
                        AIAnalysis.topics.ilike(search)
                    )
                )
            )
            .options(selectinload(Content.ai_analysis))
        )

        result = await db.execute(stmt)
        contents = result.scalars().all()

        return [
            ContentPublicSummary(
                id=content.id,
                title=content.title,
                summary=content.ai_analysis.summary,
                topics=content.ai_analysis.topics,
                created_at=content.created_at
            )
            for content in contents
        ]

    async def search_user_content(
            self,
            query: str,
            user_id: int,
            db: AsyncSession
    ) -> List[Content]:
        """Search user's private content asynchronously"""
        search = f"%{query}%"

        stmt = (
            select(Content)
            .join(AIAnalysis)
            .where(
                and_(
                    Content.user_id == user_id,
                    or_(
                        Content.title.ilike(search),
                        AIAnalysis.summary.ilike(search),
                        AIAnalysis.topics.ilike(search)
                    )
                )
            )
            .options(selectinload(Content.ai_analysis))
        )

        result = await db.execute(stmt)
        return result.scalars().all()


class RecommendationService:
    async def get_recommendations(
            self,
            content_id: int,
            limit: int,
            db: AsyncSession
    ) -> List[Content]:
        """Get similar content based on topics asynchronously"""
        # First get the content with its analysis
        content_stmt = (
            select(Content)
            .join(AIAnalysis)
            .where(Content.id == content_id)
            .options(selectinload(Content.ai_analysis))
        )
        content_result = await db.execute(content_stmt)
        content = content_result.scalar_one_or_none()

        if not content or not content.ai_analysis:
            return []

        topics = content.ai_analysis.topics.split(",")
        recommendations = []

        # Get recommendations for each topic
        for topic in topics[:3]:  # Use top 3 topics
            topic = topic.strip()
            stmt = (
                select(Content)
                .join(AIAnalysis)
                .where(
                    and_(
                        Content.id != content_id,
                        Content.is_public == True,
                        or_(
                            AIAnalysis.topics.ilike(f"%{topic}%"),
                            Content.title.ilike(f"%{topic}%")
                        )
                    )
                )
                .limit(limit)
                .options(selectinload(Content.ai_analysis))
            )

            result = await db.execute(stmt)
            recommendations.extend(result.scalars().all())

        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec.id not in seen:
                seen.add(rec.id)
                unique_recommendations.append(rec)

        return unique_recommendations[:limit]