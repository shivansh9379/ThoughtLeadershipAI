import json

from google import genai

from backend.app.config import GOOGLE_API_KEY

client = genai.Client(api_key=GOOGLE_API_KEY)


def extract_profile(user_message: str):

    prompt = f"""
You are an AI profile extractor.

Extract information from the user's message.

Return ONLY valid JSON.

JSON format:

{{
    "name": null,
    "profession": null,
    "goal": null,
    "interests": []
}}

Rules:

- If information is missing, return null.
- Do not explain anything.
- Do not write markdown.
- Return JSON only.

User Message:

{user_message}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        profile = json.loads(text)

        return profile

    except Exception as e:

        print("Profile Extraction Error:", e)

        return {
            "name": None,
            "profession": None,
            "goal": None,
            "interests": []
        }