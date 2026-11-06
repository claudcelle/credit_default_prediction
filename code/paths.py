"""Shared project paths, independent of the current working directory."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CODE_DIR = PROJECT_ROOT / "code"
DATA_DIR = PROJECT_ROOT / "data"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
DOCS_DIR = PROJECT_ROOT / "docs"
MODELS_DIR = PROJECT_ROOT / "models"

RAW_DATA_FILE = DATA_DIR / "default_of_credit_card_clients.xls"
