from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    name: str


class Search(BaseModel):
    __root__: list[SearchResult]
