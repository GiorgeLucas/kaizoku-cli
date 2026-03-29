from abc import ABC, abstractmethod
from enum import Enum

from kaizoku.core.anime import Anime, Episode

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


class Language(Enum):
    PT_BR = ("pt-BR", "Portuguese", "#089F41 bold")
    EN_US = ("en-US", "English", "#00205B bold")

    def __init__(self, lang_code: str, lang_name: str, lang_color: str):
        self.lang_code = lang_code
        self.lang_name = lang_name
        self.lang_color = lang_color


class BaseProvider(ABC):
    title: str
    color: str
    base_url: str
    language: Language

    @abstractmethod
    def search_anime(self, anime_name: str) -> list[Anime]:
        pass

    @abstractmethod
    def search_episodes(self, anime: Anime) -> list[Episode]:
        pass

    @abstractmethod
    def get_play_options(self, episode: Episode) -> dict[str, str]:
        pass
