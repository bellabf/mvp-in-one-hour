from __future__ import annotations

import json
import time

from client import get_client
from config import SETTINGS
from prompts import build_recipes_messages, build_shopping_list_messages
from schemas import MealPlan, RecipesOnly


def _parse_json_content(content: str) -> dict:
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]
    return json.loads(content)


class MealPlanGenerator:
    """Generates weekly themed meal plans."""

    def __init__(self):
        self.client = get_client()

    def generate_recipes(
        self,
        dietary_preference: str,
        theme_requests: str = "random",
        additional_preferences: str = "none",
        model: str | None = None,
    ) -> RecipesOnly:
        messages = build_recipes_messages(
            dietary_preference=dietary_preference,
            theme_requests=theme_requests if theme_requests else "random diverse cuisines",
            additional_preferences=additional_preferences if additional_preferences else "none",
        )

        result = self.client.chat.completions.create(
            model=model or SETTINGS.meal_plan_model,
            temperature=SETTINGS.temperature,
            messages=messages,
            response_format={"type": "json_object"},
        )

        content = result.choices[0].message.content or "{}"
        recipes_data = _parse_json_content(content)
        return RecipesOnly(**recipes_data)

    def generate_shopping_list(self, recipes: RecipesOnly, model: str | None = None) -> dict:
        recipes_json = json.dumps(recipes.model_dump())
        messages = build_shopping_list_messages(recipes_json)

        result = self.client.chat.completions.create(
            model=model or SETTINGS.shopping_list_model,
            temperature=SETTINGS.temperature,
            messages=messages,
            response_format={"type": "json_object"},
        )

        content = result.choices[0].message.content or "{}"
        return _parse_json_content(content)

    def generate(
        self,
        dietary_preference: str,
        theme_requests: str = "random",
        additional_preferences: str = "none",
    ) -> dict:
        start_time = time.time()

        try:
            recipes = self.generate_recipes(
                dietary_preference=dietary_preference,
                theme_requests=theme_requests,
                additional_preferences=additional_preferences,
            )
            shopping_list_data = self.generate_shopping_list(recipes)

            meal_plan = MealPlan(
                dietary_preference=recipes.dietary_preference,
                recipes=recipes.recipes,
                shopping_list=shopping_list_data.get("shopping_list", []),
            )

            generation_time = time.time() - start_time

            return {
                "success": True,
                "meal_plan": meal_plan.model_dump(),
                "generation_time": round(generation_time, 2),
                "error": None,
            }

        except json.JSONDecodeError as e:
            return {"success": False, "meal_plan": None, "error": f"JSON parsing error: {str(e)}"}
        except Exception as e:
            return {"success": False, "meal_plan": None, "error": str(e)}
