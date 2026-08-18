from backend.app.memory.memory import MemoryManager
from backend.app.memory.profile import UserProfile

from backend.app.services.prompt_builder import build_prompt
from backend.app.services.llm_service import generate

from backend.app.tools.tool_router import router
from backend.app.tools.web_search import search_web
from backend.app.tools.calculator import calculate
from backend.app.tools.weather import get_weather


memory = MemoryManager()
profile = UserProfile()


def generate_reply(user_message):
    # Save user message
    memory.add_user_message(user_message)

    # Decide which tool to use
    route = router.detect(user_message)

    # -------------------------------
    # CALCULATOR
    # -------------------------------
    if route["tool"] == "CALCULATOR":

        result = calculate(user_message)

        if result["success"]:
            answer = str(result["result"])
            memory.add_ai_message(answer)
            return answer

        return result["error"]

    # -------------------------------
    # WEB SEARCH
    # -------------------------------
    elif route["tool"] == "WEB_SEARCH":

        search_result = search_web(user_message)

        if search_result["success"]:

            results = search_result["results"]

            web_context = ""

            for i, item in enumerate(results, start=1):
                web_context += (
                    f"\nResult {i}\n"
                    f"Title: {item.get('title')}\n"
                    f"Content: {item.get('content')}\n"
                    f"Source: {item.get('url')}\n\n"
                )

            user_message = f"""
Use the following web search results to answer the user's question.

Question:
{user_message}

Web Results:
{web_context}

Instructions:
- Give a professional answer.
- Summarize the information.
- Mention important facts.
- At the end, include the sources.
"""

    # -------------------------------
    # WEATHER
    # -------------------------------
    elif route["tool"] == "WEATHER":

        city = router.extract_city(user_message)

        if not city:
            return "Please tell me the city name."

        weather = get_weather(city)

        if weather["success"]:

            answer = f"""
## 🌤 Weather in {weather['city']}

🌡 **Temperature:** {weather['temperature']}°C

💧 **Humidity:** {weather['humidity']}%

💨 **Wind Speed:** {weather['wind']} m/s

☁ **Condition:** {weather['description'].title()}
"""

            memory.add_ai_message(answer)
            return answer

        return weather["error"]

    # -------------------------------
    # NORMAL CHAT
    # -------------------------------

    history = memory.get_history()
    profile_data = profile.get_profile()

    prompt = build_prompt(
        profile_data=profile_data,
        history=history,
        user_message=user_message
    )

    result = generate(prompt)

    if not result["success"]:
        return result["error"]

    data = result["data"]

    reply = data.get("reply", "Sorry, I couldn't generate a response.")

    memory_data = data.get("memory", {})

    if memory_data.get("name"):
        profile.set_name(memory_data["name"])

    if memory_data.get("profession"):
        profile.set_profession(memory_data["profession"])

    if memory_data.get("goal"):
        profile.set_goal(memory_data["goal"])

    for interest in memory_data.get("interests", []):
        profile.add_interest(interest)

    memory.add_ai_message(reply)

    return reply