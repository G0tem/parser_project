# parser_project

Парсер статей хабр, на python

При запуске происходит парсинг главной страницы и страниц этих статей.
Результат сохраняется в postgres.
Также настроена api с CRUD манипуляциями для работы с данными. swagger документацию открыть по http://0.0.0.0:8000/docs

Запуск командой: docker compose up -d --build

запуск 3х контейнеров:

БД postgres
api на фреймворке fastapi, ORM - SQLAlchemy, alembic - для работы с миграциями
Парсер использует BeautifulSoup, библиотеку для асинхронной работы asyncio, aiohttp
