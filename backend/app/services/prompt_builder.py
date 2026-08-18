import json


def build_prompt(profile_data, history, user_message):
    system_prompt = """
You are Core AI Engine.

Your task is to:
1. Reply naturally to the user.
2. Update the user's profile if new information is provided.

Return ONLY valid JSON.

Schema:

{
    "reply": "Assistant reply",
    "memory": {
        "name": null,
        "profession": null,
        "goal": null,
        "interests": []
    }
}

Rules:
- Return ONLY JSON.
- Do not add markdown.
- Do not use ```json.
- If a field is unknown, return null.
- Only update fields mentioned by the user.
"""

    prompt = f"""
{system_prompt}

Current User Profile:
{json.dumps(profile_data, indent=2)}

Conversation History:
{history}

Latest User Message:
{user_message}
"""

    return prompt