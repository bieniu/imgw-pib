"""IMDB-PIB constants."""

from aiohttp import ClientTimeout

API_ENDPOINT = "https://danepubliczne.imgw.pl/api/data/synop"

HEADERS = {"Content-Type": "application/json"}
TIMEOUT = ClientTimeout(total=20)

API_HUMIDITY = "wilgotnosc_wzgledna"
API_MEASUREMENT_DATE = "data_pomiaru"
API_MEASUREMENT_TIME = "godzina_pomiaru"
API_PRECIPITATION = "suma_opadu"
API_PRESSURE = "cisnienie"
API_STATION = "stacja"
API_STATION_ID = "id_stacji"
API_TEMPERATURE = "temperatura"
API_WIND_DIRECTION = "kierunek_wiatru"
API_WIND_SPEED = "predkosc_wiatru"

UNIT_CELSIUS = "°C"
UNIT_DEGREE = "°"
UNIT_HPA = "hPa"
UNIT_METERS_PER_SECOND = "m/s"
UNIT_MILLIMETERS = "mm"
UNIT_PERCENT = "%"
