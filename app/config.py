import os

APP_NAME = "gha-lab-app"
APP_VERSION = "0.1.0"


def get_app_env() -> str | None:
    """Return the configured application environment, if one is set."""
    return os.getenv("APP_ENV")

