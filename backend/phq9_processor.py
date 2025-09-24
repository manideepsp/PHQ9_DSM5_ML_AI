from models import PHQ9Assessment, DSM5Assessment
import dsm_5_assessment
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def save_dsm5_assessment(user_id, severity, q9_flag, mdd_assessment):
    session = Session()
    try:
        dsm5 = DSM5Assessment(
            user_id=user_id,
            severity=severity,
            q9_flag=str(q9_flag).lower(),
            mdd_assessment=mdd_assessment
        )
        session.add(dsm5)
        session.commit()
        return {"status": "success", "dsm5_id": dsm5.id}
    except Exception as e:
        session.rollback()
        print(f"Error saving DSM-5 assessment: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        session.close()

def process_phq9_submission(user_id, responses, total_score, doctors_notes="", patients_notes=""):
    print(f"Processing PHQ-9 submission for user_id: {user_id}")
    print(f"Responses: {responses}")
    print(f"Total Score: {total_score}")
    print(f"Doctor's Notes: {doctors_notes}")
    print(f"Patient's Notes: {patients_notes}")
    print(f"type of responses: {type(responses)}") #dictionary

    severity, q9_flag, mdd_assessment = dsm_5_assessment.dsm_5_assessment(responses, total_score)

    session = Session()
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
        # Save DSM-5 assessment as well
        save_dsm5_assessment(user_id, severity, q9_flag, mdd_assessment)
        return {"status": "success", "assessment_id": assessment.id}
    except Exception as e:
        session.rollback()
        print(f"Error saving assessment: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        session.close()
