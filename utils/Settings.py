import json
import os
from pathlib import Path
from utils.Validators import Validators

class Settings:
    """
    Application settings for Case Manager. Stored in a JSON file in the user's profile.
    """
    CONFIG_FILENAME = ".case_manager_settings.json"

    def __init__(self):
        # Default values
        self.case_root = str(Validators.default_case_root())
        self.theme = "light"              # or "dark"
        self.auto_index = True             # File indexing on launch
        self.integrity_on_open = True      # Check integrity when opening a case

        # Load stored settings (if present)
        self._load()

    @property
    def config_path(self) -> Path:
        # Windows: %APPDATA%  Other: $HOME
        base = Path(os.environ.get("APPDATA") or os.environ.get("HOME"))
        return base / self.CONFIG_FILENAME

    def _load(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.case_root = data.get("case_root", self.case_root)
                self.theme = data.get("theme", self.theme)
                self.auto_index = data.get("auto_index", self.auto_index)
                self.integrity_on_open = data.get("integrity_on_open", self.integrity_on_open)
            except Exception:
                # If loading fails, stick with defaults
                pass

    def save(self):
        data = {
            "case_root": self.case_root,
            "theme": self.theme,
            "auto_index": self.auto_index,
            "integrity_on_open": self.integrity_on_open,
        }
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            # Could add logging here
            pass

# Usage:
# settings = Settings()
# settings.case_root -> current base folder
# settings.save()   -> persist changes
