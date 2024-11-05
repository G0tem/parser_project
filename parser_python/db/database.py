import psycopg2


def save_database(results):
    """
    Сохраняем данные в базу данных, создаем таблицу если ее нет
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

        # Проверяем, существует ли уже запись с таким-же article_link
        cursor.execute('''
            SELECT 1 FROM articles WHERE article_link = %s
        ''', (article_link,))
        if cursor.fetchone():
            print(f"Статья с article_link '{article_link}' уже существует в базе данных, пропускаем запись")
            continue

        # Если запись не существует, то записываем ее в базу данных
        cursor.execute('''
            INSERT INTO articles (article_name, article_content, article_link, full_name_author, author_link, datetime_attr, name_author)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (article_name, article_content, article_link, full_name_author, author_link, datetime_attr, name_author))
    conn.commit()
    conn.close()

def connect_to_database():
    """
    Подключаемся к базе данных
    """
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="ada32f24gfDSadgAedaacascaefiiuy"
    )
    return conn
