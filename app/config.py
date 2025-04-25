import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")