from flask import Blueprint, request, jsonify
from app.services.plan_service import plan_week
import asyncio

plan_blueprint = Blueprint("plan", __name__)

@plan_blueprint.route('/plans/', methods = ["POST"])
def generate_plan():
    try:
        data = request.get_json()

        if not data or 'instructions' not in data:
            return jsonify({"error": "Missing 'instructions' in request body"}), 400

        user_prompt = data['instructions']

        full_plan = asyncio.run(plan_week(user_prompt))

        return jsonify({
            "success": True,
            "plan": full_plan
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500