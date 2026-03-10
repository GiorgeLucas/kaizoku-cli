from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import DataTable
from ui.utils import BG_COLOR, FG_COLORS

class AnimeslistContainer(Vertical):
    BORDER_TITLE = "Animes List"
    DEFAULT_CSS = f"""
        AnimeslistContainer {{
            background: transparent;
            border: round {FG_COLORS[10]};
        }}

        #animes_list {{
            background: transparent;
            scrollbar-visibility: hidden;
        }}

        #animes_list > .datatable--header {{
            color: {FG_COLORS[2]};
            background: transparent;
        }}

        #animes_list > .datatable--header-hover {{
            color: {BG_COLOR};
            background: {FG_COLORS[2]};
        }}

        #animes_list > .datatable--cursor {{
            color: {BG_COLOR};
            background: {FG_COLORS[5]};
        }}
    """

    def compose(self) -> ComposeResult:
        yield DataTable(id="animes_list")

    def on_mount(self) -> None:
        table = self.query_one("#animes_list", DataTable)
        columns = [
            ("Name", self.app.size.width - 16 - 13 - 10),
            ("Provider", 16),
            ("Language", 13)
        ]
        for label, width in columns:
            table.add_column(label, width=width)


