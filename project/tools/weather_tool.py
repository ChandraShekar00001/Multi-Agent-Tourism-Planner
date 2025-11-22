"""LangChain tool wrapper for weather service."""

from typing import Optional, ClassVar
from langchain.tools import BaseTool
from services.weather_service import get_current_weather



class WeatherTool(BaseTool):
    name: ClassVar[str] = "weather"
    description: ClassVar[str] = (
        "Get current weather for coordinates. Input: 'lat|lon' string. Returns: JSON with weather info."
    )

    def _run(self, query: str) -> Optional[dict]:
        try:
            lat_str, lon_str = (query or "").split("|", 1)
            lat = float(lat_str)
            lon = float(lon_str)
        except Exception:
            return None
        return get_current_weather(lat, lon)

    async def _arun(self, query: str) -> Optional[dict]:
        return self._run(query)
