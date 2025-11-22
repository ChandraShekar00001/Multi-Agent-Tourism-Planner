"""Weather child agent: uses geocode tool + weather tool to answer weather queries."""
from typing import Optional, Dict
from tools.geocode_tool import GeocodeTool
from tools.weather_tool import WeatherTool


class WeatherAgent:
    def __init__(self) -> None:
        self.geocode = GeocodeTool()
        self.weather = WeatherTool()

    def handle(self, place: str) -> Dict:
        """Return dict with either 'error' or 'weather' and 'location'."""
        geo = self.geocode.run(place)
        if not geo:
            return {"error": "I don't think this place exists."}

        lat = geo["lat"]
        lon = geo["lon"]
        weather = self.weather.run(f"{lat}|{lon}")
        if not weather:
            return {"error": "Weather service unavailable."}

        return {"location": geo, "weather": weather}
