
import os
import requests

from dotenv import load_dotenv
from langchain_nimble import NimbleSearchTool
from langchain.tools import tool

load_dotenv()

search_tool = NimbleSearchTool(
    k=5,
    deep_search=True,
    passing_type="markdown"
)


@tool
def google_search(query: str) -> str:
    """Search the web for real-time information using Nimble Search."""
    return search_tool.invoke(query)


@tool
def weather_rohit_tool(city: str) -> dict:
    """Get current weather information for a city, including temperature and humidity."""

    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        return {"error": "WEATHER_API_KEY is missing from .env"}

    api_url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(
            api_url,
            params={
                "q": city,
                "appid": api_key,
                "units": "metric"
            },
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        return {
            "error": "Unable to fetch weather",
            "status_code": response.status_code
        }

    except requests.RequestException as e:
        return {"error": str(e)}


ALL_TOOLS = [google_search, weather_rohit_tool]
