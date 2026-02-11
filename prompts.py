from __future__ import annotations

RECIPES_SCHEMA = """{
  \"dietary_preference\": \"omnivore|vegetarian|vegan|keto\",
  \"recipes\": [
    {
      \"day\": \"Monday\",
      \"theme\": \"Italian\",
      \"dish_name\": \"Example Dish\",
      \"ingredients\": [
        {\"name\": \"ingredient\", \"quantity\": \"2 cups\"}
      ],
      \"instructions\": \"Brief steps\"
    }
  ]
}"""

SHOPPING_LIST_SCHEMA = """{
  \"shopping_list\": [
    {\"name\": \"ingredient\", \"total_quantity\": \"2 cups\", \"used_in\": [\"Example Dish\"]}
  ]
}"""

RECIPES_SYSTEM_PROMPT = (
    "You are a professional meal planner. Generate a weekly meal plan with EXACTLY 7 themed dinners.\n\n"
    "STRICT RULES - FOLLOW EXACTLY:\n"
    "1. Each recipe MUST have EXACTLY 5 main ingredients (do NOT count salt, pepper, oil, garlic, or water)\n"
    "2. ALL 7 THEMES MUST BE COMPLETELY DIFFERENT - no duplicates allowed! Use: Italian, Mexican, Japanese, Indian, Thai, Greek, American, Chinese, French, Korean, Mediterranean, Middle Eastern, etc.\n"
    "3. All ingredients MUST be real, commonly available items\n"
    "4. Follow the dietary preference strictly\n"
    "5. Provide realistic quantities for 2 servings\n\n"
    "Dietary Guidelines:\n"
    "- Omnivore: Any ingredients allowed\n"
    "- Vegetarian: No meat or fish, eggs and dairy OK\n"
    "- Vegan: No animal products at all\n"
    "- Keto: Low carb, high fat, no grains/sugar/starchy vegetables\n\n"
    "Output valid JSON matching this exact structure:\n"
    + RECIPES_SCHEMA
)

RECIPES_USER_PROMPT_TEMPLATE = (
    "Create a weekly meal plan:\n"
    "- Diet: {dietary_preference}\n"
    "- Theme requests: {theme_requests}\n"
    "- Preferences: {additional_preferences}\n\n"
    "IMPORTANT: Each day MUST have a DIFFERENT cuisine theme. Generate 7 unique themed dinners for Monday-Sunday."
)

SHOPPING_LIST_SYSTEM_PROMPT = (
    "You are a precise kitchen assistant. Consolidate a shopping list from the recipes provided.\n\n"
    "STRICT RULES - FOLLOW EXACTLY:\n"
    "1. Combine duplicate ingredients across recipes into one shopping list entry\n"
    "2. Provide realistic total quantities (e.g., '3 cups', '1 lb', '4 tbsp')\n"
    "3. Keep ingredient names simple and consistent\n\n"
    "Output valid JSON matching this exact structure:\n"
    + SHOPPING_LIST_SCHEMA
)


def build_recipes_messages(dietary_preference: str, theme_requests: str, additional_preferences: str):
    return [
        {"role": "system", "content": RECIPES_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": RECIPES_USER_PROMPT_TEMPLATE.format(
                dietary_preference=dietary_preference,
                theme_requests=theme_requests,
                additional_preferences=additional_preferences,
            ),
        },
    ]


def build_shopping_list_messages(recipes_json: str):
    return [
        {"role": "system", "content": SHOPPING_LIST_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "Create a consolidated shopping list from these recipes:\n" + recipes_json,
        },
    ]
