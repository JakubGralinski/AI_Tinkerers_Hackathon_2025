from agents import Runner
from agents import Runner
from app.agents.plan.exercise_plan_agent import exercise_plan_agent
from app.agents.plan.meal_plan_agent import meal_plan_agent
from app.agents.plan.response_schemas import MealPlanSchema
from app.agents.plan.response_schemas import ExercisePlanSchema
import asyncio

async def plan_week(user_prompt: str):
    meal_task = Runner.run(
        meal_plan_agent,
        user_prompt,
    )
    exercise_task = Runner.run(
        exercise_plan_agent,
        user_prompt,
    )

    meal_result, exercise_result = await asyncio.gather(meal_task, exercise_task)

    meal_output = meal_result.final_output_as(MealPlanSchema)
    exercise_output = exercise_result.final_output_as(ExercisePlanSchema)

    return {
        "meal_plan": meal_output.model_dump(),
        "exercise_plan": exercise_output.model_dump()
    }