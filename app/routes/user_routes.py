from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema

user_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_bp.route('/users/', methods=['GET'])
def get_users():
    users = UserService.get_all_users()
    return users_schema.dump(users), 200

@user_bp.route('/users/', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    
    if not name or not email:
        return {
            "error": "Name and Email are both required"
        }, 400
    
    user = UserService.create_user(name, email)
    return user_schema.dump(user), 201