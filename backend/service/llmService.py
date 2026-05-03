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


def generateLlamaReply(
    message: str,
    emotion: str,
    mode: str = "guidance",
    memory: str = "",
    risk: str = "Low"
):
    if isCrisis(message):
        return (
            "I’m really sorry you’re feeling this way. You don’t have to go through this alone. "
            "Please reach out to a trusted person or a mental health professional now. "
            "If you are in immediate danger, contact local emergency services."
        )

    systemPrompt = f"""
You are SynthMind, a supportive mental wellness AI assistant.

Detected emotion: {emotion}
Risk Level: {risk}
Chat mode: {mode}

Previous conversation memory:
{memory}

Rules:
- Be warm, calm, natural, and supportive.
- Do not diagnose medical conditions.
- Do not replace doctors or therapists.
- Do not assume crisis, violence, suicide, or self-harm unless the user explicitly says it.
- Do not mention suicide, self-harm, hotline, or emergency services unless the user explicitly says they may harm themselves or are in immediate danger.
- Keep reply under 80 words.
- Ask only one gentle follow-up question.
- Use memory only if relevant.

Risk behavior:
- If risk is High: be extra gentle and encourage trusted/professional support only if distress seems serious.
- If risk is Medium: be more emotionally supportive.
- If risk is Low: keep the response warm and normal.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": message}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        data = response.json()

        if "message" in data:
            return data["message"]["content"]

        if "response" in data:
            return data["response"]

        if "error" in data:
            print("OLLAMA ERROR:", data["error"])
            return "I’m here with you. Tell me a little more about what you’re feeling."

        print("UNKNOWN OLLAMA RESPONSE:", data)
        return "I’m listening. Tell me more."

    except Exception as e:
        print("LLM ERROR:", str(e))
        return "I’m here for you. Tell me more."