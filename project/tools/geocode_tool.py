"""LangChain tool wrapper for geocoding service."""

from typing import Optional, ClassVar
from langchain.tools import BaseTool
from services.geocode_service import geocode_place



class GeocodeTool(BaseTool):
    name: ClassVar[str] = "geocode"
    description: ClassVar[str] = (
        "Geocode a place name using Nominatim. Input: place name. Returns: JSON with lat/lon/display_name or error."
    )

    def _run(self, query: str) -> Optional[dict]:
        return geocode_place(query)

    async def _arun(self, query: str) -> Optional[dict]:
        return self._run(query)
