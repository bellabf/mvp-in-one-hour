from __future__ import annotations

from openai import OpenAI

from config import SETTINGS


def get_client(api_key: str | None = None) -> OpenAI:
    """Get a configured OpenAI client."""
    return OpenAI(api_key=api_key or SETTINGS.openai_api_key)
