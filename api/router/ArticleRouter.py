from typing import Annotated
from fastapi import APIRouter, Depends

from repositories.ArticleRepositories import ArticleRepositories
from schemas.ArticleSchemas import Article, ArticleAdd
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session


entity_router = APIRouter(
    prefix="/api/v1",
    tags=["Article"]
)


@entity_router.get("/article")
async def get_entity(session: AsyncSession = Depends(get_async_session)) -> list[Article]:
    """Get article."""
    result = await ArticleRepositories.get_article(session)
    return result

@entity_router.post("/article")
async def post_entity(article: Annotated[ArticleAdd, Depends()], session: AsyncSession = Depends(get_async_session)) -> Article:
    """Post article."""
    result =  await ArticleRepositories.post_article(article, session)
    return result

@entity_router.put("/article/{id:int}")
async def update_entity(id, article: Annotated[Article, Depends()], session: AsyncSession = Depends(get_async_session)) -> Article:
    """Update article."""
    result = await ArticleRepositories.update_article(id, article, session)
    return result

@entity_router.delete("/article/{id:int}")
async def delete_entity(id: int, session: AsyncSession = Depends(get_async_session)):
    """Delete article."""
    result = await ArticleRepositories.delete_article(id, session)
    return result