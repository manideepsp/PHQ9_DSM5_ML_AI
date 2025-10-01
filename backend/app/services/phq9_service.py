# app/services/phq9_service.py
from app.models import PHQ9Assessment, DSM5Assessment
from app.db import SessionLocal
from app.services.dsm5_service import dsm_5_assessment, save_dsm5_assessment

def process_phq9_submission(user_id, responses, total_score, doctors_notes="", patients_notes=""):
    severity, q9_flag, mdd_assessment = dsm_5_assessment(responses, total_score)
    session = SessionLocal()
    try:
        assessment = PHQ9Assessment(
            user_id=user_id,
            responses=responses,
            total_score=total_score,
            doctors_notes=doctors_notes,
            patients_notes=patients_notes
        )
        session.add(assessment)
        session.commit()
        save_dsm5_assessment(session, user_id, severity, q9_flag, mdd_assessment)
        return {"status": "success", "assessment_id": assessment.id}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        session.close()
