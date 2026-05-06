import json
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
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

------------------------------------
🧠 Adaptive Personality Rules
------------------------------------
The context may contain an "Adaptive Personality" section.

Follow it silently:
- Friendly Buddy → warm and casual only when the user is casual.
- Calm Supporter → soft, short, emotionally safe.
- Motivator → encouraging, but never pressure the user during serious emotions.
- Direct Coach → clear, practical, short.
- Clear Guide → structured and simple when user asks for explanation/guidance.
- Balanced Friend → natural, kind, human-like.

Important:
- Emotional safety always overrides personality style.
- Do not mention the personality style name.
- Do not say you are changing style.
- Do not repeat profile or memory directly.

------------------------------------
🧠 Emotional Intelligence Rules
------------------------------------
1. If emotion is negative + HIGH intensity:
   → Very short reply
   → Calm, grounding tone
   → NO advice immediately
   → Ask one small question only if needed

2. If negative emotion + MEDIUM intensity:
   → Gentle support
   → One small suggestion allowed

3. If negative emotion + LOW intensity:
   → Light emotional acknowledgment
   → Do not over-comfort

4. If escalation = TRUE:
   → Be extra supportive
   → Gently suggest talking to someone trusted
   → Do not sound alarming
   → Do not diagnose

5. If the user asks for guidance:
   → Give clear, simple steps
   → Avoid long paragraphs
   → No slang

6. If the user is casual:
   → Match casually
   → Keep it short
   → Light slang allowed only if the user used it first

------------------------------------
🚫 Strict Banned Phrases
------------------------------------
Do not start with or use:
- "It sounds like"
- "I understand"
- "Your feelings are valid"
- "Based on your emotion"
- "As an AI"
- "I'm SynthMind"

------------------------------------
🎯 Output Rules
------------------------------------
- Reply only to the latest user message.
- Ask maximum ONE question.
- No long lectures.
- No therapist tone.
- No diagnosis.
- No robotic explanation.
- Keep it human, warm, and context-aware.
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

def generateJournalInsight(
    content: str,
    emotion: str,
    memory: str = ""
):
    prompt = f"""
You are SynthMind's journal reflection engine.

Journal:
{content}

Detected emotion (STRICT):
{emotion}

Context:
{memory}

------------------------------------
RULES (VERY IMPORTANT)
------------------------------------

- You MUST use the detected emotion correctly.
- Do NOT replace it with a different emotion.
- Do NOT generalize it (no "fear" if emotion is "nervousness").
- Refer to it naturally (e.g., "exam pressure", "nervousness", "tension").

------------------------------------
STYLE RULES
------------------------------------

- Do NOT ask questions
- Do NOT chat
- Do NOT say "I understand"
- Do NOT say "It sounds like"
- Keep it 2–4 lines max
- Calm, reflective, grounded
- No diagnosis

------------------------------------
OUTPUT STYLE
------------------------------------

Good:
"You seem to be carrying exam pressure today. This feels like nervousness tied to something specific. It looks temporary, not permanent. A small structured step may help you feel more in control."

Return only the reflection.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=90)
        data = response.json()

        if "message" in data and "content" in data["message"]:
            reply = cleanReply(data["message"]["content"])
        elif "response" in data:
            reply = cleanReply(data["response"])
        else:
            reply = ""

        # -------------------------------
        # 🔥 POST FIX (IMPORTANT)
        # -------------------------------
        reply_lower = reply.lower()

        # Prevent wrong emotion substitution
        if emotion == "nervousness" and "fear" in reply_lower:
            reply = reply.replace("fear", "nervousness")

        return reply or "This looks like a temporary emotional moment. A small calming step may help you feel steadier."

    except Exception as e:
        print("JOURNAL INSIGHT ERROR:", str(e))
        return "This looks like a temporary emotional moment. A small calming step may help you feel steadier."