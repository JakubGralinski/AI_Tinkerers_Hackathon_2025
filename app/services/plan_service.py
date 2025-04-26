from app.agents.plan.exercise_plan_agent import exercise_plan_agent
from app.agents.plan.meal_plan_agent import NutritionPlannerAgent
from app.agents.plan.response_schemas import MealPlanSchema
from app.agents.plan.response_schemas import ExercisePlanSchema
from app.agents.plan.tool_wrapper import Tool
from openai import OpenAI
from agents import Agent, Runner
from app.agents.plan.plan_mgr_agent import PlanManagerAgent
import json
from app.config import Config

with open("./demo/mfp_daily_totals_and_menu.json", encoding="utf-8") as f:
    mfp_data = json.load(f)
with open("./demo/strava_activities.json", encoding="utf-8") as f:
    strava_data = json.load(f)

async def plan_week(user_prompt: str):
    nutrition_planner_agent = NutritionPlannerAgent(
        client=OpenAI(api_key=Config.OPENAI_API_KEY),
        user_profile_path="./demo/user_profile.json"
    )
    
    def run_meal_planner(self, input_text):
        nutrition_planner_agent.plan_meals(mfp_data, strava_data, user_prompt)
    
    tools = [
        Tool(name="Meal Planner", description="Creates a weekly meal plan based on nutrition data and goals.", agent=nutrition_planner_agent, run_func=run_meal_planner),
        Tool(name="Exercise Planner", description="Creates a weekly training plan based on Strava activities and fitness goals.", agent=exercise_plan_agent),
    ]
    
    plan_manager = PlanManagerAgent(
        name="Plan Manager",
        handoffs=tools
    )

    plan = await plan_manager.run(user_prompt)

    return {
        "plan": plan
    }
    

    