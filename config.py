"""
Configuration handling – loads environment variables and YAML config.
"""

import os
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

from logger import setup_logger

logger = setup_logger(__name__)

DEFAULT_CONFIG_PATH = Path(__file__).with_name("config.yaml")
ENV_PATH = Path(".env")

def load_environment(env_path: Path = ENV_PATH) -> Dict[str, str]:
    """
    Load environment variables from a .env file.

    Returns:
        Mapping of environment variable names to values.
    """
    if env_path.is_file():
        load_dotenv(dotenv_path=env_path)
        logger.debug("Loaded .env from %s", env_path)
    else:
        logger.warning(".env file not found at %s – falling back to system env", env_path)

    fernet_key = os.getenv("FERNET_KEY")
    if not fernet_key:
        raise RuntimeError("FERNET_KEY not set in environment")
    return {"FERNET_KEY": fernet_key.encode()}

def load_yaml_config(config_path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """
    Load runtime configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Parsed configuration dictionary.
    """
    if not config_path.is_file():
        logger.warning("Config file %s not found – using defaults", config_path)
        return {}

    with config_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
        logger.debug("Loaded config: %s", cfg)
        return cfg