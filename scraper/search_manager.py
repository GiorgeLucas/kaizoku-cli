from typing import Any, Union
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.anime import Anime, Episode
from providers.animefire import Animefire
from providers.animesdigital import AnimesDigital
from providers.base_provider import BaseProvider

class SearchManager:
    providers: list[BaseProvider] = [Animefire(), AnimesDigital()]

    @staticmethod
    def search_anime(raw_anime_name: str) -> list[Anime]:
        animes_list: list[Anime] = []
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(provider.search_anime, raw_anime_name): provider for provider in SearchManager.providers
            }
            for future in as_completed(futures):
                try:
                    provider_name_results = future.result()
                    animes_list.extend(provider_name_results)
                except Exception as e:
                    print(f"Error searching with provider {futures[future].title}: {e}")
        return animes_list


    @staticmethod
    def get_episodes_list(anime: Anime) -> list[Episode]:
        episodes_list = anime.provider.get_episodes_list(anime)
        return episodes_list

    @staticmethod
    def get_episode_url(episode: Episode) -> Union[dict[str, Any], None]:
        episode_url = episode.anime.provider.get_episode_video_url(episode)
        return episode_url




    



        
        
