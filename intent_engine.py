def evaluate_intent(detail: dict) -> list:
    """
    Evaluate plausible intent hypotheses for a security-relevant event.
    Each hypothesis includes risk, confidence, explanation, and
    recommended next actions.
    """

    event_name = detail.get("eventName")
    user = detail.get("userIdentity", {}).get("userName", "unknown")
    context = detail.get("context", {})

    hypotheses = []

    # ---------- Base signals ----------
    privilege_change_events = {
        "AttachRolePolicy",
        "PutRolePolicy",
        "CreateRole"
    }

    is_privilege_change = event_name in privilege_change_events
    is_on_call = context.get("on_call", False)
    incident_active = context.get("incident_active", False)
    new_location = context.get("new_location", False)

    # ==========================================================
    # Hypothesis 1: Potentially malicious / risky intent
    # ==========================================================

    risk_score = 0.4
    confidence = 0.2
    reasons = []
    actions = []

    if is_privilege_change:
        risk_score += 0.3
        reasons.append("Privilege-affecting IAM action")
        actions.append("Review policy scope and permissions granted")

    if new_location:
        risk_score += 0.2
        reasons.append("Action from new or unusual location")
        actions.append("Validate user login location and device")

    if is_on_call:
        risk_score -= 0.2
        reasons.append("User was on-call (risk reduced)")

    if incident_active:
        risk_score -= 0.1
        reasons.append("Incident response context")

    if risk_score >= 0.7:
        actions.append("Escalate for security review")
        actions.append("Check recent activity for privilege chaining")
    else:
        actions.append("Monitor subsequent activity")

    hypotheses.append({
        "intent": "potentially_malicious",
        "actor": user,
        "risk_score": round(min(risk_score, 1.0), 2),
        "confidence": round(confidence, 2),
        "explanation": reasons,
        "recommended_actions": actions
    })

    # ==========================================================
    # Hypothesis 2: Legitimate administrative activity
    # ==========================================================

    legit_score = 0.6
    legit_confidence = 0.4
    legit_reasons = []
    legit_actions = []

    if is_privilege_change:
        legit_reasons.append("Change aligns with administrative responsibilities")
        legit_actions.append("Ensure change is documented")

    if is_on_call:
        legit_score += 0.2
        legit_confidence += 0.2
        legit_reasons.append("User on-call supports legitimacy")
        legit_actions.append("Correlate with incident ticket")

    if incident_active:
        legit_score += 0.2
        legit_confidence += 0.2
        legit_reasons.append("Incident response likely required change")
        legit_actions.append("Confirm change aligns with remediation steps")

    if new_location:
        legit_score -= 0.2
        legit_reasons.append("Unusual location weakens legitimacy")
        legit_actions.append("Perform secondary identity verification")

    if legit_score >= 0.7:
        legit_actions.append("No immediate action required")
    else:
        legit_actions.append("Light review recommended")

    hypotheses.append({
        "intent": "legitimate_admin_activity",
        "actor": user,
        "likelihood": round(min(legit_score, 1.0), 2),
        "confidence": round(min(legit_confidence, 1.0), 2),
        "explanation": legit_reasons,
        "recommended_actions": legit_actions
    })

    return hypotheses