"""Simple parser to determine user intent (weather, places, both) and extract place name.

This is intentionally lightweight and keyword-driven for reliability without an LLM.
"""
from typing import Tuple


WEATHER_KEYWORDS = {
    "weather",
    "temperature",
    "forecast",
    "rain",
    "snow",
    "sunny",
}

PLACES_KEYWORDS = {
    "place",
    "places",
    "sights",
    "attractions",
    "things to do",
    "tourist",
    "tourism",
    "restaurants",
    "hotels",
}


def parse_query(query: str) -> Tuple[bool, bool, str]:
    """Return (want_weather, want_places, place).

    If place cannot be found heuristically, returns the original query as place.
    The parent agent will then attempt geocoding and can respond if not found.
    """
    text = (query or "").strip().lower()
    want_weather = any(k in text for k in WEATHER_KEYWORDS)
    want_places = any(k in text for k in PLACES_KEYWORDS)

    # If user mentions both or neither explicitly, we treat as both by default.
    if not want_weather and not want_places:
        want_weather = True
        want_places = True

    # Heuristic to extract a place name: look for 'in <place>' or 'at <place>' or final token(s)
    place = text
    for pre in ("in ", "at "):
        if pre in text:
            candidate = text.split(pre, 1)[1].strip()
            if candidate:
                place = candidate
                break

    return want_weather, want_places, place
