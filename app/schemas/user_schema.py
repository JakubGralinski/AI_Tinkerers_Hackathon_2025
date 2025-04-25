from app.models.user_model import UserModel
from flask_marshmallow import Marshmallow
from app.extensions import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True