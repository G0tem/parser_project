from pydantic import BaseModel
from datetime import datetime

class Article(BaseModel):
    id: int
    article_name: str
    article_content: str
    article_link: str
    full_name_author: str | None = None
    author_link: str
    datetime_attr: datetime
    name_author: str


class ArticleAdd(BaseModel):
    article_name: str
    article_content: str
    article_link: str
    full_name_author: str | None = None
    author_link: str
    datetime_attr: datetime
    name_author: str