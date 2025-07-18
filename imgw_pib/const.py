"""IMGW-PIB constants."""

from datetime import timedelta
from pathlib import Path

from aiohttp import ClientTimeout
from yarl import URL

BASE_DIR = Path(__file__).resolve().parent
WEATHER_STATIONS_INFO_FILE = BASE_DIR / "data" / "weather_stations_info.json"

API_BASE_ENDPOINT = URL("https://danepubliczne.imgw.pl/api/data")
API_HYDROLOGICAL_ENDPOINT = API_BASE_ENDPOINT / "hydro"
API_HYDROLOGICAL_WARNINGS_ENDPOINT = API_BASE_ENDPOINT / "warningshydro"
API_WEATHER_ENDPOINT = API_BASE_ENDPOINT / "synop"
API_WEATHER_WARNINGS_ENDPOINT = API_BASE_ENDPOINT / "warningsmeteo"
API_HYDROLOGICAL_DETAILS_ENDPOINT = URL(
    "https://hydro-back.imgw.pl/station/hydro/status"
)

HEADERS = {"Content-Type": "application/json"}
TIMEOUT = ClientTimeout(total=20)

DATA_VALIDITY_PERIOD = timedelta(hours=6)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

NO_ALERT = "no_alert"
WEATHER_ALERTS_MAP = {
    "brak": "no_alert",
    "burze": "storms",
    "intensywne opady deszczu": "heavy_rainfall",
    "silny deszcz z burzami": "heavy_rain_with_storms",
    "silny wiatr": "strong_wind",
    "upał": "heat",
}
HYDROLOGICAL_ALERTS_MAP = {
    "brak": "no_alert",
    "susza hydrologiczna": "hydrological_drought",
    "gwałtowne wzrosty stanów wody": "rapid_water_level_rise",
    "wezbranie z przekroczeniem stanów ostrzegawczych": "exceeding_the_warning_level",
}
ALERT_LEVEL_MAP = {
    "-1": "none",
    "1": "yellow",
    "2": "orange",
    "3": "red",
}
