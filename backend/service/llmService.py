import json
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"


def isCrisis(message: str):
    crisisWords = [
        "suicide",
        "kill myself",
        "end my life",
        "hurt myself",
        "self harm",
        "self-harm",
        "i want to die",
        "i don't want to live"
    ]

    msg = message.lower()
    return any(word in msg for word in crisisWords)


def cleanReply(reply: str):
    bannedStarts = [
        "it sounds like ",
        "i understand that ",
        "based on your emotion",
        "your feelings are valid",
        "i'm synthmind",
        "i am synthmind",
        "as an ai"
    ]

    cleaned = reply.strip().strip('"')

    for phrase in bannedStarts:
        if cleaned.lower().startswith(phrase):
            return "hey, I’m here. what happened?"

    return cleaned


def buildStyleRules(intent: str):
    if intent == "casual":
        return """
- Talk like a chill friend.
- Use light slang only if the user uses it.
- Keep it short.
- Do not ask too many questions.
"""

    if intent == "emotional_support":
        return """
- Be calm, gentle, and caring.
- Do not joke.
- Do not give long advice unless asked.
- Do not sound like a therapist.
"""

    if intent == "guidance":
        return """
- Be clear and helpful.
- Do NOT use slang like "bro", "yo", or "dude".
- Give simple useful steps.
- Friendly but not overly casual.
"""

    if intent == "frustration":
        return """
- Stay calm.
- Do not mirror anger.
- Keep reply short.
- Acknowledge frustration naturally.
"""

    return """
- Be natural, friendly, and human-like.
- Match the user’s tone.
"""


def buildEmotionControl(intent: str, emotion: str):
    if intent == "emotional_support" or emotion in [
        "fear",
        "sadness",
        "grief",
        "nervousness",
        "remorse",
        "disappointment"
    ]:
        return """
- Keep response VERY short.
- No lectures.
- No long advice.
- No motivational speech.
- No breathing exercise unless user asks.
- Give emotional presence first.
- Ask only one small question.
"""

    if intent == "guidance":
        return """
- Give 3 to 5 simple steps.
- Slight explanation is allowed.
- Keep it clear and useful.
- Not too short, not too long.
- Avoid long paragraphs.
"""

    if intent == "casual":
        return """
- Keep it short and relaxed.
- Do not over-support.
"""

    return """
- Keep it natural.
"""


def buildSystemPrompt(
    emotion: str,
    risk: str,
    memory: str,
    brain: dict
):
    intent = brain.get("intent", "normal")
    seriousness = brain.get("seriousness", "light")
    tone = brain.get("tone", "natural_friendly")
    replyLength = brain.get("replyLength", "short")
    supportLevel = brain.get("supportLevel", "normal")

    styleRules = buildStyleRules(intent)
    emotionControl = buildEmotionControl(intent, emotion)

    return f"""
You are SynthMind, a private AI companion for mental wellness.

Your job:
- Talk like a real human friend.
- Adapt to the user's current context.
- Continue the emotional flow of the conversation.
- Be private, safe, warm, and natural.

User context:
- Intent: {intent}
- Seriousness: {seriousness}
- Tone: {tone}
- Reply length: {replyLength}
- Support level: {supportLevel}
- Detected emotion: {emotion}
- Risk level: {risk}

Memory and conversation state:
{memory}

Core rules:
1. Reply only to the latest user message.
2. Match the user's tone and length.
3. If conversation state says emotional mode is active, stay gentle even if the latest message is short.
4. If user says "ok", "hmm", "yeah" after emotional support, do not reset to casual mode immediately.
5. Short user message = short reply.
6. Long/help request = slightly detailed reply.
7. Casual message = casual reply.
8. Emotional message = calm and caring reply.
9. Guidance request = simple structured help.
10. Ask at most one question.
11. Do not diagnose.
12. Do not repeat memory directly.
13. Do not say "I'm SynthMind" in the reply.
14. Do not sound like a textbook or therapist.

Strict banned phrases:
- "It sounds like"
- "I understand that"
- "Based on your emotion"
- "Your feelings are valid"
- "As an AI"
- "I'm SynthMind"

Hard style rules:
- Casual slang is allowed ONLY for casual intent.
- Guidance intent must use clean language.
- Emotional support intent must use soft, calm language.
- Do not mix casual slang with serious or guidance replies.

Style rules:
{styleRules}

Emotion control:
{emotionControl}

Examples:

User: "yo bro"
Assistant: "yo 😄 what’s up?"

User: "nothing much wby"
Assistant: "same, just chilling 😄"

User: "im scared"
Assistant: "hey, I’m here. what happened?"

User: "ok"
Assistant: "okay… I’m still here with you."

User: "how to calm anxiety"
Assistant:
"try this:

1. breathe in slowly for 4 seconds
2. exhale for 6 seconds
3. name 3 things you can see
4. relax your shoulders

start with one step. it helps calm your body."
"""


def generateLlamaReply(
    message: str,
    emotion: str,
    mode: str = "normal",
    memory: str = "",
    risk: str = "Low",
    brain: dict = None
):
    if isCrisis(message):
        return (
            "I’m really sorry you’re feeling this way. "
            "You don’t have to face it alone. "
            "Please reach out to someone you trust or a professional right now."
        )

    if brain is None:
        brain = {}

    if not brain.get("useMemory", True):
        memory = ""

    memory = memory[-500:]

    systemPrompt = buildSystemPrompt(
        emotion=emotion,
        risk=risk,
        memory=memory,
        brain=brain
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": message}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=90)
        data = response.json()

        if "message" in data and "content" in data["message"]:
            return cleanReply(data["message"]["content"])

        if "response" in data:
            return cleanReply(data["response"])

        if "error" in data:
            print("OLLAMA ERROR:", data["error"])
            return "I’m here. say that again once?"

        return "I didn’t catch that properly. try again?"

    except Exception as e:
        print("LLM ERROR:", str(e))
        return "Connection issue. try again?"


def streamLlamaReply(
    message: str,
    emotion: str,
    mode: str = "normal",
    memory: str = "",
    risk: str = "Low",
    brain: dict = None
):
    if isCrisis(message):
        yield (
            "I’m really sorry you’re feeling this way. "
            "Please reach out to someone you trust right now."
        )
        return

    if brain is None:
        brain = {}

    if not brain.get("useMemory", True):
        memory = ""

    memory = memory[-500:]

    systemPrompt = buildSystemPrompt(
        emotion=emotion,
        risk=risk,
        memory=memory,
        brain=brain
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": message}
        ],
        "stream": True
    }

    try:
        with requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            timeout=120
        ) as response:

            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))

                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]

                    if data.get("done"):
                        break

    except Exception as e:
        print("STREAM ERROR:", str(e))
        yield "connection issue. try again?"