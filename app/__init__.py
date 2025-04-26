from flask import Flask
from .config import Config
from dotenv import load_dotenv
from app.routes.plan_routes import plan_blueprint
import openai

load_dotenv()

openai.api_key = Config.OPENAI_API_KEY

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(plan_blueprint, url_prefix="/api")
    
    return app