def evaluate_intent(detail: dict) -> list:
    
    event_name = detail.get("eventName")
    user = detail.get("userIdentity", {}).get("userName", "unknown")
    context = detail.get("context", {})

    hypotheses = []

    risk_score = 0.5
    confidence = 0.2
    reasons = []

    if event_name in ["AttachRolePolicy", "PutRolePolicy", "CreateRole"]:
        risk_score += 0.3
        reasons.append("Privilege-affecting IAM action")

    if context.get("on_call"):
        risk_score -= 0.2
        confidence += 0.3
        reasons.append("User was on-call")

    hypotheses.append({
        "intent": "potentially_suspicious",
        "actor": user,
        "risk_score": round(risk_score, 2),
        "confidence": round(confidence, 2),
        "reasons": reasons
    })

    return hypotheses