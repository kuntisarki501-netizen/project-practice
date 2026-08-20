from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from dotenv import load_dotenv
import requests
import os

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY not found. Please add it to the .env file.")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# -----------------------------
# Create FastAPI App
# -----------------------------
app = FastAPI(
    title="Weather Information API",
    description="A REST API built with FastAPI that retrieves current weather information using the OpenWeatherMap API.",
    version="1.0.0"
)

# -----------------------------
# Response Model
# -----------------------------
class WeatherResponse(BaseModel):
    status: str
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    weather: str
    description: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "city": "Kathmandu",
                "country": "NP",
                "temperature": 26.8,
                "feels_like": 27.5,
                "humidity": 72,
                "pressure": 1012,
                "wind_speed": 2.1,
                "weather": "Clouds",
                "description": "broken clouds"
            }
        }
    )

# -----------------------------
# Home Endpoint
# -----------------------------
@app.get(
    "/",
    tags=["Home"],
    summary="Home",
    description="Returns a welcome message."
)
def home():
    return {
        "status": "success",
        "message": "Welcome to the Weather Information API!",
        "developer": "Mahima Parajuli",
        "documentation": "/docs",
        "example": "/weather?city=Kathmandu"
    }

# -----------------------------
# Weather Endpoint
# -----------------------------
@app.get(
    "/weather",
    response_model=WeatherResponse,
    tags=["Weather"],
    summary="Get Current Weather",
    description="Returns the current weather information for a specified city."
)
def get_weather(
    city: str = Query(
        ...,
        min_length=2,
        max_length=50,
        description="Enter the city name"
    )
):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="City not found."
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Unable to retrieve weather information."
            )

        data = response.json()

        return WeatherResponse(
            status="success",
            city=data["name"],
            country=data["sys"]["country"],
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            wind_speed=data["wind"]["speed"],
            weather=data["weather"][0]["main"],
            description=data["weather"][0]["description"]
        )

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="The request to the Weather API timed out."
        )

    
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
