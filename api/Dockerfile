FROM python:3.12

RUN mkdir /fastapi

WORKDIR /fastapi

COPY api_requirements.txt .

RUN pip install -r api_requirements.txt

EXPOSE 8000

COPY . .

CMD alembic upgrade head && uvicorn main:app --reload --host 0.0.0.0 --port 8000