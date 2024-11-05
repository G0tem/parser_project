from fastapi import HTTPException
from models.ArticleModel import Article
from sqlalchemy import select
from schemas.ArticleSchemas import ArticleAdd


class ArticleRepositories:
    """Class for article repositories."""

    async def get_article(session):
        articles = await session.execute(
            select(Article).order_by(Article.id)
        )
        return [
            {
                "id": article.id,
                "article_name": article.article_name,
                "article_content": article.article_content,
                "article_link": article.article_link,
                "full_name_author": article.full_name_author,
                "author_link": article.author_link,
                "datetime_attr": article.datetime_attr,
                "name_author": article.name_author,
            }
            for article in articles.scalars().all()
        ]

    async def post_article(article, session):
        new_article = Article(
            article_name=article.article_name,
            article_content=article.article_content,
            article_link=article.article_link,
            full_name_author=article.full_name_author,
            author_link=article.author_link,
            datetime_attr=article.datetime_attr,
            name_author=article.name_author
        )
        session.add(new_article)
        await session.commit()
        await session.refresh(new_article)
        return {
            "id": new_article.id,
            "article_name": new_article.article_name,
            "article_content": new_article.article_content,
            "article_link": new_article.article_link,
            "full_name_author": new_article.full_name_author,
            "author_link": new_article.author_link,
            "datetime_attr": new_article.datetime_attr,
            "name_author": new_article.name_author
        }

    async def update_article(id: int, article: ArticleAdd, session):
        article_to_update = await session.get(Article, id)
        if article_to_update is None:
            raise HTTPException(status_code=404, detail=f"нет cтатьи с {id}, изменить невозможно")
        article_to_update.article_name = article.article_name
        article_to_update.article_content = article.article_content
        article_to_update.article_link = article.article_link
        article_to_update.full_name_author = article.full_name_author
        article_to_update.author_link = article.author_link
        article_to_update.datetime_attr = article.datetime_attr
        article_to_update.name_author = article.name_author
        await session.commit()
        await session.refresh(article_to_update)
        return {
            "id": article_to_update.id,
            "article_name": article_to_update.article_name,
            "article_content": article_to_update.article_content,
            "article_link": article_to_update.article_link,
            "full_name_author": article_to_update.full_name_author,
            "author_link": article_to_update.author_link,
            "datetime_attr": article_to_update.datetime_attr,
            "name_author": article_to_update.name_author
        }

    async def delete_article(id: int, session):
        article_to_delete = await session.get(Article, id)
        if article_to_delete is None:
            raise HTTPException(status_code=404, detail=f"нет cтатьи с {id}, удалить невозможно")
        await session.delete(article_to_delete)
        await session.commit()
        return {"message": "Entity deleted"}
       