from flask import Flask
from .config import Config
from app.extensions import db, api, ma
from app.routes.user_routes import user_bp
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # init extensions
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    
    # register routes
    app.register_blueprint(user_bp, url_prefix="/api")
    
    return app