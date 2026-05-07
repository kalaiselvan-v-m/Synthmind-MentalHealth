import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"


# -----------------------------------
# 🔥 SAFE PARSE
# -----------------------------------
def safeParseMemory(content: str):

    try:
        content = content.strip()

        # remove markdown
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # extract JSON array safely
        match = re.search(r"\[.*\]", content, re.DOTALL)

        if not match:
            return []

        data = json.loads(match.group())

        if not isinstance(data, list):
            return []

        cleaned = []

        validTypes = [
            "preference",
            "stress_trigger",
            "emotion_pattern",
            "coping_strategy",
            "goal",
            "recurring_issue",
            "positive_progress"
        ]

        blockedKeys = [
            "short_key",
            "mention",
            "key"
        ]

        for item in data:

            if not isinstance(item, dict):
                continue

            memoryType = item.get("type", "").strip()
            memoryKey = item.get("key", "").strip()
            memoryValue = item.get("value", "").strip()
            importance = item.get("importance", 1)

            # -----------------------------------
            # BLOCK INVALID TYPES
            # -----------------------------------
            if memoryType not in validTypes:
                continue

            # -----------------------------------
            # BLOCK BAD PLACEHOLDERS
            # -----------------------------------
            if memoryKey in blockedKeys:
                continue

            if (
                "clear human-readable memory"
                in memoryValue.lower()
            ):
                continue

            if not memoryKey or not memoryValue:
                continue

            # -----------------------------------
            # IMPORTANCE CLEANUP
            # -----------------------------------
            try:
                importance = int(importance)
            except Exception:
                importance = 1

            importance = max(1, min(importance, 5))

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


# -----------------------------------
# 🔥 MAIN MEMORY EXTRACTION
# -----------------------------------
def extractMemoryWithLLM(message: str):

    prompt = f"""
You extract emotionally useful long-term memory from a user's message.

USER MESSAGE:
"{message}"

IMPORTANT:
Return ONLY JSON.
No markdown.
No explanation.
No extra text.

-----------------------------------
VALID MEMORY TYPES
-----------------------------------

- preference
- stress_trigger
- emotion_pattern
- coping_strategy
- goal
- recurring_issue
- positive_progress

-----------------------------------
RULES
-----------------------------------

1. Extract only information useful for future emotional conversations.

2. Ignore meaningless casual messages:
- hi
- hello
- lol
- ok
- nice
- thanks

3. Use short snake_case keys.

4. Memory value must sound natural and human-readable.

5. Do NOT invent severe mental conditions.

6. importance must be:
1 = weak
2 = useful
3 = important
4 = very important
5 = core recurring pattern

7. Never output placeholders like:
- short_key
- mention
- clear human-readable memory

-----------------------------------
GOOD EXAMPLES
-----------------------------------

User:
"talk casually bro"

Output:
[
  {{
    "type": "preference",
    "key": "casual_tone",
    "value": "User prefers a casual conversational tone.",
    "importance": 2
  }}
]

-----------------------------------

User:
"i get stressed before exams"

Output:
[
  {{
    "type": "stress_trigger",
    "key": "academic_pressure",
    "value": "User often feels stressed before exams.",
    "importance": 4
  }}
]

-----------------------------------

User:
"music helps calm me down"

Output:
[
  {{
    "type": "coping_strategy",
    "key": "music_calming",
    "value": "Listening to music helps the user calm down.",
    "importance": 3
  }}
]

-----------------------------------

User:
"i want to become more confident"

Output:
[
  {{
    "type": "goal",
    "key": "confidence_growth",
    "value": "User wants to improve confidence.",
    "importance": 3
  }}
]

-----------------------------------

User:
"i've been overthinking every night lately"

Output:
[
  {{
    "type": "recurring_issue",
    "key": "night_overthinking",
    "value": "User tends to overthink at night.",
    "importance": 4
  }}
]

-----------------------------------

User:
"journaling actually helped this week"

Output:
[
  {{
    "type": "positive_progress",
    "key": "journaling_helpful",
    "value": "Journaling has recently helped the user emotionally.",
    "importance": 3
  }}
]

-----------------------------------

User:
"hi"

Output:
[]

-----------------------------------

Now extract memory from the USER MESSAGE.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    try:
        res = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        data = res.json()

        content = (
            data
            .get("message", {})
            .get("content", "[]")
        )

        return safeParseMemory(content)

    except Exception as e:
        print("MEMORY LLM ERROR:", str(e))
        return []