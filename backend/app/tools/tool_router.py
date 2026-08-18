import re


class ToolRouter:
    """
    Decides which tool should handle the user's query.
    """

    def __init__(self):
        self.web_keywords = [
            "today",
            "latest",
            "news",
            "current",
            "breaking",
            "headline",
            "recent",
            "update",
            "updates",
            "live"
        ]

        self.weather_keywords = [
            "weather",
            "temperature",
            "rain",
            "forecast",
            "humidity",
            "wind"
        ]

    def is_math(self, query: str) -> bool:
        query = query.replace(" ", "")
        return bool(re.fullmatch(r"[0-9+\-*/().%]+", query))

    def detect(self, query: str):

        q = query.lower()

        # Calculator
        if self.is_math(q):
            return {
                "tool": "CALCULATOR",
                "reason": "Mathematical expression detected."
            }

        # Weather
        if any(word in q for word in self.weather_keywords):
            return {
                "tool": "WEATHER",
                "reason": "Weather-related query."
            }

        # Web Search
        if any(word in q for word in self.web_keywords):
            return {
                "tool": "WEB_SEARCH",
                "reason": "Latest or real-time information requested."
            }

        # Default
        return {
            "tool": "LLM",
            "reason": "General knowledge query."
        }

    def extract_city(self, query: str):
        """
        Extract city name from a weather query.
        """

        query = query.lower()

        query = re.sub(
            r"\b(weather|temperature|forecast|rain|humidity|wind|in|of|at|for|today|current)\b",
            "",
            query,
        )

        city = " ".join(query.split()).title()

        if city:
            return city

        return None


router = ToolRouter()