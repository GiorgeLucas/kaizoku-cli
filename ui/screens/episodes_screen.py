import subprocess
from typing import Any, Union
from rich.text import Text
from textual.containers import Container, Vertical
from scraper.search_manager import SearchManager
from textual import events, work
from textual.app import ComposeResult
from textual.screen import ModalScreen, Screen
from textual.widgets import DataTable, Input, LoadingIndicator, OptionList

from core.anime import Anime, Episode
from ui.widgets.episodes.episodes_info import EpisodesInfoContainer
from ui.widgets.episodes.episodes_table import EpisodesTableContainer

class EpisodeQualityModal(ModalScreen[str]):
    BINDINGS = [("escape", "dismiss(None)", "Close")]
    options: list

    def __init__(self, options):
        super().__init__()
        self.options = options

    def compose(self) -> ComposeResult:
        yield OptionList(*self.options)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self.dismiss(str(event.option.prompt))



class EpisodesScreen(Screen):   
    BINDINGS = [("escape", "app.pop_screen()", "Back")]
    anime: Anime
    filtered_episodes = {}
    episodes_dict = {}

    def __init__(self, anime: Anime):
        super().__init__()
        self.anime = anime

    def compose(self) -> ComposeResult:
        yield LoadingIndicator()
        yield EpisodesInfoContainer(id="info-container")
        yield EpisodesTableContainer()

    def on_mount(self):
        self.get_episodes(self.anime)


    def on_key(self, event: events.Key):
        if event.key in ("up", "down"):
            self.query_one("#episodes_list", DataTable).focus()
            event.prevent_default()

    def on_input_changed(self, event: Input.Changed):
        value = event.value.strip()
        table = self.query_one("#episodes_list", DataTable)
        table.clear()
        self.filtered_episodes.clear()

        source = self.episodes_dict if not value else {
            k: v for k, v in self.episodes_dict.items()
            if value.lower() in v.title.lower() or value in str(k + 1) 
        }

        for new_key, (_, episode) in enumerate(source.items()):
            self.filtered_episodes[new_key] = episode
            table.add_row(
                Text(episode.title, overflow="ellipsis", no_wrap=True),
                key=str(new_key)
            )

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        if event.row_key.value is not None:
            key = int(event.row_key.value)
            source = self.filtered_episodes if self.filtered_episodes else self.episodes_dict
            episode = source[key]
            self.get_episode_url(episode)

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted):
        if event.row_key.value is not None:
            key = int(event.row_key.value)
            source = self.filtered_episodes if self.filtered_episodes else self.episodes_dict
            if key in source:
                episode = source[key]
                self.query_one("#info-container", EpisodesInfoContainer).episode = episode

    def update_episodes_datatable(self, episodes_list: list[Episode]):
        option_list = self.query_one("#episodes_list", DataTable)
        for i, episode in enumerate(episodes_list):
            key = i
            self.episodes_dict[key] = episode
            option_list.add_row(
                Text(episode.title, overflow="ellipsis", no_wrap=True),
                key=str(key)
            )
        self.query_one("LoadingIndicator").display = False

    def handle_episode_play(self, episode_url: Union[dict[str, Any], None]):
        if episode_url is not None:
            qualities = episode_url.keys()
            def open_mpv(quality: str | None) -> None:
                if quality is not None:
                    self.exec_mpv(episode_url[quality])
            self.app.push_screen(EpisodeQualityModal(qualities), open_mpv)


    @work(thread=True)
    async def exec_mpv(self, url: str):
        subprocess.Popen(
            ["mpv", url], 
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    @work(exclusive=True, thread=True)
    async def get_episodes(self, anime: Anime):
        episodes_list = SearchManager.get_episodes_list(anime)
        self.app.call_from_thread(self.update_episodes_datatable, episodes_list)       

    @work(exclusive=True, thread=True)
    async def get_episode_url(self, episode: Episode) -> Union[dict[str, Any], None]:
        episode_url = SearchManager.get_episode_url(episode)
        self.app.call_from_thread(self.handle_episode_play, episode_url)   

