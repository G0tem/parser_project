import psycopg2
from db.config import db_name, db_user, db_pass, db_host
from datetime import datetime


def save_database(results):
    """
    We save the data to the database, create a table if it does not exist
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles
        (id SERIAL PRIMARY KEY, article_name TEXT, article_content TEXT, article_link TEXT, full_name_author TEXT, author_link TEXT, datetime_attr TIMESTAMP WITH TIME ZONE, name_author TEXT)
    ''')
    for result in results:
        article_name = list(result.keys())[0]
        article_content = result[article_name]
        article_link = result['article_link']
        full_name_author = result['full_name_author']
        author_link = result['author_link']
        datetime_attr = result['datetime_attr']
        name_author = result['name_author']

        # print to console
        print(f"ИНФОРМАЦИЯ название: {article_name}, ссылка: {article_link}, автор: {name_author}, ссылка на автора: {author_link}, дата: {datetime_attr}, полное имя: {full_name_author}, текст: {article_content[:15]}...")
        print()
        # We check whether an entry with the same article_link already exists
        cursor.execute('''
            SELECT 1 FROM articles WHERE article_link = %s
        ''', (article_link,))
        if cursor.fetchone():
            print(f"Статья с article_link '{article_link}' уже существует в базе данных, пропускаем запись")
            continue

        # If the record does not exist, then write it to the database
        cursor.execute('''
            INSERT INTO articles (article_name, article_content, article_link, full_name_author, author_link, datetime_attr, name_author)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (article_name, article_content, article_link, full_name_author, author_link, datetime_attr, name_author))
        print(f"Запись '{article_name}' добавлена в базу данных")
    conn.commit()
    conn.close()

def connect_to_database():
    """
    Connecting to the database
    """
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_pass
    )
    return conn
