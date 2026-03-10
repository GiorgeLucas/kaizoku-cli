from rich.text import Text
from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Input

from core.anime import Anime
from scraper.search_manager import SearchManager
from ui.screens.episodes_screen import EpisodesScreen
from ui.widgets.animes.animes_search import AnimeSearchContainer
from ui.widgets.animes.animes_table import AnimesTableContainer

class AnimeScreen(Screen):
    animes_dict = {}

    def compose(self) -> ComposeResult:
        yield AnimeSearchContainer()
        yield AnimesTableContainer()

    def on_input_submitted(self, event: Input.Submitted):
        match event.input.id:
            case "search_input":
                event.input.disabled = True
                self.search_animes(event.value)


    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        anime = self.animes_dict[event.row_key.value]
        self.app.push_screen(EpisodesScreen(anime))


    def update_animes_datatable(self, animes_list: list[Anime]):
        option_list = self.query_one("#animes_list", DataTable)
        self.animes_dict.clear()
        option_list.clear()       
        for anime in animes_list:
            self.animes_dict[anime.title] = anime
            option_list.add_row(
                Text(anime.title, overflow="ellipsis", no_wrap=True), 
                Text(anime.provider.title, style=anime.provider.color), 
                Text(anime.provider.language.lang_name, style=anime.provider.language.lang_color),
                key=anime.title
            )
        self.query_one("#search_input", Input).disabled = False
        self.query_one("#animes_list", DataTable).focus()
        

    @work(exclusive=True, thread=True)
    async def search_animes(self, raw_anime_name: str):
        animes_list = SearchManager.search_anime(raw_anime_name)
        self.app.call_from_thread(self.update_animes_datatable, animes_list)       

