import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")