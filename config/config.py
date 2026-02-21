"""
Centralized configuration loader.
- Loads static config from YAML
- Loads secrets from .env
- Validates required environment variables
- OS-agnostic (pathlib)
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT_DIR / "config"
DATA_DIR = ROOT_DIR / "data"

ENV_PATH = ROOT_DIR / ".env"
YAML_PATH = CONFIG_DIR / "config.yaml"

# ---------------------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------------------

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    logger.warning(".env file not found at project root")

# ---------------------------------------------------------------------
# Environment validation
# ---------------------------------------------------------------------

REQUIRED_ENV_VARS = [
    "DB_USERNAME",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
]

missing_vars = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
if missing_vars:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

# ---------------------------------------------------------------------
# Load YAML config
# ---------------------------------------------------------------------

def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

_yaml_config = _load_yaml(YAML_PATH)

# ---------------------------------------------------------------------
# Data paths
# ---------------------------------------------------------------------

DATA_PATH_TRAIN = ROOT_DIR / _yaml_config["data"]["train_path"]
DATA_PATH_TEST = ROOT_DIR / _yaml_config["data"]["test_path"]

# ---------------------------------------------------------------------
# Model configuration
# ---------------------------------------------------------------------

MODEL_CONFIG = {
    "name": _yaml_config["model"]["name"],
    "threshold": _yaml_config["model"]["threshold"],
}

MODEL_PARAMS = _yaml_config["model"]["params"]

# ---------------------------------------------------------------------
# Feature configuration
# ---------------------------------------------------------------------

PREDICTION_COLS = _yaml_config["features"]["prediction_cols"]
DRIFT_FEATURES = _yaml_config["features"]["drift_features"]

# ---------------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------------

DB_PARAMS = {
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "dbname": os.getenv("DB_NAME"),
}

DB_URL = (
    f"postgresql+psycopg2://{DB_PARAMS['user']}:"
    f"{DB_PARAMS['password']}@{DB_PARAMS['host']}:"
    f"{DB_PARAMS['port']}/{DB_PARAMS['dbname']}"
)

# ---------------------------------------------------------------------
# Public exports
# ---------------------------------------------------------------------

__all__ = [
    "ROOT_DIR",
    "DATA_PATH_TRAIN",
    "DATA_PATH_TEST",
    "MODEL_CONFIG",
    "MODEL_PARAMS",
    "PREDICTION_COLS",
    "DRIFT_FEATURES",
    "DB_PARAMS",
    "DB_URL",
]

if __name__ == "__main__":
    print(ROOT_DIR)
    print(DATA_PATH_TRAIN)
    print(DATA_PATH_TEST)