from bs4 import BeautifulSoup
import random
import json
import requests
import datetime
from fake_useragent import UserAgent


ua = UserAgent()


headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}


article_dict = {}


# url = f'https://habr.com/ru/top/daily/'
url = f'https://habr.com/ru/articles/'


req = requests.get(url, headers=headers).text


soup = BeautifulSoup(req, 'lxml')
all_hrefs_articles = soup.find_all('a', class_='tm-title__link') # получаем статьи


for article in all_hrefs_articles: # проходимся по статьям
    article_name = article.find('span').text # собираем названия статей
    article_link = f'https://habr.com{article.get("href")}' # ссылки на статьи
    article_dict[article_name] = article_link


def parse_article_page(article_dict):
    parsed_articles = {}
    for article_name, article_link in article_dict.items():
        try:
            req = requests.get(article_link, headers=headers).text
            soup = BeautifulSoup(req, 'lxml')
            article_content = soup.find('div', class_='article-formatted-body').text.strip()
            parsed_articles[article_name] = article_content
        except Exception as e:
            print(f"Ошибка парсинга статьи {article_name}: {str(e)}")
    return parsed_articles


parsed_articles = parse_article_page(article_dict)


with open(f"parsed_articles_{datetime.datetime.now().strftime('%d_%m_%Y')}.json", "w", encoding='utf-8') as f: 
    try:  
        json.dump(parsed_articles, f, indent=4, ensure_ascii=False)
        print('Статьи были успешно распарсены')
    except:
        print('Статьи не удалось распарсить')
# ---------------------------------------------------
# from bs4 import BeautifulSoup
# import random
# import json
# import requests
# import datetime
# from fake_useragent import UserAgent

# ua = UserAgent()

# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'user-Agent': ua.google,
# }

# article_dict = {}

# # url = f'https://habr.com/ru/top/daily/'
# url = f'https://habr.com/ru/articles/'

# req = requests.get(url, headers=headers).text

# soup = BeautifulSoup(req, 'lxml')
# all_hrefs_articles = soup.find_all('a', class_='tm-title__link') # получаем статьи

# for article in all_hrefs_articles: # проходимся по статьям
#     article_name = article.find('span').text # собираем названия статей
#     article_link = f'https://habr.com{article.get("href")}' # ссылки на статьи
#     article_dict[article_name] = article_link


# with open(f"articles_{datetime.datetime.now().strftime('%d_%m_%Y')}.json", "w", encoding='utf-8') as f: 
#     try:    
#         json.dump(article_dict, f, indent=4, ensure_ascii=False)
#         print('Статьи были успешно получены')
#     except:
#         print('Статьи не удалось получить')
# ------------------------------------------------------------------
# from bs4 import BeautifulSoup
# import random
# import json
# import requests
# import datetime
# from fake_useragent import UserAgent

# ua = UserAgent()

# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'user-Agent': ua.google,
# }

# article_dict = {}
# article_content_dict = {}

# url = f'https://habr.com/ru/articles/'

# req = requests.get(url, headers=headers).text

# soup = BeautifulSoup(req, 'lxml')
# all_hrefs_articles = soup.find_all('a', class_='tm-title__link')  # получаем статьи

# for article in all_hrefs_articles:  # проходимся по статьям
#     article_name = article.find('span').text  # собираем названия статей
#     article_link = f'https://habr.com{article.get("href")}'  # ссылки на статьи
#     article_dict[article_name] = article_link

#     # делаем запрос на статью по ссылке
#     article_req = requests.get(article_link, headers=headers).text
#     article_soup = BeautifulSoup(article_req, 'lxml')

#     # парсим содержимое статьи
#     article_content = article_soup.find('div', class_='post__text').text.strip()
#     article_content_dict[article_name] = article_content

# with open(f"articles_{datetime.datetime.now().strftime('%d_%m_%Y')}.json", "w", encoding='utf-8') as f:
#     try:
#         json.dump(article_dict, f, indent=4, ensure_ascii=False)
#         print('Статьи были успешно получены')
#     except:
#         print('Статьи не удалось получить')

# with open(f"new_article_content_{datetime.datetime.now().strftime('%d_%m_%Y')}.json", "w", encoding='utf-8') as f:
#     try:
#         json.dump(article_content_dict, f, indent=4, ensure_ascii=False)
#         print('Содержимое статей было успешно получено')
#     except:
#         print('Содержимое статей не удалось получить')