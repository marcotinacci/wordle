import os
import logging
from typing import Final
from pathlib import Path

SYMBOL_MATCH: Final = "X"
SYMBOL_MISPLACED: Final = "."
SYMBOL_MISS: Final = "_"
MAX_ATTEMPTS: Final = 6

DATA_ROOT = Path(__file__).parent.parent / "data"
DEBUG = os.environ.get("DEBUG", False)
LOG_LEVEL = logging.DEBUG if DEBUG else logging.WARNING
