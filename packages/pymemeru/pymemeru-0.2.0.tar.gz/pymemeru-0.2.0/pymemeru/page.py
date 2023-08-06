from bs4 import BeautifulSoup

from .models import Page, Trending
from .aioget import aioget


async def page(name: str) -> Page:
    page = await aioget(f"https://memepedia.ru/{name}/")

    soup = BeautifulSoup(page, "lxml")
    post = soup.find_all(class_="s-post-main")[0]

    try:
        image = post.find_all("figure", class_="post-thumbnail", recursive=True)[0].img["src"]
    except:
        image = post.find_all("div", class_="bb-media-placeholder")[0].img["src"]

    try:
        trending_ = soup.find_all(class_="widget_trending_entries")[0].ul
    except:
        trending_ = []

    try:
        comments = (
            soup.find_all("a", class_="post-comments")[0]
                .find_all("span", class_="count")[0].text
        )
    except:
        comments = 0

    return Page(
        title=post.h1.text,
        published_at=post.find_all("time", class_="published")[0].text,

        author_name=(
            soup.find_all("div", class_="author-info")[0]
                .find_all("a", class_="auth-url")[0]
                .span.text
        ),

        views=(
            soup.find_all("span", class_="post-views")[0]
                .find_all("span", class_="count")[0].text
        ),
        comments=comments,

        main_image=image,

        text=str(post),
        trending=[Trending(
            preview=trending.find_all("img")[0]["src"],
            title=trending.find_all(class_="content")[0].find_all("a")[0].text,
            url="/" + trending.find_all(class_="content")[0].find_all("a")[0]["href"].split("/")[-2]
        ) for trending in trending_]
    )

