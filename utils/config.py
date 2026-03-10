import json
import os
from pathlib import Path
from typing import Union

DEFAULT_DATA_DIR = Path(
    os.environ.get("XDG_DATA_HOME", Path.home() / "Videos")
) / "kaizoku-cli"

CONFIG_FILE = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "kaizoku-cli" / "config.json"

def get_download_dir(raw_anime_name: Union[str, None] = None, episode: Union[int, None] = None):
    if CONFIG_FILE.exists():
        config = json.load(open(CONFIG_FILE, encoding="utf-8"))
        base_path = Path(config.get("download_path", DEFAULT_DATA_DIR))
    else:
        base_path = DEFAULT_DATA_DIR    

    if raw_anime_name:
        base_path = base_path / raw_anime_name
        if episode is not None:
            base_path = base_path / f"Episode {episode}"

    base_path.mkdir(parents=True, exist_ok=True)
    return base_path

