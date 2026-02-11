from __future__ import annotations

from email_utils import format_meal_plan_email
from validation import run_basic_validation


SAMPLE_MEAL_PLAN = {
    "dietary_preference": "omnivore",
    "recipes": [
        {
            "day": "Monday",
            "theme": "Italian",
            "dish_name": "Pasta Primavera",
            "ingredients": [
                {"name": "pasta", "quantity": "8 oz"},
                {"name": "zucchini", "quantity": "1 cup"},
                {"name": "tomatoes", "quantity": "1 cup"},
                {"name": "parmesan", "quantity": "1/2 cup"},
                {"name": "basil", "quantity": "2 tbsp"},
            ],
            "instructions": "Cook pasta and toss with veggies.",
        }
    ]
    + [
        {
            "day": day,
            "theme": theme,
            "dish_name": f"Dish {i}",
            "ingredients": [
                {"name": "a", "quantity": "1"},
                {"name": "b", "quantity": "1"},
                {"name": "c", "quantity": "1"},
                {"name": "d", "quantity": "1"},
                {"name": "e", "quantity": "1"},
            ],
            "instructions": "Do it.",
        }
        for i, (day, theme) in enumerate(
            [
                ("Tuesday", "Mexican"),
                ("Wednesday", "Japanese"),
                ("Thursday", "Indian"),
                ("Friday", "Thai"),
                ("Saturday", "Greek"),
                ("Sunday", "American"),
            ],
            start=2,
        )
    ],
    "shopping_list": [
        {"name": "pasta", "total_quantity": "8 oz", "used_in": ["Pasta Primavera"]}
    ],
}


def test_format_meal_plan_email_includes_sections():
    body = format_meal_plan_email(SAMPLE_MEAL_PLAN)
    assert "SHOPPING LIST" in body
    assert "RECIPES" in body
    assert "Pasta Primavera" in body


def test_run_basic_validation_passes_for_valid_plan():
    result = {"success": True, "meal_plan": SAMPLE_MEAL_PLAN}
    validation = run_basic_validation(result)
    assert validation["passed"] is True


def test_run_basic_validation_fails_for_bad_counts():
    broken = {
        **SAMPLE_MEAL_PLAN,
        "recipes": SAMPLE_MEAL_PLAN["recipes"][:1],
    }
    result = {"success": True, "meal_plan": broken}
    validation = run_basic_validation(result)
    assert validation["passed"] is False
