"""Service to query Overpass API for nearby places/tourist attractions."""
from typing import Optional, List, Dict
import requests
import math


OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def _haversine(lat1, lon1, lat2, lon2):
    # return distance in meters
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def find_places(lat: float, lon: float, radius: int = 3000, limit: int = 20) -> Optional[List[Dict]]:
    """Query Overpass for tourism, attraction, amenity, restaurant around the coordinates.

    Returns a list of places with basic metadata sorted by distance.
    """
    # Overpass QL: search nodes and ways with common tourism/amenity tags
    q = f"""
[out:json][timeout:25];
(
  node(around:{radius},{lat},{lon})[tourism];
  node(around:{radius},{lat},{lon})[amenity];
  way(around:{radius},{lat},{lon})[tourism];
  way(around:{radius},{lat},{lon})[amenity];
);
out center {limit};
"""

    try:
        resp = requests.post(OVERPASS_URL, data={"data": q}, timeout=25)
        resp.raise_for_status()
        data = resp.json()
        elements = data.get("elements", [])
        results = []
        for el in elements:
            lat_el = el.get("lat") or (el.get("center") or {}).get("lat")
            lon_el = el.get("lon") or (el.get("center") or {}).get("lon")
            tags = el.get("tags") or {}
            name = tags.get("name")
            if not name:
                continue
            dist = _haversine(lat, lon, lat_el, lon_el) if lat_el and lon_el else None
            results.append({
                "id": el.get("id"),
                "name": name,
                "tags": tags,
                "lat": lat_el,
                "lon": lon_el,
                "distance_m": dist,
            })

        # sort by distance
        results = [r for r in results if r.get("distance_m") is not None]
        results.sort(key=lambda x: x["distance_m"])  # type: ignore
        return results[:limit]
    except requests.RequestException:
        return None
