"""
JARVIS Weather Plugin
Provides weather information and forecasts

Commands:
- "what's the weather" - Get current weather
- "weather in [city]" - Get weather for a specific city
- "weather forecast" - Get 5-day forecast
"""

import urllib.request
import json
from datetime import datetime

PLUGIN_INFO = {
    "name": "Weather",
    "version": "1.0.0",
    "description": "Get current weather and forecasts",
    "author": "Farhan",
    "commands": {
        "what's the weather": "get_weather",
        "whats the weather": "get_weather",
        "weather in": "get_weather_city",
        "weather forecast": "get_forecast",
        "temperature": "get_weather",
    }
}

# Free weather API (no key required for basic usage)
# Using wttr.in which is free and doesn't require API key
WEATHER_API = "https://wttr.in/{city}?format=j1"

_context = None


def setup(jarvis_context):
    """Called when plugin is loaded."""
    global _context
    _context = jarvis_context
    print("🌤️ Weather plugin loaded!")


def cleanup():
    """Called when plugin is unloaded."""
    pass


def _fetch_weather(city: str = ""):
    """Fetch weather data from API."""
    try:
        # Default to auto-detect location if no city specified
        url = WEATHER_API.format(city=city if city else "")
        
        req = urllib.request.Request(url, headers={"User-Agent": "JARVIS/2.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Weather API error: {e}")
        return None


def get_weather(command: str, context):
    """Get current weather for user's location."""
    speak = context.speak
    
    speak("Let me check the weather for you, Sir.")
    
    data = _fetch_weather()
    if not data:
        speak("I apologize, Sir. I couldn't fetch the weather information.")
        return True
    
    try:
        current = data["current_condition"][0]
        location = data["nearest_area"][0]
        
        city = location["areaName"][0]["value"]
        country = location["country"][0]["value"]
        temp_c = current["temp_C"]
        temp_f = current["temp_F"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        desc = current["weatherDesc"][0]["value"]
        
        weather_report = (
            f"Currently in {city}, {country}, it's {temp_c} degrees Celsius, "
            f"or {temp_f} Fahrenheit. {desc}. "
            f"Feels like {feels_like} degrees with {humidity}% humidity."
        )
        
        speak(weather_report)
    except (KeyError, IndexError) as e:
        speak("I received the weather data but couldn't parse it properly, Sir.")
    
    return True


def get_weather_city(command: str, context):
    """Get weather for a specific city."""
    speak = context.speak
    
    # Extract city from command: "weather in london" -> "london"
    city = command.lower().replace("weather in", "").strip()
    
    if not city:
        speak("Which city would you like the weather for, Sir?")
        return True
    
    speak(f"Checking the weather in {city}, Sir.")
    
    data = _fetch_weather(city)
    if not data:
        speak(f"I apologize, Sir. I couldn't find weather information for {city}.")
        return True
    
    try:
        current = data["current_condition"][0]
        location = data["nearest_area"][0]
        
        area = location["areaName"][0]["value"]
        temp_c = current["temp_C"]
        temp_f = current["temp_F"]
        desc = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        
        weather_report = (
            f"In {area}, it's currently {temp_c} degrees Celsius, "
            f"{temp_f} Fahrenheit. {desc} with {humidity}% humidity."
        )
        
        speak(weather_report)
    except (KeyError, IndexError):
        speak(f"I found {city} but couldn't parse the weather data, Sir.")
    
    return True


def get_forecast(command: str, context):
    """Get weather forecast."""
    speak = context.speak
    
    speak("Let me get the forecast for you, Sir.")
    
    data = _fetch_weather()
    if not data:
        speak("I apologize, Sir. I couldn't fetch the forecast.")
        return True
    
    try:
        location = data["nearest_area"][0]
        city = location["areaName"][0]["value"]
        forecast = data["weather"][:3]  # Next 3 days
        
        speak(f"Here's the forecast for {city}:")
        
        for day in forecast:
            date = datetime.strptime(day["date"], "%Y-%m-%d").strftime("%A")
            max_temp = day["maxtempC"]
            min_temp = day["mintempC"]
            desc = day["hourly"][4]["weatherDesc"][0]["value"]  # Midday weather
            
            speak(f"{date}: {desc}, high of {max_temp}, low of {min_temp} degrees.")
        
    except (KeyError, IndexError):
        speak("I received forecast data but couldn't parse it properly, Sir.")
    
    return True
