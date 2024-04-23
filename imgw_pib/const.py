"""IMDB-PIB constants."""

from aiohttp import ClientTimeout

API_BASE_ENDPOINT = "https://danepubliczne.imgw.pl/api/data"
API_HYDROLOGICAL_ENDPOINT = f"{API_BASE_ENDPOINT}/hydro"
API_WEATHER_ENDPOINT = f"{API_BASE_ENDPOINT}/synop"
API_HYDROLOGICAL_DETAILS_ENDPOINT = (
    "https://hydro-back.imgw.pl/station/hydro/status?id={hydrological_station_id}"
)

HEADERS = {"Content-Type": "application/json"}
TIMEOUT = ClientTimeout(total=20)
