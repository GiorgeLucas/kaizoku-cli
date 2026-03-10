from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import DataTable


class AnimesTableContainer(Container):
    BORDER_TITLE = "Anime List"

    DEFAULT_CSS = """
        #animes_list > .datatable--hover {
            background: ansi_white;
            color: ansi_black;
        }
    """

    def compose(self) -> ComposeResult:
        yield DataTable(id="animes_list", cursor_type="row")

    def on_mount(self) -> None:
        table = self.query_one("#animes_list", DataTable)
        columns = [
            ("Name", self.app.size.width - 16 - 13 - 10),
            ("Provider", 16),
            ("Language", 13)
        ]
        for label, width in columns:
            table.add_column(label, width=width)
