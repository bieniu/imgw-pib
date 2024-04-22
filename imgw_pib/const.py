"""IMDB-PIB constants."""

from aiohttp import ClientTimeout

API_BASE_ENDPOINT = "https://danepubliczne.imgw.pl/api/data"
API_HYDROLOGICAL_ENDPOINT = f"{API_BASE_ENDPOINT}/hydro"
API_WEATHER_ENDPOINT = f"{API_BASE_ENDPOINT}/synop"

HEADERS = {"Content-Type": "application/json"}
TIMEOUT = ClientTimeout(total=20)

API_HUMIDITY = "wilgotnosc_wzgledna"
API_MEASUREMENT_DATE = "data_pomiaru"
API_MEASUREMENT_TIME = "godzina_pomiaru"
API_PRECIPITATION = "suma_opadu"
API_PRESSURE = "cisnienie"
API_RIVER = "rzeka"
API_STATION = "stacja"
API_STATION_ID = "id_stacji"
API_TEMPERATURE = "temperatura"
API_WATER_LEVEL = "stan_wody"
API_WATER_LEVEL_MEASUREMENT_DATE = "stan_wody_data_pomiaru"
API_WATER_TEMPERATURE = "temperatura_wody"
API_WATER_TEMPERATURE_MEASUREMENT_DATE = "temperatura_wody_data_pomiaru"
API_WIND_DIRECTION = "kierunek_wiatru"
API_WIND_SPEED = "predkosc_wiatru"

UNIT_CELSIUS = "°C"
UNIT_CENTIMETERS = "cm"
UNIT_DEGREE = "°"
UNIT_HPA = "hPa"
UNIT_METERS_PER_SECOND = "m/s"
UNIT_MILLIMETERS = "mm"
UNIT_PERCENT = "%"
