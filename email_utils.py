from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import SETTINGS


def format_meal_plan_email(meal_plan: dict) -> str:
    """Format meal plan as readable email content (shopping list first)."""
    lines = []
    lines.append("=" * 40)
    lines.append(f"WEEKLY MEAL PLAN ({meal_plan['dietary_preference'].upper()})")
    lines.append("=" * 40)
    lines.append("")

    # Shopping list FIRST
    lines.append("SHOPPING LIST")
    lines.append("-" * 20)
    for item in meal_plan["shopping_list"]:
        lines.append(f"- {item['total_quantity']} {item['name']}")
    lines.append("")

    # Recipes
    lines.append("=" * 40)
    lines.append("RECIPES")
    lines.append("=" * 40)
    for recipe in meal_plan["recipes"]:
        lines.append(f"\n{recipe['day'].upper()} - {recipe['theme']}")
        lines.append(f"{recipe['dish_name']}")
        ingredients = ", ".join([f"{ing['quantity']} {ing['name']}" for ing in recipe["ingredients"]])
        lines.append(f"Ingredients: {ingredients}")
        lines.append(f"Instructions: {recipe['instructions']}")

    return "\n".join(lines)


def send_meal_plan_email(recipient_email: str, meal_plan: dict) -> dict:
    """Send meal plan via email."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SETTINGS.email_sender
        msg["To"] = recipient_email
        msg["Subject"] = "Your Weekly Meal Plan"

        body = format_meal_plan_email(meal_plan)
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SETTINGS.email_sender, SETTINGS.email_password)
            server.send_message(msg)

        return {"success": True, "message": f"Email sent to {recipient_email}"}
    except Exception as e:
        return {"success": False, "message": f"Failed to send email: {str(e)}"}
