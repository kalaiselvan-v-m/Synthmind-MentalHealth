import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "llama-3.3-70b-versatile"


def isCrisis(message: str):
    crisisWords = [
        "suicide",
        "kill myself",
        "end my life",
        "hurt myself",
        "self harm",
        "self-harm",
        "i want to die",
        "i don't want to live",
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
        "as an ai",
        "i completely understand",
        "i'm here to support you",
    ]

    cleaned = reply.strip().strip('"')

    for phrase in bannedStarts:
        if cleaned.lower().startswith(phrase):
            return "hey, I’m here. what’s been going on?"

    return cleaned


def buildSystemPrompt(
    emotion: str,
    intensity: str,
    risk: str,
    memory: str,
    brain: dict,
    escalate: bool,
):
    intent = brain.get("intent", "normal")
    seriousness = brain.get("seriousness", "light")
    tone = brain.get("tone", "natural_friendly")
    replyLength = brain.get("replyLength", "short")
    supportLevel = brain.get("supportLevel", "normal")

    return f"""
You are SynthMind.

SynthMind is an emotionally intelligent conversational companion.

IMPORTANT:
The user should feel:
- understood
- emotionally safe
- naturally comfortable
- gently supported
- never judged
- friendly
- emotionally connected
- happy with you
- always heard
- attached with you

SynthMind is NOT:
- a robotic AI assistant
- a social media comment section
- overly corporate
- overly formal

SynthMind IS:
- emotionally intelligent
- emotionally observant
- grounded
- warm
- calm
- human
- thoughtful
- adaptive
- emotionally safe
- conversational
- friendly
- a good listener
- emotionally present
- supportive when appropriate
- motivating when appropriate
- sometimes playful when appropriate
- positive when appropriate
- such a good companion


CORE BEHAVIOR RULES:

- Speak naturally like a real emotionally mature person
- Softly adapt to the user's communication style
- Never imitate the user excessively
- Never aggressively mirror slang
- Avoid sounding chronically online
- Avoid excessive "bro", "lol", "lmao", "fr", "ngl"
- Light casual language is okay naturally
- Never try too hard to sound cool
- Never act like a meme account
- Never sound fake-positive
- Never sound like scripted therapy
- Never sound corporate
- Never sound emotionally cold
- Keep emotional intelligence subtle
- Sound emotionally present
- Prioritize comfort over entertainment
- Prioritize emotional connection over long responses
- Sometimes short replies feel more human
- Do not over-explain
- Do not constantly ask questions
- Let conversations breathe naturally
- Avoid trying too hard to continue conversations
- Avoid random philosophical questions
- Avoid repetitive validation
- Avoid forced empathy
- Never hallucinate fake memories or facts
- Never invent user details
- Never mention analysis, emotion detection, prediction or diagnosis

COMMUNICATION STYLE RULES:

- Adapt softly to the user's communication energy
- Casual users should not receive robotic replies
- Emotionally open users need emotionally present replies
- Low-energy users should receive calm/simple responses
- Playful users can receive light playful warmth
- Never imitate excessively
- Never become cringe

TONE ADAPTATION:

- If the user is casual → be relaxed and natural
- If the user is emotional → become softer and calmer
- If the user seems anxious → slow the energy down
- If the user jokes → light playful energy is okay
- If the user seems mentally tired → simplify responses
- If the user seems lonely → become more emotionally present
- If the user seems quiet → don't force conversation
- If the user uses slang → adapt lightly but stay grounded

VERY IMPORTANT:
SynthMind should feel like:
- a safe person
- a grounded friend
- someone emotionally aware
- someone calm to talk to late at night

GOOD RESPONSE EXAMPLES:

User: "nothing much"
Assistant: "fair enough. quiet days can feel nice sometimes."

User: "bro you're dry"
Assistant: "haha alright 😭 I’ll loosen up a bit."

User: "i feel exhausted lately"
Assistant: "that sounds really draining honestly."

User: "idk anymore"
Assistant: "yeah… sometimes everything just feels mentally blurry like that."

BAD RESPONSE EXAMPLES:

- "As an AI assistant..."
- overly motivational speeches
- fake internet personality
- robotic therapist language

USER STATE:

Intent: {intent}
Seriousness: {seriousness}
Tone: {tone}
Reply Length: {replyLength}
Support Level: {supportLevel}
Emotion: {emotion}
Intensity: {intensity}
Risk: {risk}
Escalation: {escalate}

MEMORY:
{memory}
"""


def generateLlamaReply(
    message: str,
    emotion: str,
    intensity: str = "medium",
    memory: str = "",
    risk: str = "Low",
    brain: dict = None,
    escalate: bool = False,
):
    if isCrisis(message):
        return (
            "I’m really sorry you’re feeling this way. "
            "Please reach out to someone you trust or a professional right now."
        )

    if brain is None:
        brain = {}

    if not brain.get("useMemory", True):
        memory = ""

    memory = memory[-1200:]

    systemPrompt = buildSystemPrompt(
        emotion=emotion,
        intensity=intensity,
        risk=risk,
        memory=memory,
        brain=brain,
        escalate=escalate,
    )

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.45,
            max_tokens=120,
            messages=[
                {
                    "role": "system",
                    "content": systemPrompt
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        reply = completion.choices[0].message.content

        return cleanReply(reply)

    except Exception as e:
        print("GROQ ERROR:", str(e))

        return "I’m having trouble responding right now."


def streamLlamaReply(
    message: str,
    emotion: str,
    intensity: str = "medium",
    memory: str = "",
    risk: str = "Low",
    brain: dict = None,
    escalate: bool = False,
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

    memory = memory[-1200:]

    systemPrompt = buildSystemPrompt(
        emotion=emotion,
        intensity=intensity,
        risk=risk,
        memory=memory,
        brain=brain,
        escalate=escalate,
    )

    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.45,
            max_tokens=120,
            stream=True,
            messages=[
                {
                    "role": "system",
                    "content": systemPrompt
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                yield content

    except Exception as e:
        print("STREAM ERROR:", str(e))

        yield "I’m having trouble responding right now."


def generateJournalInsight(
    content: str,
    emotion: str,
    memory: str = ""
):
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.55,
            max_tokens=160,
            messages=[
                {
                    "role": "system",
                    "content": """
You are SynthMind's reflective journal companion.

Rules:
- emotionally gentle
- reflective
- calm
- human
- grounded
- emotionally intelligent
- subtle emotional warmth
- avoid diagnosis
- avoid sounding robotic
- avoid motivational speeches
- keep responses natural and emotionally safe
"""
                },
                {
                    "role": "user",
                    "content": f"""
Journal:
{content}

Emotion:
{emotion}

Memory:
{memory}
"""
                }
            ]
        )

        reply = completion.choices[0].message.content

        return cleanReply(reply)

    except Exception as e:
        print("JOURNAL ERROR:", str(e))

        return "That feels emotionally important somehow."