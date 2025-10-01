# app/services/dsm5_service.py
from app.models import DSM5Assessment

def dsm_5_severity(total_score:int) -> str:
    if total_score >= 20:
        return "Severe depression"
    elif total_score >= 15:
        return "Moderately severe depression"
    elif total_score >= 10:
        return "Moderate depression"
    elif total_score >= 5:
        return "Mild depression"
    return "No depression"

def assess_mdd(responses):
    rule1 = sum(1 for v in responses.values() if v >= 2) >= 5
    rule2 = responses.get('1', 0) >= 2 or responses.get('2', 0) >= 2
    return rule1 and rule2

def dsm_5_assessment(responses, total_score):
    severity = dsm_5_severity(total_score)
    q9_flag = responses.get('9', 0) >= 2
    mdd_assessment = assess_mdd(responses)
    return severity, q9_flag, mdd_assessment

def save_dsm5_assessment(session, user_id, severity, q9_flag, mdd_assessment):
    dsm5 = DSM5Assessment(
        user_id=user_id,
        severity=severity,
        q9_flag=str(q9_flag).lower(),
        mdd_assessment=mdd_assessment
    )
    session.add(dsm5)
    session.commit()
    return {"status": "success", "dsm5_id": dsm5.id}
