from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from providers.common import BaseProvider


class Anime:
    title: str
    page_link: str
    provider: BaseProvider

    def __init__(self, title: str, page_link: str, provider: BaseProvider):
        self.title = title
        self.page_link = page_link
        self.provider = provider


class Episode:
    title: str
    anime: Anime
    page_link: str

    def __init__(self, title: str, anime: Anime, page_link: str):
        self.title = title
        self.page_link = page_link
        self.anime = anime
