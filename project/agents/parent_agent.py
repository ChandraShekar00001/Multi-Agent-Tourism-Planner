"""Parent (Orchestrator) Agent: coordinates child agents based on parsed intent."""
from typing import Dict, Any
from utils.parser import parse_query
from agents.weather_agent import WeatherAgent
from agents.places_agent import PlacesAgent


class ParentAgent:
    def __init__(self) -> None:
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()

    def handle(self, user_input: str) -> Dict[str, Any]:
        """Decide which child agents to call and aggregate results.

        Returns a dict with keys: 'weather' and/or 'places' or 'error'.
        """
        want_weather, want_places, place = parse_query(user_input)

        response: Dict[str, Any] = {"query": user_input, "place": place}

        if want_weather:
            weather_res = self.weather_agent.handle(place)
            response["weather"] = weather_res

        if want_places:
            places_res = self.places_agent.handle(place)
            response["places"] = places_res

        return response
