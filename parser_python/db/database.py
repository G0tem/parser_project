import psycopg2
from config import db_name, db_user, db_pass, db_host


def save_database(results):
    """
    We save the data to the database, create a table if it does not exist
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    print("Соединение с базой данных установлено")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles
        (id SERIAL PRIMARY KEY, article_name TEXT, article_content TEXT, article_link TEXT, full_name_author TEXT, author_link TEXT, datetime_attr TEXT, name_author TEXT)
    ''')
    for result in results:
        article_name = list(result.keys())[0]
        article_content = result[article_name]
        article_link = result['article_link']
        full_name_author = result['full_name_author']
        author_link = result['author_link']
        datetime_attr = result['datetime_attr']
        name_author = result['name_author']

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
    # conn = psycopg2.connect(
    #     host="postgres_parser_python",
    #     database="postgres",
    #     user="postgres",
    #     password="ada32f24gfDSadgAedaacascaefiiuy"
    # )
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_pass
    )
    return conn
