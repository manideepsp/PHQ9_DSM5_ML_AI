def dsm_5_severity(total_score):
    # Example DSM-5 based assessment logic
    if total_score >= 20:
        severity = "Severe depression"
    elif total_score >= 15:
        severity = "Moderately severe depression"
    elif total_score >= 10:
        severity = "Moderate depression"
    elif total_score >= 5:
        severity = "Mild depression"
    else:
        severity = "No depression"

    print(f"DSM-5 Assessment Severity: {severity}")
    return severity

def assess_mdd(responses):
    # Rule 1: Count responses with score >= 2
    num_responses_ge_2 = sum(1 for v in responses.values() if v >= 2)
    rule1 = num_responses_ge_2 >= 5

    # Rule 2: q1 >= 2 or q2 >= 2
    rule2 = responses.get('0', 0) >= 2 or responses.get('1', 0) >= 2

    # MDD assessment is positive if both rules are satisfied
    return rule1 and rule2

def dsm_5_assessment(responses, total_score):
    severity = dsm_5_severity(total_score)
    q9_flag = responses.get('8', 0) >= 2  # Check if there's any positive response to question 9
    mdd_assessment = assess_mdd(responses)

    
    return severity, q9_flag, mdd_assessment