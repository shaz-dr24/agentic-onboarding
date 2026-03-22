from flask import Blueprint, jsonify
from services.onboarding_service import run_onboarding

workflow_bp = Blueprint("workflow", __name__)

@workflow_bp.route("/start_onboarding/<int:emp_id>", methods=["GET"])
def start(emp_id):
    status = run_onboarding(emp_id)
    return jsonify({"status": status})