def generate_ai_profile(answers: dict):
    stress_score = 0
    risk_score = 0
    support_score = 0
    personality_points = []

    all_answers = []

    for value in answers.values():
        if isinstance(value, list):
            all_answers.extend(value)
        else:
            all_answers.append(value)

    for ans in all_answers:
        ans_lower = ans.lower()

        if ans_lower in ["running on empty", "up and down"]:
            stress_score += 25

        if ans_lower in ["yes, something big", "some things weighing on me"]:
            stress_score += 25
            risk_score += 20

        if ans_lower in ["no one, really", "i don’t reach out", "i don't reach out"]:
            support_score -= 20
            risk_score += 20

        if ans_lower in ["a few close people", "my family", "my partner", "plenty of people"]:
            support_score += 20

        if ans_lower in ["my future", "my career", "my health", "whether i’m on the right path"]:
            stress_score += 10

        if ans_lower in ["a bit too sensitive", "shy but deep inner world", "trusting my gut"]:
            personality_points.append(ans)

        if ans_lower in ["that i never give up", "that i keep going no matter what", "how i treat people"]:
            personality_points.append(ans)

    stress_score = min(stress_score, 100)
    risk_score = min(risk_score, 100)

    wellness_score = max(100 - stress_score, 10)

    if stress_score >= 70:
        emotional_state = "Overwhelmed"
    elif stress_score >= 40:
        emotional_state = "Emotionally loaded"
    else:
        emotional_state = "Stable"

    if support_score >= 20:
        support_level = "Good support system"
    elif support_score == 0:
        support_level = "Moderate support system"
    else:
        support_level = "Low support system"

    if risk_score >= 60:
        risk_level = "High"
    elif risk_score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    personality_summary = (
        ", ".join(personality_points)
        if personality_points
        else "Reflective and emotionally aware"
    )

    return {
        "stress_score": stress_score,
        "wellness_score": wellness_score,
        "emotional_state": emotional_state,
        "support_level": support_level,
        "risk_level": risk_level,
        "personality_summary": personality_summary,
    }