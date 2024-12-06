"""
Configuration management for the contrast-route-duplicates tool.
Handles loading and validating environment variables.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Final, Optional

from dotenv import load_dotenv

from contrast_route_duplicates.models import EnvConfig

logger = logging.getLogger(__name__)

def load_config() -> EnvConfig:
    """Load configuration from environment variables and/or .env file"""
    # Try to load from .env if it exists, but environment variables take precedence
    if Path('.env').exists():
        logger.debug("Found .env file, loading...")
        load_dotenv(Path('.env'))
    
    required_vars: Final[Dict[str, str]] = {
        "CONTRAST_BASE_URL": "Base URL",
        "CONTRAST_ORG_UUID": "Organization UUID",
        "CONTRAST_API_KEY": "API Key",
        "CONTRAST_AUTH": "Authorization header",
    }

    config: Dict[str, Optional[str]] = {}
    missing_vars: list[str] = []

    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            logger.debug(f"Found {var} from {'environment' if var in os.environ else '.env file'}")
        else:
            missing_vars.append(f"{var} ({description})")
        config[var] = value

    if missing_vars:
        raise ValueError(
            "Missing required variables (check both environment and .env file):\n"
            f"{chr(10).join(missing_vars)}"
        )

    validated_config: Dict[str, str] = {
        k: v for k, v in config.items() if v is not None and k in required_vars
    }

    return EnvConfig(
        CONTRAST_BASE_URL=validated_config["CONTRAST_BASE_URL"],
        CONTRAST_ORG_UUID=validated_config["CONTRAST_ORG_UUID"],
        CONTRAST_API_KEY=validated_config["CONTRAST_API_KEY"],
        CONTRAST_AUTH=validated_config["CONTRAST_AUTH"],
    )
