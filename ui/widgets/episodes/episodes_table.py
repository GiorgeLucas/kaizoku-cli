from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Vertical, VerticalScroll
from textual.widgets import DataTable, Input, Label

class EpisodesTableContainer(Vertical):
    BORDER_TITLE = "Episodes List"

    DEFAULT_CSS = """
        #search_header {
            height: 3;
            padding: 0;
            border: none;
        }

        #episode_search {
            padding: 0 1;
            height: 1;
        }

        #episodes_list > .datatable--hover {
            background: ansi_white;
            color: ansi_black;
        }
    """

    def compose(self) -> ComposeResult:
        with Horizontal(id="search_header"):
            yield Label("Search:", id="episode_search_prefix")
            yield Input(
                placeholder="Enter an episode number", 
                id="episode_search",
                select_on_focus=False
            )
        with VerticalScroll(can_focus=False):
            yield DataTable(id="episodes_list", cursor_type="row")

    def on_mount(self):
        self.query_one("#episodes_list", DataTable).add_column("Name")
