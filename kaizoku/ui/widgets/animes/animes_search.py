from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Input

class AnimeSearchContainer(Container):
    BORDER_TITLE = "Anime Search"
    DEFAULT_CSS = f"""
        AnimeSearchContainer {{
          padding: 0 2;
          height: 3;
        }}

        #search_input {{
          background: transparent;
          color: ansi_white;
          padding: 0;
          border: none;
          height: 1;
        }}
    """

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter an anime name", id="search_input")



