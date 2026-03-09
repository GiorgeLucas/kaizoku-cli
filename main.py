import subprocess

import questionary

from core.anime import Anime
from scraper.search_manager import SearchManager
from utils.system import clear

def no_animes_found():
    print("No animes found!")
    questionary.press_any_key_to_continue().ask()


def episode_not_working():
    print("This episode from this provider is not working. Try another one")
    questionary.press_any_key_to_continue().ask()

def no_episodes_list():
    print("This anime doesnt have episodes list. Try another one")
    questionary.press_any_key_to_continue().ask()


def get_pretty_anime_label(anime: Anime):
    label = [
        (anime.provider.language.lang_color, f"({anime.provider.language.lang_code}) "),
        (anime.provider.color, f"({anime.provider.title}) "),
        ("", f"{anime.title}")
    ]
    return label 

def search_and_select_anime():
    anime_name = questionary.text("Enter an anime name: ").ask()
    animes_list = SearchManager.search_anime(anime_name)

    if not animes_list:
        no_animes_found()
        return None

    anime_dict = {
        f"{anime.title}": {"provider": anime.provider, "anime": anime}
        for anime in animes_list
    }

    def make_choice(key):
        data = anime_dict[key]
        label = get_pretty_anime_label(data["anime"])
        return questionary.Choice(title=label, value=key)

    choices = [questionary.Choice(title="[GO BACK]", value="__back__")] + [ make_choice(key) for key in anime_dict ]

    selected_key = questionary.select("Select an anime from the list: ", choices=choices).ask()

    if selected_key == "__back__":
        return None

    return anime_dict[selected_key]["anime"]


def select_episode(anime):
    episodes_list = SearchManager.get_episodes_list(anime)

    if episodes_list == []:
        no_episodes_list()
        return None

    episodes_dict = {episode.title: episode for episode in episodes_list}

    selected_title = questionary.select(
        "Select an episode from the list: ",
        choices=list(episodes_dict.keys()),
        use_search_filter=True,
        use_jk_keys=False
    ).ask()

    return episodes_dict[selected_title]


def handle_playback(final_url):
    action = questionary.select("What do you want to do? ", ["Download it", "Watch it"]).ask()

    if action == "Download it":
        print("Not implemented yet :/")
        return

    if isinstance(final_url, dict):
        selected_quality = questionary.select("Choose a quality: ", choices=list(final_url.keys())).ask()
        final_url = str(final_url[selected_quality])

    subprocess.run(["mpv", final_url])


def main():
    while True:
        clear()

        anime = search_and_select_anime()
        if anime is None:
            continue

        episode = select_episode(anime)
        if(episode is None):
            continue

        clear()
        print(f"Selected Anime: {anime.title}")
        print(f"Selected Episode: {episode.title}")

        final_url = SearchManager.get_episode_url(episode)
        if final_url is not None:
            handle_playback(final_url)
        else:
            episode_not_working()


if __name__ == "__main__":
    main()
