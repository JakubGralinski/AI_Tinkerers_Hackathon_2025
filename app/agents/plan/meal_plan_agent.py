import os
import json
import statistics
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("mfp_daily_totals_and_menu.json", encoding="utf-8") as f:
    mfp_data = json.load(f)
with open("strava_activities.json", encoding="utf-8") as f:
    strava_data = json.load(f)

class NutritionPlannerAgent:
    """
    AI agent that plans meals based on MyFitnessPal and Strava data,
    user profile (height, weight, budget, preferences, days to plan) loaded from JSON.
    """

    def __init__(self, client: OpenAI, user_profile_path: str):
        # OpenAI client
        self.client = client
        # Load user profile from JSON
        with open(user_profile_path, encoding="utf-8") as pf:
            profile = json.load(pf)
        self.height_cm       = profile.get("height_cm")
        self.weight_kg       = profile.get("weight_kg")
        self.daily_budget    = profile.get("daily_budget")
        self.diet_pref       = profile.get("diet_pref", "no preferences")
        self.include_recipes = profile.get("include_recipes", False)
        self.plan_days       = profile.get("plan_days", 3)

    def summarize_mfp(self, mfp, days=7):
        """Return list of dicts with date and totals for last `days` days"""
        recent = mfp[-days:]
        result = []
        for day in recent:
            t = day.get("totals", {})
            result.append({
                "date":    day.get("date"),
                "cal":     t.get("calories", 0),
                "protein": t.get("protein", 0),
                "carb":    t.get("carbohydrates", 0),
                "fat":     t.get("fat", 0),
            })
        return result

    def summarize_strava(self, strava, n=5):
        """Return list of dicts for last `n` workouts, classifying cardio vs strength"""
        result = []
        for a in strava[:n]:
            km = round(a.get("distance", 0) / 1000, 2)
            if km == 0:
                session = "strength"
                est_burn = 1.5 * 8 * self.weight_kg  # 8 kcal/kg/hr
            else:
                session = "cardio"
                est_burn = km * 60  # kcal per km
            result.append({
                "name":     a.get("name"),
                "session":  session,
                "km":       km,
                "date":     a.get("start_date", "")[:10],
                "est_burn": round(est_burn),
            })
        return result

    def _compute_averages(self, mfp_summary):
        """Compute 7-day average intake"""
        avg_cal  = statistics.mean(d["cal"]     for d in mfp_summary)
        avg_prot = statistics.mean(d["protein"] for d in mfp_summary)
        avg_carb = statistics.mean(d["carb"]    for d in mfp_summary)
        avg_fat  = statistics.mean(d["fat"]     for d in mfp_summary)
        return round(avg_cal), round(avg_prot), round(avg_carb), round(avg_fat)

    def _predict_targets(self, workouts):
        """
        Predict daily calorie and macro targets based on user profile and workouts:
        - BMR by Mifflin-St Jeor (male assumed)
        - TDEE = BMR * activity factor
        - Distribute macros: protein 2g/kg, carbs 3g/kg, fat 0.8g/kg
        """
        bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * 30 + 5
        act_factor = 1.2 + min(len([w for w in workouts if w['session']=='cardio']) * 0.05, 0.3)
        tdee = bmr * act_factor
        prot = 2 * self.weight_kg
        carb = 3 * self.weight_kg
        fat  = 0.8 * self.weight_kg
        return round(tdee), round(prot), round(carb), round(fat)

    def plan_meals(self, mfp_data, strava_data):
        # Summaries
        mfp_sum    = self.summarize_mfp(mfp_data)
        strava_sum = self.summarize_strava(strava_data)
        avg_cal, avg_prot, avg_carb, avg_fat = self._compute_averages(mfp_sum)

        # Predict targets
        target_cal, target_prot, target_carb, target_fat = self._predict_targets(strava_sum)

        # Build prompt
        prompt = f"""
        You are a professional AI Nutritionist and Fitness Coach.

        User profile:
        - Height: {self.height_cm} cm
        - Weight: {self.weight_kg} kg
        - Dietary preference: {self.diet_pref}
        - Daily budget: {self.daily_budget or 'no limit'} USD

        Recent nutrition (7-day average):
        - Energy intake: {avg_cal} kcal
        - Protein: {avg_prot} g
        - Carbohydrates: {avg_carb} g
        - Fat: {avg_fat} g

        Recent workouts:
        """
        for w in strava_sum:
            prompt += f"  • {w['name']} ({w['session']}) — {w['km']} km on {w['date']} (approx. {w['est_burn']} kcal burned)\n"

        prompt += f"""

        Training Targets:
        - Daily Calories: {target_cal} kcal
        - Protein: {target_prot} g
        - Carbohydrates: {target_carb} g
        - Fat: {target_fat} g

        🛠️ Your tasks:
        1. Analyze the user's nutrition and training history to highlight any imbalances or opportunities for improvement.
        2. Design a {self.plan_days}-day detailed daily meal plan matching the target macros and calories.
        3. Each day must include:
            - Breakfast
            - Lunch
            - Dinner
            - 2 Snack ideas
        4. For each meal/snack, provide:
            - Meal name
            - Estimated calories
            - Macros (Protein/Carbs/Fats) in grams
            - Key ingredients
            - Short preparation instructions
        """
        if self.include_recipes:
            prompt += "- Additionally, suggest a validated URL link to a trusted recipe youtube video for each dish, that is no older than 6 months.\n"

        prompt += f"""
        Constraints:
        - Stay within the budget of {self.daily_budget or 'no limit'} USD per day.
        - Keep meals practical, easy to prepare, and healthy.
        - Vary meals across days to avoid repetition.
        - Focus on balanced, high-quality nutrition suitable for an athlete improving endurance and strength.

        Respond in a clean, structured format.

        Thank you!
        """

        # Call API
        resp = self.client.chat.completions.create(
            model="o3",
            messages=[
                {"role": "system", "content": "You are a Nutrition & Fitness expert."},
                {"role": "user",   "content": prompt}
            ],
        )
        return resp.choices[0].message.content

agent = NutritionPlannerAgent(client, user_profile_path="user_profile.json")
print(agent.plan_meals(mfp_data, strava_data))