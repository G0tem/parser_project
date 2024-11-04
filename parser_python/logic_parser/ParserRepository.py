from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import time


ua = UserAgent()

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}

def parser_start(url):
    """
    Входная функция логики парсера
    """
    req = requests.get(url, headers=headers).text
    soup = BeautifulSoup(req, 'lxml')

    dict_home_page = parse_home_page(soup)

    for article_name, article_link in dict_home_page.items():
        parsed_articles = parse_article_page(article_name, article_link)
        print("Результат парсинга: ", parsed_articles)
        time.sleep(3)

        

def parse_home_page(soup):
    """Функция парсинга главной страницы, получает словарь с названиями и ссылками на статьи"""
    article_dict = {}
    all_hrefs_articles = soup.find_all('a', class_='tm-title__link') # получаем статьи

    for article in all_hrefs_articles: # проходимся по статьям
        article_name = article.find('span').text # собираем названия статей
        article_link = f'https://habr.com{article.get("href")}' # ссылки на статьи
        article_dict[article_name] = article_link

    return article_dict

def parse_article_page(article_name, article_link):
    """Функция парсинга статьи, получаем словарь с содержимым статьи, датой и информацией об авторе"""
    time.sleep(3) 
    parsed_articles = {}
    try:
        req = requests.get(article_link, headers=headers).text
        soup = BeautifulSoup(req, 'lxml')
        article_content = soup.find('div', class_='article-formatted-body').text.strip()
        parsed_articles[article_name] = article_content
        parsed_articles["article_link"] = article_link

        # Проверяем имя автора
        try:
            full_name_author = soup.find("span", class_='tm-user-card__name').text.strip()
            parsed_articles["full_name_author"] = full_name_author
        except Exception as e:
            parsed_articles["full_name_author"] = None
        
        # Парсим информацию об авторе
        author = soup.find('div', class_='tm-article-presenter__header')
        author_name, author_link, datetime_attr = parse_author(author)
        
        parsed_articles["author_link"] = author_link
        parsed_articles["datetime_attr"] = datetime_attr
        parsed_articles["name_author"] = author_name
    except Exception as e:
        print(f"Ошибка парсинга статьи {article_name}: {str(e)}")
    
    return parsed_articles

def parse_author(author):
    """Функция парсинга информации об авторе"""
    block_url = author.find('a')
    author_name = block_url.get('title') # Ник автора
    article_link = f'https://habr.com{block_url.get("href")}' # ссылки на автора

    datastr = author.find("span", class_='tm-article-datetime-published')
    time_element = datastr.find("time")
    datetime_attr = time_element.get("datetime")  # время статьи
    return author_name, article_link, datetime_attr
