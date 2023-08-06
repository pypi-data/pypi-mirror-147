from pydantic import BaseModel
from bs4 import BeautifulSoup


class Trending(BaseModel):
    preview: str
    title: str
    url: str

    views: str = 0


class Page(BaseModel):
    title: str
    published_at: str

    views: str
    comments: str

    author_name: str

    main_image: str
    text: str
    trending: list[Trending]

    @property
    def cleared_text(self) -> BeautifulSoup:
        soup = BeautifulSoup(self.text)

        for tag in [
            *soup.find_all("time"),
            *soup.find_all("img", class_=["avatar"]),
            *soup.find_all("span", class_=["count"]),
            *soup.find_all("span", itemprop="name"),
            *soup.find_all("div", class_=["mistape_caption", "share-box"]),
            *soup.find_all("h1"),
            *soup.find_all("hr"),
            *soup.find_all("figure", class_="bb-mb-el")
        ]:
            tag.replace_with("")

        for tag in soup.find_all("div", class_="su-quote-inner"):
            tag.name = "blockquote"

        for tag in soup.find_all("span", class_="su-quote-cite"):
            tag.name = "cite"

        for tag in soup.find_all("a"):
            if tag["href"] == "https://t.me/memepedia_Ru":
                tag.replace_with("")

        for tag in soup.find_all("a"):
            if tag["href"].startswith("https://memepedia.ru/"):
                tag["href"] = "/memepedia/" + tag["href"].removeprefix("https://memepedia.ru/")

        return soup
