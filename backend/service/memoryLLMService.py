import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"


def safeParseMemory(content: str):
    try:
        # Remove markdown code fences if model adds them
        content = content.strip()
        content = content.replace("```json", "").replace("```", "").strip()

        # Extract JSON array safely
        match = re.search(r"\[.*\]", content, re.DOTALL)
        if not match:
            return []

        data = json.loads(match.group())

        if not isinstance(data, list):
            return []

        cleaned = []

        for item in data:
            if not isinstance(item, dict):
                continue

            memoryType = item.get("type", "").strip()
            memoryKey = item.get("key", "").strip()
            memoryValue = item.get("value", "").strip()
            importance = item.get("importance", 1)

            # Block placeholder/template memories
            if memoryKey in ["short_key", "mention", "key"]:
                continue

            if "clear human-readable memory" in memoryValue.lower():
                continue

            if memoryType not in ["preference", "stress_trigger", "emotion_pattern"]:
                continue

            if not memoryKey or not memoryValue:
                continue

            try:
                importance = int(importance)
            except:
                importance = 1

            importance = max(1, min(importance, 3))

            cleaned.append({
                "type": memoryType,
                "key": memoryKey,
                "value": memoryValue,
                "importance": importance
            })

        return cleaned

    except Exception as e:
        print("MEMORY PARSE ERROR:", str(e))
        return []


def extractMemoryWithLLM(message: str):
    prompt = f"""
You extract useful long-term memory from a user message.

User message:
"{message}"

Return JSON ONLY.
Do not explain.
Do not use markdown.
Do not copy examples.

Valid memory types:
- preference
- stress_trigger
- emotion_pattern

Return format:
[
  {{
    "type": "preference",
    "key": "casual_tone",
    "value": "User prefers casual friendly tone",
    "importance": 2
  }}
]

Rules:
- Extract only useful information for future conversations.
- Ignore simple casual messages like "hi", "hello", "lol", "ok".
- Do NOT return placeholder values like "short_key" or "clear human-readable memory".
- Use snake_case for key.
- importance must be 1, 2, or 3.

Examples:

User message: "talk like a friend bro"
Output:
[
  {{
    "type": "preference",
    "key": "casual_tone",
    "value": "User prefers casual friendly tone",
    "importance": 2
  }}
]

User message: "i have exam tomorrow and im anxious"
Output:
[
  {{
    "type": "stress_trigger",
    "key": "exam_stress",
    "value": "User feels stressed about exams",
    "importance": 3
  }},
  {{
    "type": "emotion_pattern",
    "key": "anxiety_pattern",
    "value": "User has mentioned anxiety",
    "importance": 3
  }}
]

User message: "hi"
Output:
[]

Now extract memory from the user message.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=60)
        data = res.json()

        content = data.get("message", {}).get("content", "[]")

        return safeParseMemory(content)

    except Exception as e:
        print("MEMORY LLM ERROR:", str(e))
        return []