"""
Configuration management for the contrast-route-duplicates tool.
Handles loading and validating environment variables.
"""

import os
from typing import Dict, Final, Optional

from dotenv import load_dotenv

from contrast_route_duplicates.models import EnvConfig


def load_config() -> EnvConfig:
    """Load configuration from .env file"""
    load_dotenv()

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
        if not value:
            missing_vars.append(f"{var} ({description})")
        config[var] = value

    if missing_vars:
        raise ValueError(
            "Missing required environment variables in .env file:\n"
            f"{chr(10).join(missing_vars)}"
        )

    # Cast to EnvConfig since we've verified all values exist
    validated_config: Dict[str, str] = {
        k: v for k, v in config.items() if v is not None and k in required_vars
    }

    if set(validated_config.keys()) != set(required_vars.keys()):
        raise ValueError("Configuration validation failed: missing required keys")

    return EnvConfig(
        CONTRAST_BASE_URL=validated_config["CONTRAST_BASE_URL"],
        CONTRAST_ORG_UUID=validated_config["CONTRAST_ORG_UUID"],
        CONTRAST_API_KEY=validated_config["CONTRAST_API_KEY"],
        CONTRAST_AUTH=validated_config["CONTRAST_AUTH"],
    )
