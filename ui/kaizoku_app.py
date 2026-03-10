from textual.app import App
from ui.screens.anime_screen import AnimeScreen

class KaizokuApp(App):
    TITLE = "Kaizoku-cli"
    CSS = f"""
        Screen {{
            background: transparent;
        }}

        Vertical, Horizontal, Container {{
            background: transparent;
            border: round ansi_green;
        }}

        DataTable {{
            scrollbar-visibility: hidden;
            background: transparent;
        }}

        .datatable--header {{
            background: transparent;
            color: ansi_magenta;
        }}

        .datatable--header-hover {{
            background: ansi_magenta;
            color: ansi_black;
        }}

        .datatable--cursor {{
            background: ansi_magenta;
            color: ansi_black;
        }}

        Input {{
            background: transparent;
            color: ansi_white;
            border: none;
        }}

        Input:disabled {{
            background: transparent;
            opacity: 100%;
        }}
    """

    def on_mount(self):
        self.push_screen(AnimeScreen())


    
