from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Label

from core.anime import Episode

class EpisodesInfoContainer(Container):
    BORDER_TITLE = "Aditional Information"
    
    can_focus = False

    episode = reactive(None)

    def compose(self) -> ComposeResult:
        yield Label("", id="anime-title")
        yield Label("", id="episode-title")
        yield Label("", id="provider")

    def on_mount(self):
        self.styles.height = 5
        self.styles.padding = (0, 1)

    def watch_episode(self, episode: Episode):
        if episode is not None:
            selected_anime_text = Text("Selected anime: ")
            selected_anime_text.append(episode.anime.title, style="magenta bold")
            self.query_one("#anime-title", Label).update(selected_anime_text)

            selected_episode_text = Text("Selected episode: ")
            selected_episode_text.append(episode.title, style="magenta bold")
            self.query_one("#episode-title", Label).update(selected_episode_text)

            provider_text = Text("Provider: ")
            provider_text.append(episode.anime.provider.title, style=episode.anime.provider.color)
            self.query_one("#provider", Label).update(provider_text)



    
