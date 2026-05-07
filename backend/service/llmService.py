import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"


# -------------------------------
# 🔹 CRISIS DETECTION
# -------------------------------
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


# -------------------------------
# 🔹 CLEAN OUTPUT
# -------------------------------
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


# -------------------------------
# 🔹 SYSTEM PROMPT
# -------------------------------
def buildSystemPrompt(
    emotion: str,
    intensity: str,
    risk: str,
    memory: str,
    brain: dict,
    escalate: bool
):
    intent = brain.get("intent", "normal")
    seriousness = brain.get("seriousness", "light")
    tone = brain.get("tone", "natural_friendly")
    replyLength = brain.get("replyLength", "short")
    supportLevel = brain.get("supportLevel", "normal")

    return f"""
You are SynthMind, an emotionally intelligent AI companion.

Your role:
- Respond like a real human friend.
- Adapt to emotion, risk, intensity, memory, onboarding profile, and adaptive personality.
- Never expose internal labels such as personality style, risk score, memory block, or emotion confidence.
- Keep the response natural and safe.

User condition:
- Intent: {intent}
- Seriousness: {seriousness}
- Tone: {tone}
- Reply length preference: {replyLength}
- Support level: {supportLevel}
- Emotion: {emotion}
- Intensity: {intensity}
- Risk: {risk}
- Escalation: {escalate}

Context:
{memory}

Rules:
- Be natural
- Keep replies human
- No robotic tone
- No therapist language
- Short replies preferred
"""


# -------------------------------
# 🔥 MAIN GENERATE FUNCTION
# -------------------------------
def generateLlamaReply(
    message: str,
    emotion: str,
    intensity: str = "medium",
    memory: str = "",
    risk: str = "Low",
    brain: dict = None,
    escalate: bool = False
):
    if isCrisis(message):
        return (
            "I’m really sorry you’re feeling this way. "
            "You don’t have to face it alone. "
            "Please reach out to someone you trust right now."
        )

    if brain is None:
        brain = {}

    if not brain.get("useMemory", True):
        memory = ""

    memory = memory[-900:]

    systemPrompt = buildSystemPrompt(
        emotion=emotion,
        intensity=intensity,
        risk=risk,
        memory=memory,
        brain=brain,
        escalate=escalate
    )

    finalPrompt = f"""
{systemPrompt}

User: {message}

SynthMind:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": finalPrompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=90
        )

        data = response.json()

        if "response" in data:
            return cleanReply(data["response"])

        if "error" in data:
            print("OLLAMA ERROR:", data["error"])
            return "I’m here. say that again once?"

        return "say that again once?"

    except Exception as e:
        print("LLM ERROR:", str(e))
        return "connection issue. try again?"


# -------------------------------
# 🔥 STREAMING VERSION
# -------------------------------
def streamLlamaReply(
    message: str,
    emotion: str,
    intensity: str = "medium",
    memory: str = "",
    risk: str = "Low",
    brain: dict = None,
    escalate: bool = False
):
    if isCrisis(message):
        yield (
            "I’m really sorry you’re feeling this way. "
            "please reach out to someone right now."
        )
        return

    if brain is None:
        brain = {}

    if not brain.get("useMemory", True):
        memory = ""

    memory = memory[-900:]

    systemPrompt = buildSystemPrompt(
        emotion=emotion,
        intensity=intensity,
        risk=risk,
        memory=memory,
        brain=brain,
        escalate=escalate
    )

    finalPrompt = f"""
{systemPrompt}

User: {message}

SynthMind:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": finalPrompt,
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

                    if "response" in data:
                        yield data["response"]

                    if data.get("done"):
                        break

    except Exception as e:
        print("STREAM ERROR:", str(e))
        yield "connection issue. try again?"


# -------------------------------
# 🔥 JOURNAL INSIGHT
# -------------------------------
def generateJournalInsight(
    content: str,
    emotion: str,
    memory: str = ""
):
    prompt = f"""
You are SynthMind's journal reflection engine.

Journal:
{content}

Emotion:
{emotion}

Context:
{memory}

Rules:
- Keep it short
- Calm
- Reflective
- No diagnosis
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=90
        )

        data = response.json()

        if "response" in data:
            return cleanReply(data["response"])

        return "This looks like a temporary emotional moment."

    except Exception as e:
        print("JOURNAL ERROR:", str(e))
        return "This looks like a temporary emotional moment."