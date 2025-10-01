# routes/dashboard.py
from flask import Blueprint, jsonify
from your_app import Session  # your session factory
from services.dashboard_service import get_triage_lists

bp = Blueprint("dashboard", __name__, url_prefix="/api")

@bp.route("/triage", methods=["GET"])
def triage():
    db = Session()
    try:
        data = get_triage_lists(db)
        return jsonify(data), 200
    finally:
        db.close()
