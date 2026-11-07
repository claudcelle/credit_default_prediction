"""Project paths shared by training, notebooks, and the prediction service."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
RAW_DATA_FILE = DATA_DIR / "default_of_credit_card_clients.xls"
MODEL_FILE = MODELS_DIR / "xgboost_pipeline.pkl"
MODEL_METADATA_FILE = MODELS_DIR / "xgboost_metadata.json"
