from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import datetime
from sqlalchemy.types import DateTime


Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_name: Mapped[str]
    article_content: Mapped[str]
    article_link: Mapped[str]
    full_name_author: Mapped[str | None]
    author_link: Mapped[str]
    datetime_attr: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    name_author: Mapped[str]
