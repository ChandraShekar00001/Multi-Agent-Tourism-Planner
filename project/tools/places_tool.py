"""LangChain tool wrapper for places service."""

from typing import Optional, ClassVar
from langchain.tools import BaseTool
from services.places_service import find_places



class PlacesTool(BaseTool):
    name: ClassVar[str] = "places"
    description: ClassVar[str] = (
        "Find tourism places near coordinates. Input: 'lat|lon|radius' string. Returns: JSON list of places."
    )

    def _run(self, query: str) -> Optional[list]:
        try:
            parts = (query or "").split("|")
            lat = float(parts[0])
            lon = float(parts[1])
            radius = int(parts[2]) if len(parts) > 2 and parts[2] else 3000
        except Exception:
            return None
        return find_places(lat, lon, radius=radius)

    async def _arun(self, query: str) -> Optional[list]:
        return self._run(query)
