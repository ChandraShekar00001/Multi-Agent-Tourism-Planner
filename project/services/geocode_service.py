"""Service to call Nominatim (OpenStreetMap) for geocoding.
"""
from typing import Optional, Dict
import requests


def geocode_place(place: str, limit: int = 1) -> Optional[Dict]:
    """Query Nominatim for a place. Returns a dict with lat, lon, display_name or None.

    Respects Nominatim usage policy by sending a User-Agent header.
    """
    if not place:
        return None

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place,
        "format": "json",
        "addressdetails": 1,
        "limit": limit,
    }
    headers = {"User-Agent": "multi-agent-tourism-planner/1.0 (evaluation)"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        first = data[0]
        return {
            "lat": float(first.get("lat")),
            "lon": float(first.get("lon")),
            "display_name": first.get("display_name"),
            "raw": first,
        }
    except requests.RequestException:
        return None
