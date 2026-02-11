from __future__ import annotations

import os
import pytest

from generator import MealPlanGenerator


def test_generate_meal_plan_integration():
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")

    generator = MealPlanGenerator()
    result = generator.generate(dietary_preference="omnivore")

    assert result["success"] is True
    assert result["meal_plan"]["dietary_preference"] == "omnivore"
    assert len(result["meal_plan"]["recipes"]) == 7
    assert len(result["meal_plan"]["shopping_list"]) > 0
