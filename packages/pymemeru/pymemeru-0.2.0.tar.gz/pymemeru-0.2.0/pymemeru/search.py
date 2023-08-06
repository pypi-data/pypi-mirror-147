from bs4 import BeautifulSoup

from .models import Search, SearchResult
from .aioget import aioget


async def search(query: str) -> list[SearchResult]:
    page = await aioget("https://memepedia.ru", {"s": query})
    soup = BeautifulSoup(page, "lxml")

    ul = soup.find("ul", {"class": "post-items"})
    results = []

    for li in ul.find_all("li"):
        article = li.find("article")
        content = article.find_all("div", {"class": "content"})[0]

        results.append({
            "title": content.header.h2.a.text,
            "name": content.header.h2.a["href"][21:-1]
        })

    return Search.parse_obj(results).__root__
