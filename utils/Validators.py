# utils/Validators.py

import re
import os
from pathlib import Path

class Validators:
    # matches 25-12345678 or 2025-12345678-Jones etc.
    CASE_ID_PATTERN = re.compile(r'^(?:\d{2}|\d{4})-\d{1,8}(?:-[A-Za-z0-9_]+)?$')

    @staticmethod
    def is_valid_case_id(case_id: str) -> bool:
        """True if case_id matches YY‑ or YYYY‑ + up to 8 digits + optional suffix."""
        return bool(Validators.CASE_ID_PATTERN.fullmatch(case_id))

    @staticmethod
    def default_case_root() -> Path:
        """
        Returns the default folder for cases:
          • Windows: %USERPROFILE%\\Documents\\case-maker
          • Other OS: $HOME/Documents/case-maker
        """
        home = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME", ""))
        documents = home / "Documents"
        return (documents / "case-maker").expanduser()
