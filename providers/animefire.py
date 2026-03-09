from typing import Any, Union

from bs4 import BeautifulSoup
import requests

from core.anime import Anime, Episode
from providers.base_provider import BaseProvider
from providers.common import Language
from providers.exceptions import ExceptionSearchingNetworkError

from .common import headers

import re

class Animefire(BaseProvider):
    title = "Animefire"
    color = "fg:#21D3FF bold"
    base_url = "https://animefire.io"
    language = Language.PT_BR

    def parse_anime_name(self, raw_anime_name: str):
        parsed = re.sub(r'[^a-zA-Z0-9]+', '-', raw_anime_name).lower().strip("-")
        return parsed

    def get_episode_video_url(self, episode: Episode) -> Union[dict[str, Any], None]:
        page_link = episode.page_link
        response = requests.get(page_link, headers=headers)
        if response.status_code != 200:
            raise  ExceptionSearchingNetworkError("episode video url", episode.anime.title, self.title)
        soup = BeautifulSoup(response.text, "html.parser")
        video = soup.find("video")
        if video is not None:
            metadata = video.get("data-video-src")
            response = requests.get(str(metadata), headers=headers)
            data = response.json()
            data = data["data"]
            return {  option["label"]: option["src"] for option in data }

    def get_episodes_list(self, anime: Anime) -> list[Episode]:
        page_link = anime.page_link
        response = requests.get(page_link, headers=headers)
        if response.status_code != 200:
            raise  ExceptionSearchingNetworkError("episodes list", anime.title, self.title)
        soup = BeautifulSoup(response.text, "html.parser")
        episodes_links = soup.select(".div_video_list > a")
        if len(episodes_links) == 0:
            return []
        episodes_list = []
        if episodes_links is not None:
            for episode in episodes_links:
                episode_title = episode.getText()
                episode_link = str(episode.get("href"))
                episodes_list.append(Episode(episode_title, anime, episode_link))
        return episodes_list

    def search_anime(self, raw_anime_name: str) -> list[Anime]:
        parsed_anime_name = self.parse_anime_name(raw_anime_name)
        search_url = f"{self.base_url}/pesquisar/{parsed_anime_name}"
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            raise ExceptionSearchingNetworkError("search result", raw_anime_name, self.title)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div",attrs={"title": True})
        animes = []
        if results is not None:
            for result in results:
                anime_title = str(result.get("title"))
                element_link = result.find("a")
                homepage_link = str(element_link.get("href")) if element_link else ""
                animes.append(Anime(anime_title, homepage_link, self))
        return animes




