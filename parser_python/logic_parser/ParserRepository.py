import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from db.database import save_database


ua = UserAgent()

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}

async def fetch_page(session, url):
    """
    Fetching the page
    """
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def parse_home_page(html):
    """
    Parsing the main page
    """
    soup = BeautifulSoup(html, 'lxml')
    article_dict = {}
    all_hrefs_articles = soup.find_all('a', class_='tm-title__link')
    for article in all_hrefs_articles:
        article_name = article.find('span').text
        article_link = f'https://habr.com{article.get("href")}'
        article_dict[article_name] = article_link
    return article_dict

async def parse_article_page(session, article_name, article_link):
    """
    Parsing the article
    """
    html = await fetch_page(session, article_link)
    soup = BeautifulSoup(html, 'lxml')
    parsed_articles = {}
    try:
        article_content = soup.find('div', class_='article-formatted-body').text.strip()
        parsed_articles[article_name] = article_content
        parsed_articles["article_link"] = article_link

        # Checking the author's name
        try:
            full_name_author = soup.find("span", class_='tm-user-card__name').text.strip()
            parsed_articles["full_name_author"] = full_name_author
        except Exception as e:
            parsed_articles["full_name_author"] = None

        # Parsing information about the author
        author = soup.find('div', class_='tm-article-presenter__header')
        author_name, author_link, datetime_attr = await parse_author(author)

        parsed_articles["author_link"] = author_link
        parsed_articles["datetime_attr"] = datetime_attr
        parsed_articles["name_author"] = author_name
    except Exception as e:
        print(f"Ошибка парсинга статьи {article_name}: {str(e)}")
    return parsed_articles

async def parse_author(author):
    """
    Parsing information about the author
    """
    block_url = author.find('a')
    author_name = block_url.get('title')
    article_link = f'https://habr.com{block_url.get("href")}'
    datastr = author.find("span", class_='tm-article-datetime-published')
    time_element = datastr.find("time")
    datetime_attr = time_element.get("datetime")
    return author_name, article_link, datetime_attr

async def parser_logic(url):
    """
    Logic with calls to auxiliary functions for page parsing, returning the result of parsing all pages
    """
    async with aiohttp.ClientSession() as session:
        html = await fetch_page(session, url)
        article_dict = await parse_home_page(html)
        tasks = []
        for article_name, article_link in article_dict.items():
            task = asyncio.create_task(parse_article_page(session, article_name, article_link))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

async def parser_run():
    """
    Launching the parser and sending the result for saving
    """
    url = 'https://habr.com/ru/articles/'
    results = await parser_logic(url)
    save_database(results)  # Saving data to a database
