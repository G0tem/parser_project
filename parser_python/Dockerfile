FROM python:3.12

RUN mkdir /parser

WORKDIR /parser

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080

COPY . .

CMD [ "python3", "main.py" ]
