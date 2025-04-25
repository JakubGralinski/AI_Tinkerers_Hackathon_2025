from typing import List
from pydantic import BaseModel

class MealPlanItem(BaseModel):
    meal: str
    ingredients: List[str]
    calories: int
    instructions: str

class MealPlanSchema(BaseModel):
    meal_plan: List[MealPlanItem]

class Exercise(BaseModel):
    name: str
    sets: int
    reps: int
    rest_time: int

class ExercisePlanItem(BaseModel):
    day: int
    exercises: List[Exercise]

class ExercisePlanSchema(BaseModel):
    exercise_plan: List[ExercisePlanItem]
