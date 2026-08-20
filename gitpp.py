import os
import requests
from dotenv import load_dotenv

load_dotenv()  # reads .env and loads variables into environment

load_dotenv()
print("Key loaded:", repr(os.getenv("OPENWEATHER_API_KEY")))


API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Kathmandu"

def get_weather(city, api_key):
    if not api_key:
        print("Error: API key not found. Check your .env file.")
        return

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        print(f"Weather in {city}:")
        print(f"  Condition: {description}")
        print(f"  Temperature: {temp}°C (feels like {feels_like}°C)")
        print(f"  Humidity: {humidity}%")
        print(f"  Wind speed: {wind} m/s")
    else:
        print(f"Error: {data.get('message', 'Something went wrong')}")

if __name__ == "__main__":
    get_weather(CITY, API_KEY)