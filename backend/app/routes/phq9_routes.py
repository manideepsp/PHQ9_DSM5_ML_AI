# app/routes/phq9_routes.py
from flask import Blueprint, request, jsonify
from app.services.phq9_service import process_phq9_submission

phq9_bp = Blueprint('phq9', __name__)

@phq9_bp.route('/api/phq9', methods=['POST'])
def phq9():
    data = request.get_json()
    result = process_phq9_submission(
        user_id=data.get('user_id'),
        responses=data.get('responses'),
        total_score=data.get('totalScore'),
        doctors_notes=data.get('doctors_notes', ""),
        patients_notes=data.get('patients_notes', "")
    )
    return jsonify(result), 200
