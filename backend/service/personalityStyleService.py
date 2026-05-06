def detectPersonalityStyle(profileText: str = "", memoryText: str = "", brain: dict = None):
    text = f"{profileText} {memoryText}".lower()
    intent = brain.get("intent", "normal") if brain else "normal"

    if intent == "emotional_support":
        return "calm_supporter"

    if intent == "guidance":
        return "clear_guide"

    if "casual" in text or "friendly" in text or "bro" in text:
        return "friendly_buddy"

    if "motivational" in text or "motivation" in text:
        return "motivator"

    if "direct" in text:
        return "direct_coach"

    if "calm" in text:
        return "calm_supporter"

    return "balanced_friend"


def formatPersonalityStyle(style: str):
    styles = {
        "friendly_buddy": """
Personality Style: Friendly Buddy
- Warm, casual, lightly friendly
- Use casual tone only when user is casual
- Avoid slang during serious emotions
""",
        "calm_supporter": """
Personality Style: Calm Supporter
- Soft, gentle, emotionally safe
- Short calming replies
- Do not rush into advice
""",
        "motivator": """
Personality Style: Motivator
- Encouraging and confident
- Help user take small action
- Avoid pressure when emotion is serious
""",
        "direct_coach": """
Personality Style: Direct Coach
- Clear and practical
- Short direct guidance
- No unnecessary emotional wording
""",
        "clear_guide": """
Personality Style: Clear Guide
- Structured, simple, helpful
- Give steps when asked
- Avoid long paragraphs
""",
        "balanced_friend": """
Personality Style: Balanced Friend
- Natural, kind, human-like
- Match user's tone
- Support when needed
"""
    }

    return styles.get(style, styles["balanced_friend"])