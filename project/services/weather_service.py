"""Service to fetch weather from Open-Meteo."""
from typing import Optional, Dict
import requests


def get_current_weather(lat: float, lon: float) -> Optional[Dict]:
    """Return simplified current weather info (or None on failure)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto",
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        cw = data.get("current_weather")
        if not cw:
            return None
        return {
            "temperature": cw.get("temperature"),
            "windspeed": cw.get("windspeed"),
            "winddirection": cw.get("winddirection"),
            "weathercode": cw.get("weathercode"),
            "time": cw.get("time"),
            "raw": cw,
        }
    except requests.RequestException:
        return None
