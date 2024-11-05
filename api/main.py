from fastapi import FastAPI
from router.ArticleRouter import entity_router


app = FastAPI()

app.include_router(entity_router)
