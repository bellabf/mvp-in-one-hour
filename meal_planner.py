from __future__ import annotations

import gradio as gr
import time as pytime

from email_utils import send_meal_plan_email
from generator import MealPlanGenerator
from validation import run_basic_validation


generator = MealPlanGenerator()


def format_shopping_list(meal_plan: dict) -> str:
    """Format shopping list section."""
    lines = ["## Shopping List\n"]
    for item in meal_plan["shopping_list"]:
        lines.append(f"- {item['total_quantity']} **{item['name']}**")
    return "\n".join(lines)


def format_single_recipe(recipe: dict) -> str:
    """Format a single recipe compactly."""
    ingredients = ", ".join([f"{ing['quantity']} {ing['name']}" for ing in recipe["ingredients"]])
    return f"**{recipe['day']}** | {recipe['theme']} | *{recipe['dish_name']}*\n{ingredients}\n"


def generate_plan_streaming(dietary_pref, theme_requests, additional_prefs):
    """Generate meal plan with streaming output."""
    output = "Generating your meal plan..."
    yield output

    result = generator.generate(
        dietary_preference=dietary_pref,
        theme_requests=theme_requests if theme_requests.strip() else "random",
        additional_preferences=additional_prefs if additional_prefs.strip() else "none",
    )

    if not result["success"]:
        yield f"Error: {result['error']}"
        return

    meal_plan = result["meal_plan"]

    # Show shopping list first
    output = f"## Weekly {meal_plan['dietary_preference'].title()} Meal Plan\n\n"
    output += format_shopping_list(meal_plan) + "\n\n---\n\n"
    output += "## Recipes\n\n"
    yield output
    pytime.sleep(0.1)

    # Stream recipes one by one
    for recipe in meal_plan["recipes"]:
        output += format_single_recipe(recipe) + "\n"
        yield output
        pytime.sleep(0.05)

    # Validation status
    validation = run_basic_validation(result)
    status = "All checks passed" if validation["passed"] else f"Issues: {', '.join(validation['errors'])}"
    output += f"---\n*Generated in {result['generation_time']}s | {status}*"
    yield output


def send_email_ui(email, dietary_pref, theme_requests, additional_prefs):
    """Generate and send meal plan via email."""
    if not email or "@" not in email:
        return "Enter a valid email address."

    result = generator.generate(
        dietary_preference=dietary_pref,
        theme_requests=theme_requests if theme_requests.strip() else "random",
        additional_preferences=additional_prefs if additional_prefs.strip() else "none",
    )

    if not result["success"]:
        return f"Generation failed: {result['error']}"

    email_result = send_meal_plan_email(email, result["meal_plan"])
    return email_result["message"]


with gr.Blocks(title="Weekly Meal Planner") as app:
    gr.Markdown("# Weekly Meal Planner\nGenerate 7 themed dinners with a consolidated shopping list.")

    with gr.Row():
        with gr.Column(scale=1):
            dietary_dropdown = gr.Dropdown(
                choices=["omnivore", "vegetarian", "vegan", "keto"],
                value="omnivore",
                label="Diet",
            )
            theme_input = gr.Textbox(label="Themes (optional)", placeholder="Italian, Mexican...", lines=1)
            additional_input = gr.Textbox(
                label="Preferences (optional)", placeholder="no nuts, quick meals...", lines=1
            )
            generate_btn = gr.Button("Generate", variant="primary")

            gr.Markdown("---")
            email_input = gr.Textbox(label="Email", placeholder="you@example.com")
            send_btn = gr.Button("Email Plan")
            email_status = gr.Textbox(label="Status", interactive=False)

        with gr.Column(scale=2):
            output_display = gr.Markdown("Click **Generate** to start.")

    generate_btn.click(
        fn=generate_plan_streaming,
        inputs=[dietary_dropdown, theme_input, additional_input],
        outputs=[output_display],
    )

    send_btn.click(
        fn=send_email_ui,
        inputs=[email_input, dietary_dropdown, theme_input, additional_input],
        outputs=[email_status],
    )


if __name__ == "__main__":
    app.launch(share=True)
