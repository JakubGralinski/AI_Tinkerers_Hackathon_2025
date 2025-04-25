from app.models.user_model import UserModel
from app.extensions import db

class UserService:
    @staticmethod
    def get_all_users():
        return UserModel.query.all()
    
    @staticmethod
    def create_user(name, email):
        user = UserModel(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return user