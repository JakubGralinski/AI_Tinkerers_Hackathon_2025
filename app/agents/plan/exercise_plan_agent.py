import os
import json
from dotenv import load_dotenv
from agents import Agent
from app.agents.plan.response_schemas import ExercisePlanSchema  # <- your expected output structure

load_dotenv()

with open("strava_activities.json") as f:
    activities = json.load(f)

summary = "\n".join([
    f"{a['name']} - {a['sport_type']} - {round(a.get('distance', 0) / 1000, 2)} km on {a['start_date'][:10]}"
    for a in activities
])

prompt_coach = f"""
You are an experienced personal coach and professional training planner AI.

Here is the user's complete workout history from Strava:

{summary}

User details:
- Height: 180 cm
- Weight: 80 kg
- Training Goal: Improve endurance and strength.
- I'm allergic and i have deutronopia.
- If there's a gym session, then no run and vice versa

Your task:
- Analyze the complete workout history
- Identify training gaps, overtraining risks, or missing elements
- Analyze regarding diseases
- Create a detailed 7-day training plan
- The plan should include specific workout types, target duration, intensity levels, and recovery days
- Recommend any modifications for injury prevention
- Ensure the plan supports gradual performance progression
- Be realistic and motivating
- To each exercise send a validated URL link to a youtube video showing the proper technique

Start your response with an encouraging message!
"""

exercise_plan_agent = Agent(
    name="Exercise Planner",
    instructions=prompt_coach,
    output_type=ExercisePlanSchema,
    model="o3"
)

exercise_plan = exercise_plan_agent.run({})

print("\n🏋️ Weekly Training Plan Generated:")
print(exercise_plan)