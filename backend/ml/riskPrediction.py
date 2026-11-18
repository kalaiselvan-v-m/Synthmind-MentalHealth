
"""
SynthMind risk prediction.

The current training dataset is too small for reliable ML predictions.
Until a sufficiently validated model is available, return Unavailable.
The rule-based risk assessment remains active in riskService.py.
"""

def predictRiskML(
    stress_score,
    support_level,
    low_mood_count,
    negative_emotion_count
):
    return "Unavailable"
