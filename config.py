from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # API
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")

    # Model settings
    meal_plan_model: str = os.getenv("MEAL_PLAN_MODEL", "gpt-4o-mini")
    shopping_list_model: str = os.getenv("SHOPPING_LIST_MODEL", "gpt-4o-mini")
    temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

    # Email settings (Gmail with App Password)
    email_sender: str = os.getenv("EMAIL_SENDER", "bellareadsai@gmail.com")
    email_password: str = os.getenv("EMAIL_PASSWORD", "your-app-password")

    # Meal generation settings
    ingredients_per_recipe: int = int(os.getenv("INGREDIENTS_PER_RECIPE", "5"))


SETTINGS = Settings()
