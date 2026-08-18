import requests
from backend.app.config import OPENWEATHER_API_KEY


def get_weather(city):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    print(response.status_code)
    print(response.text)

    if response.status_code != 200:
        return {
            "success": False,
            "error": "Weather not found."
        }

    data = response.json()

    return {
        "success": True,
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"]
    }