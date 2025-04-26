# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/python/process', methods=['POST'])
def process_data():
    data = request.json
    
    # Handle workout plan generation
    if data.get('action') == 'create_workout_plan':
        profile_data = data.get('profileData', {})
        communication_prefs = data.get('communicationPreferences', {})
        
        # In a real implementation, this would use the profile data to generate a custom plan
        # For this demo, we'll return a structured workout and nutrition plan
        
        return jsonify({
            "workoutPlan": generate_workout_plan(profile_data),
            "nutritionPlan": generate_nutrition_plan(profile_data)
        })
    
    # Default response for other process requests
    return jsonify({"processed": True, "input": data, "result": "Processed by Python"})

@app.route('/api/python/analyze', methods=['POST'])
def analyze_data():
    data = request.json
    # Custom data analysis with Python libraries
    # Example: Using pandas, numpy, scikit-learn, etc.
    return jsonify({"analyzed": True, "input": data, "analysis": "Data analyzed by Python"})

def generate_workout_plan(profile_data):
    # In a real implementation, this would use ML/AI to create personalized plans
    # based on the user's fitness level, goals, and preferences
    
    # Sample workout plan structure
    return {
        "weeklySchedule": [
            {
                "day": "Monday",
                "focus": "Upper Body Strength",
                "exercises": [
                    {"name": "Push-ups", "sets": 3, "reps": "10-12"},
                    {"name": "Dumbbell Rows", "sets": 3, "reps": "10-12"},
                    {"name": "Shoulder Press", "sets": 3, "reps": "10-12"},
                    {"name": "Bicep Curls", "sets": 3, "reps": "10-12"}
                ],
                "duration": "45 minutes",
                "intensity": "Moderate"
            },
            {
                "day": "Tuesday",
                "focus": "Cardio",
                "exercises": [
                    {"name": "Jogging/Running", "duration": "30 minutes", "intensity": "Moderate"}
                ],
                "duration": "30 minutes",
                "intensity": "Moderate"
            },
            {
                "day": "Wednesday",
                "focus": "Lower Body Strength",
                "exercises": [
                    {"name": "Bodyweight Squats", "sets": 3, "reps": "15"},
                    {"name": "Lunges", "sets": 3, "reps": "10 each leg"},
                    {"name": "Glute Bridges", "sets": 3, "reps": "15"},
                    {"name": "Calf Raises", "sets": 3, "reps": "15"}
                ],
                "duration": "45 minutes",
                "intensity": "Moderate"
            },
            {
                "day": "Thursday",
                "focus": "Rest Day",
                "exercises": [
                    {"name": "Light Walking", "duration": "20 minutes", "intensity": "Low"},
                    {"name": "Stretching", "duration": "10 minutes", "intensity": "Low"}
                ],
                "duration": "30 minutes",
                "intensity": "Low"
            },
            {
                "day": "Friday",
                "focus": "Full Body Circuit",
                "exercises": [
                    {"name": "Jumping Jacks", "duration": "30 seconds"},
                    {"name": "Mountain Climbers", "duration": "30 seconds"},
                    {"name": "Plank", "duration": "30 seconds"},
                    {"name": "Bodyweight Squats", "duration": "30 seconds"},
                    {"name": "Push-ups", "duration": "30 seconds"}
                ],
                "notes": "Complete 3-4 rounds with 1 minute rest between rounds",
                "duration": "30-40 minutes",
                "intensity": "High"
            },
            {
                "day": "Saturday",
                "focus": "Cardio and Core",
                "exercises": [
                    {"name": "Brisk Walking/Jogging", "duration": "20 minutes", "intensity": "Moderate"},
                    {"name": "Plank", "sets": 3, "duration": "30 seconds"},
                    {"name": "Bicycle Crunches", "sets": 3, "reps": "15 each side"},
                    {"name": "Russian Twists", "sets": 3, "reps": "10 each side"}
                ],
                "duration": "40 minutes",
                "intensity": "Moderate"
            },
            {
                "day": "Sunday",
                "focus": "Active Recovery",
                "exercises": [
                    {"name": "Yoga/Stretching", "duration": "20-30 minutes", "intensity": "Low"}
                ],
                "duration": "20-30 minutes",
                "intensity": "Low"
            }
        ]
    }

def generate_nutrition_plan(profile_data):
    # In a real implementation, this would calculate caloric needs and macronutrient distribution
    # based on the user's goals, body composition, and activity level
    
    # Sample nutrition plan structure
    return {
        "dailyCalories": "Based on your goals and activity level",
        "macroDistribution": {
            "protein": "30%",
            "carbohydrates": "40%",
            "fats": "30%"
        },
        "mealPlan": [
            {
                "meal": "Breakfast",
                "options": [
                    "Oatmeal with fruit and nuts",
                    "Greek yogurt with berries and granola",
                    "Whole grain toast with avocado and eggs"
                ]
            },
            {
                "meal": "Lunch",
                "options": [
                    "Grilled chicken salad with mixed vegetables",
                    "Quinoa bowl with vegetables and lean protein",
                    "Turkey and avocado wrap with side salad"
                ]
            },
            {
                "meal": "Dinner",
                "options": [
                    "Baked salmon with roasted vegetables",
                    "Lean beef stir-fry with brown rice",
                    "Grilled chicken with sweet potato and steamed vegetables"
                ]
            },
            {
                "meal": "Snacks (choose 2-3 per day)",
                "options": [
                    "Apple with almond butter",
                    "Protein shake",
                    "Handful of nuts and dried fruit",
                    "Carrot sticks with hummus",
                    "Greek yogurt with honey"
                ]
            }
        ],
        "hydration": "Aim for 8-10 glasses of water daily",
        "notes": "Adjust portions based on hunger and energy levels. Focus on whole, minimally processed foods when possible."
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)