from bs4 import BeautifulSoup

from .models import Trending
from .aioget import aioget


async def popular() -> list[Trending]:
    page = await aioget(f"https://memepedia.ru/memoteka/")

    soup = BeautifulSoup(page, "lxml")

    return [Trending(
        preview=trending.find_all("img")[0]["src"],
        title=trending.find_all(class_="entry-title")[0].find_all("a")[0].text,
        url="/" + trending.find_all(class_="entry-title")[0].find_all("a")[0]["href"].split("/")[-2],
        views=(
            trending.find_all("span", class_="post-views")[0]
                    .find_all("span", class_="count")[0].text
        )
    ) for trending in [
        *soup.find_all(class_="post-item"),
    ]]

