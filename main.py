from bs4 import BeautifulSoup
import random
import json
import requests
import datetime
from fake_useragent import UserAgent
import os
import time


ua = UserAgent()

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}

# Создайте папку для хранения распарсенных статей
directory = f"folder_parsed_articles"
if not os.path.exists(directory):
    os.makedirs(directory)

article_dict = {}

url = f'https://habr.com/ru/articles/'

req = requests.get(url, headers=headers).text

soup = BeautifulSoup(req, 'lxml')
all_hrefs_articles = soup.find_all('a', class_='tm-title__link') # получаем статьи

for article in all_hrefs_articles: # проходимся по статьям
    article_name = article.find('span').text # собираем названия статей
    article_link = f'https://habr.com{article.get("href")}' # ссылки на статьи
    article_dict[article_name] = article_link

file_path = os.path.join(directory, f"articles_{datetime.datetime.now().strftime('%d_%m_%Y')}.json")
with open(file_path, "w", encoding='utf-8') as f: 
    try:    
        json.dump(article_dict, f, indent=4, ensure_ascii=False)
        print('Статьи были успешно получены')
    except:
        print('Статьи не удалось получить')

def parse_article_page(article_name, article_link):
    parsed_articles = {}
    # for article_name, article_link in article_dict.items():
    try:
        req = requests.get(article_link, headers=headers).text
        soup = BeautifulSoup(req, 'lxml')
        article_content = soup.find('div', class_='article-formatted-body').text.strip()
        parsed_articles[article_name] = article_content

        # author
        try:
            name_author = soup.find("span", class_='tm-user-card__name').text.strip()
            parsed_articles["name_author"] = name_author
        except Exception as e:
            parsed_articles["name_author"] = None
        
        author = soup.find('div', class_='tm-article-presenter__header')
        article_link, datetime_attr = parse_author(author)
        parsed_articles["author_link"] = article_link
        parsed_articles["datetime_attr"] = datetime_attr
    except Exception as e:
        print(f"Ошибка парсинга статьи {article_name}: {str(e)}")
    
    return parsed_articles

def parse_author(author):
    url = author.find('a')
    article_link = f'https://habr.com{url.get("href")}' # ссылки на автора

    datastr = author.find("span", class_='tm-article-datetime-published')
    time_element = datastr.find("time")
    datetime_attr = time_element.get("datetime")  # время статьи
    return article_link, datetime_attr

n = 0
for article_name, article_link in article_dict.items():
    parsed_articles = parse_article_page(article_name, article_link)
    time.sleep(3) 
    n += 1
    file_path = os.path.join(directory, f"{n}_srt_pars_articles.json")
    with open(file_path, "w", encoding='utf-8') as f: 
        try:  
            json.dump(parsed_articles, f, indent=4, ensure_ascii=False)
            print('Статьи были успешно распарсены')
        except:
            print('Статьи не удалось распарсить')

