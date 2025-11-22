"""Places child agent: uses geocode tool + places tool to answer places queries."""
from typing import Dict
from tools.geocode_tool import GeocodeTool
from tools.places_tool import PlacesTool


class PlacesAgent:
    def __init__(self) -> None:
        self.geocode = GeocodeTool()
        self.places = PlacesTool()

    def handle(self, place: str, radius: int = 3000) -> Dict:
        geo = self.geocode.run(place)
        if not geo:
            return {"error": "I don't think this place exists."}

        lat = geo["lat"]
        lon = geo["lon"]
        results = self.places.run(f"{lat}|{lon}|{radius}")
        if results is None:
            return {"error": "Places service unavailable."}

        return {"location": geo, "places": results}
