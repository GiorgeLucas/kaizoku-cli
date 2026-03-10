import re
from typing import Any, Union
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup
import requests

from core.anime import Anime, Episode
from providers.base_provider import BaseProvider
from providers.common import Language

from .common import headers
from .exceptions import ExceptionSearchingNetworkError


class AnimesDigital(BaseProvider):
    title = "Animes Digital"
    color = "#ff4545 bold"
    base_url = "https://animesdigital.org"
    language = Language.PT_BR

    def parse_anime_name(self, raw_anime_name: str):
        parsed = re.sub(r'[^a-zA-Z0-9]+', '+', raw_anime_name)
        return parsed

    def get_episode_video_url(self, episode: Episode) -> Union[dict[str, Any], None]:
        page_link = episode.page_link
        response = requests.get(page_link, headers=headers)
        if response.status_code != 200:
            raise  ExceptionSearchingNetworkError("episode video url", episode.anime.title, self.title)
        soup = BeautifulSoup(response.text, "html.parser")
        iframe = soup.select("#player1 > iframe")[0]
        if iframe is not None:
            iframe_src = iframe.get("src")
            parsed_url = urlparse(str(iframe_src))
            parsed_query = parse_qs(parsed_url.query)
            return  { "1080p": str(parsed_query['d'][0]) } 

    def get_episodes_list(self, anime: Anime, page: int = 1, episodes_list: Union[list[Episode], None] = None) -> list[Episode]:
        if episodes_list is None:
            episodes_list = []
        page_link = f"{anime.page_link}/" + "?odr=1" if page == 1 else f"{anime.page_link}/page/{page}/?odr=1"
        response = requests.get(page_link, headers=headers)

        if response.status_code != 200:
            raise  ExceptionSearchingNetworkError("episodes list", anime.title, self.title)

        soup = BeautifulSoup(response.text, "html.parser")

        episodes_links = soup.select(".item_ep.b_flex > a")
        if len(episodes_links) == 0:
            return []
        if episodes_links is not None:
            for episode in episodes_links:
                episode_title = episode.select(".title_anime")[0].get_text()
                episode_link = str(episode.get("href"))
                episodes_list.append(Episode(episode_title, anime, episode_link))

        pages_links = soup.select(".content-pagination.b_flex.b_wrap > li > a")
        if len(pages_links) > 0:
            total_pages = int(pages_links[-2].get_text())
            if page < total_pages:
                return self.get_episodes_list(anime, page + 1, episodes_list)

        return episodes_list

    def search_anime(self, raw_anime_name: str) -> list[Anime]:
        parsed_anime_name = self.parse_anime_name(raw_anime_name)
        search_url = f"{self.base_url}/search/{parsed_anime_name}"
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            raise ExceptionSearchingNetworkError("search result", raw_anime_name, self.title)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".itemA > a")
        animes = []
        if results is not None:
            for result in results:
                anime_title = str(result.get("title")).replace("Assistir ", "").replace(" Online em HD", "")
                homepage_link = str(result.get("href"))
                response = requests.get(homepage_link, headers=headers)
                resolved_homepage_url = response.url
                animes.append(Anime(anime_title, resolved_homepage_url, self))
        return animes
