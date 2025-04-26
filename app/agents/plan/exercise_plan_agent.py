#%%
import os
import json
import requests
from dotenv import load_dotenv
from agents import Agent
from app.agents.plan.response_schemas import ExercisePlanSchema
from app.config import Config

STRAVA_ACCESS_TOKEN = Config.STRAVA_ACCESS_TOKEN

# 1. Fetch Strava Activities
if not STRAVA_ACCESS_TOKEN:
    raise ValueError("❌ STRAVA_ACCESS_TOKEN missing in .env!")

response = requests.get(
    "https://www.strava.com/api/v3/athlete/activities",
    headers={"Authorization": f"Bearer {STRAVA_ACCESS_TOKEN}"},
    params={"per_page": 100, "page": 1}
)

activities = response.json()

# Save activities locally
with open("strava_activities.json", "w", encoding="utf-8") as f:
    json.dump(activities, f, indent=2)

print("✅ Saved strava_activities.json")

# 2. Prepare Summary
summary_text = "\n".join([
    f"{a['name']} - {a['sport_type']} - {round(a.get('distance', 0) / 1000, 2)} km on {a['start_date'][:10]}"
    for a in activities if "start_date" in a
])

# 3. Prepare Prompt (outside any function ✅)
prompt_coach = f"""
You are an experienced personal coach and professional training planner AI.

Here is the user's complete workout history from Strava:

{summary_text}

User details:
- Height: 180 cm
- Weight: 80 kg
- Training Goal: Improve endurance and strength.
- I'm allergic and I have deuteranopia (color blindness).
- If there's a gym session, then no running that day, and vice versa.

Your task:
- Analyze the workout history
- Identify training gaps, overtraining risks, or missing elements
- Analyze considering special needs (allergy, vision)
- Create a detailed 7-day training plan
- Each workout should include type, duration, intensity
- Suggest YouTube video links for proper exercise technique
- Recommend injury prevention strategies
- Be realistic and motivating

Start with an encouraging message!
"""

# 4. Create Agent
exercise_plan_agent = Agent(
    name="Exercise Planner",
    instructions=prompt_coach,
    output_type=ExercisePlanSchema,
    model="o3"
)