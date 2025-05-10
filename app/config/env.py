# Path: app/config/env.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class EnvConfig:
    """Load and validate environment variables"""

    # Required environment variables
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    @classmethod
    def validate(cls):
        """Ensure all required environment variables are set"""
        missing_vars = [
            var
            for var in [
                "DB_HOST",
                "DB_PORT",
                "DB_USER",
                "DB_PASSWORD",
                "DB_NAME",
            ]
            if getattr(cls, var) is None
        ]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )


# Validate environment variables at startup
EnvConfig.validate()
