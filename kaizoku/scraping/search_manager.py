from kaizoku.core.anime import Anime, Episode
from kaizoku.providers.animefire import Animefire
from kaizoku.providers.common import BaseProvider


class SearchManager:
    providers: list[BaseProvider] = [Animefire()]

    @staticmethod
    def search_anime(raw_anime_name: str) -> list[Anime]:
        animes_list: list[Anime] = []
        for provider in SearchManager.providers:
            provider_anime_results = provider.search_anime(raw_anime_name)
            for provider_anime in provider_anime_results:
                animes_list.append(provider_anime)
        return animes_list

    @staticmethod
    def search_episodes(anime: Anime) -> list[Episode]:
        episodes_list = anime.provider.search_episodes(anime)
        return episodes_list

    @staticmethod
    def get_play_options(episode: Episode) -> dict[str, str] | None:
        episode_url = episode.anime.provider.get_play_options(episode)
        return episode_url
