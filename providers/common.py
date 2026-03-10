from enum import Enum

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

class Language(Enum):
    PT_BR = ("pt-BR", "Portuguese", "#089F41 bold")
    EN_US = ("en-US", "English"   , "#00205B bold")

    def __init__(self, lang_code: str, lang_name: str, lang_color: str):
        self.lang_code = lang_code
        self.lang_name = lang_name
        self.lang_color = lang_color
