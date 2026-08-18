import json
import re

from google import genai
from google.genai.errors import ClientError, ServerError

from backend.app.config import GOOGLE_API_KEY, MODEL_NAME


client = genai.Client(api_key=GOOGLE_API_KEY)


def extract_json(text: str):
    """
    Extract the first JSON object from Gemini's response.
    """

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in response.")

    return json.loads(match.group())


def generate(prompt):
    try:

        print(f"Using model: {MODEL_NAME}")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        raw_text = response.text.strip()

        print(
            "\n================ RAW GEMINI RESPONSE ================\n"
        )

        print(raw_text)

        print(
            "\n=====================================================\n"
        )


        data = extract_json(raw_text)


        print(
            "\n================ PARSED JSON =========================\n"
        )

        print(
            json.dumps(
                data,
                indent=4
            )
        )

        print(
            "\n=====================================================\n"
        )


        return {
            "success": True,
            "data": data
        }


    # =========================================
    # JSON ERROR
    # =========================================

    except json.JSONDecodeError as e:

        print("\n******** JSON PARSE ERROR ********")

        print(e)

        return {
            "success": False,
            "error": f"JSON Parse Error: {e}"
        }


    # =========================================
    # CLIENT ERROR
    # =========================================

    except ClientError as e:

        print("\n******** GEMINI CLIENT ERROR ********")

        print(e)


        error_text = str(e)


        # Gemini quota / rate limit
        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            return {
                "success": False,
                "error": (
                    "Gemini API quota has been exhausted. "
                    "Please wait for the quota to reset or "
                    "use a higher API tier."
                )
            }


        # Model not found / unavailable
        if (
            "404" in error_text
            or "NOT_FOUND" in error_text
        ):

            return {
                "success": False,
                "error": (
                    f"Gemini model '{MODEL_NAME}' "
                    "is unavailable. Please select "
                    "an available model in config.py."
                )
            }


        return {
            "success": False,
            "error": f"Gemini Client Error: {e}"
        }


    # =========================================
    # SERVER ERROR
    # =========================================

    except ServerError as e:

        print("\n******** GEMINI SERVER ERROR ********")

        print(e)

        return {
            "success": False,
            "error": f"Gemini Server Error: {e}"
        }


    # =========================================
    # UNKNOWN ERROR
    # =========================================

    except Exception as e:

        print("\n******** UNKNOWN ERROR ********")

        print(type(e))

        print(e)

        return {
            "success": False,
            "error": "AI service is temporarily unavailable. Please try again."
        }