from agents import Agent
from app.agents.plan.response_schemas import ExercisePlanSchema

exercise_plan_agent = Agent(
    name="Exercise Planner",
    instructions=(
        "Create a structured exercise plan for a full day.\n"
        "For each day, list multiple exercises. Take into account user details from the input to generate suitable plan for him. "
        "Each exercise must include:\n"
        "- The name of the exercise\n"
        "- The number of sets\n"
        "- The number of repetitions per set\n"
        "- The rest time in seconds between sets\n\n"
        "Respond strictly following the ExercisePlanSchema output model."
    ),
    output_type=ExercisePlanSchema,
    model="o3"
)