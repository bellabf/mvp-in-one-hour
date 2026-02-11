from __future__ import annotations


def run_basic_validation(meal_plan_result: dict) -> dict:
    """Run quick programmatic validation checks (not LLM-based)."""
    if not meal_plan_result.get("success"):
        return {"passed": False, "errors": [meal_plan_result.get("error")]}

    meal_plan = meal_plan_result["meal_plan"]
    errors = []

    # Check 1: 7 recipes
    if len(meal_plan["recipes"]) != 7:
        errors.append(f"Expected 7 recipes, got {len(meal_plan['recipes'])}")

    # Check 2: Unique themes
    themes = [r["theme"].lower() for r in meal_plan["recipes"]]
    if len(themes) != len(set(themes)):
        duplicates = [t for t in themes if themes.count(t) > 1]
        errors.append(f"Duplicate themes: {set(duplicates)}")

    # Check 3: 5 ingredients per recipe
    for recipe in meal_plan["recipes"]:
        if len(recipe["ingredients"]) != 5:
            errors.append(
                f"{recipe['day']}: {len(recipe['ingredients'])} ingredients (expected 5)"
            )

    return {"passed": len(errors) == 0, "errors": errors}
