import re
from typing import cast

import requests
from bs4 import BeautifulSoup

from kaizoku.core import Anime, Episode
from kaizoku.providers.common import BaseProvider, Language, headers


class Animefire(BaseProvider):
    title = "Animefire"
    color = "#21D3FF bold"
    base_url = "https://animefire.io"
    language = Language.PT_BR

    def search_anime(self, anime_name: str) -> list[Anime]:
        response_text = self._fetch_anime_results_html(anime_name)
        return self._parse_animes_from_html(response_text)

    def _fetch_anime_results_html(self, anime_name: str) -> str:
        parsed_anime_name = self._parse_anime_name(anime_name)
        search_url = f"{self.base_url}/pesquisar/{parsed_anime_name}"
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        return response.text

    def _parse_anime_name(self, raw_anime_name: str) -> str:
        parsed = re.sub(r"[^a-zA-Z0-9]+", "-", raw_anime_name).lower().strip("-")
        return parsed

    def _parse_animes_from_html(self, html: str) -> list[Anime]:
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.find_all("div", attrs={"title": True})
        return [self._map_element_to_anime(el) for el in elements]

    def _map_element_to_anime(self, element) -> Anime:
        anime_title = str(element.get("title"))
        link_tag = element.find("a")
        link = str(link_tag.get("href")) if link_tag else ""
        return Anime(anime_title, link, self)

    def search_episodes(self, anime: Anime) -> list[Episode]:
        response_text = self._fetch_episodes_results_html(anime)
        return self._parse_episodes_from_html(response_text, anime)

    def _fetch_episodes_results_html(self, anime: Anime) -> str:
        response = requests.get(anime.page_link, headers=headers)
        response.raise_for_status()
        return response.text

    def _parse_episodes_from_html(self, html: str, anime: Anime) -> list[Episode]:
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.select(".div_video_list > a")
        return [self._map_element_to_episode(anime, el) for el in elements]

    def _map_element_to_episode(self, anime: Anime, element) -> Episode:
        episode_title = element.getText()
        episode_link = str(element.get("href"))
        return Episode(episode_title, anime, episode_link)

    def get_play_options(self, episode: Episode) -> dict[str, str]:
        response_text = self._fetch_episode_page_html(episode)
        return self._parse_play_options_from_html(response_text)

    def _fetch_episode_page_html(self, episode: Episode) -> str:
        page_link = episode.page_link
        response = requests.get(page_link, headers=headers)
        response.raise_for_status()
        return response.text

    def _parse_play_options_from_html(self, html: str) -> dict[str, str]:
        soup = BeautifulSoup(html, "html.parser")
        video = soup.find("video")
        if video is None:
            return {}
        metadata = video.get("data-video-src")
        if metadata is None:
            return {}
        return self._fetch_episode_play_options(str(metadata))

    def _fetch_episode_play_options(self, metadata: str) -> dict[str, str]:
        response = requests.get(metadata, headers=headers)
        response.raise_for_status()
        data = response.json()
        data = cast(list[dict[str, str]], data["data"])
        return {option_dict["label"]: option_dict["src"] for option_dict in data}
