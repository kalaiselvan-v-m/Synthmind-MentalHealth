def updateConversationState(state: dict, message: str, emotion: str, brain: dict):
    if state is None:
        state = {}

    # 🔥 Track last intent
    state["lastIntent"] = brain.get("intent")

    # 🔥 Track emotional state
    if emotion in ["fear", "sadness", "anxiety"]:
        state["emotionalMode"] = True
    else:
        state["emotionalMode"] = False

    # 🔥 Track topic
    msg = message.lower()

    if "exam" in msg:
        state["topic"] = "exam"
    elif "interview" in msg:
        state["topic"] = "interview"

    # 🔥 Track seriousness
    state["seriousness"] = brain.get("seriousness", "light")

    return state