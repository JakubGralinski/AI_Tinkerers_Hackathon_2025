from agents import Agent
from app.agents.plan.response_schemas import MealPlanSchema

meal_plan_agent = Agent(
    name="Meal Planner",
    instructions=(
        "Create a full daily meal plan. Take into account user details from the input to generate suitable plan for him."
        "Each meal must include:\n"
        "- The meal name (e.g., Breakfast, Lunch, Dinner, Snack)\n"
        "- A list of ingredients\n"
        "- The total estimated calories\n"
        "- Short preparation instructions\n\n"
        "Respond structured according to the provided MealPlanSchema output model."
    ),
    output_type=MealPlanSchema,
    model="o3"
)
