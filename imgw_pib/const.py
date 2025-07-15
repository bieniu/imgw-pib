"""IMGW-PIB constants."""

from datetime import timedelta
from pathlib import Path

from aiohttp import ClientTimeout
from yarl import URL

BASE_DIR = Path(__file__).resolve().parent
RIVERS_FILE = BASE_DIR / "data" / "rivers.json"

API_BASE_ENDPOINT = URL("https://danepubliczne.imgw.pl/api/data")
API_HYDROLOGICAL_ENDPOINT = API_BASE_ENDPOINT / "hydro"
API_HYDROLOGICAL_ENDPOINT_2 = API_BASE_ENDPOINT / "hydro2"
API_WEATHER_ENDPOINT = API_BASE_ENDPOINT / "synop"
API_WEATHER_WARNINGS_ENDPOINT = API_BASE_ENDPOINT / "warningsmeteo"
API_HYDROLOGICAL_DETAILS_ENDPOINT = URL(
    "https://hydro-back.imgw.pl/station/hydro/status"
)
API_HYDROLOGICAL_WARNINGS_ENDPOINT = API_BASE_ENDPOINT / "warningshydro"

HEADERS = {"Content-Type": "application/json"}
TIMEOUT = ClientTimeout(total=20)

DATA_VALIDITY_PERIOD = timedelta(hours=6)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

ID_TO_TERYT_MAP = {
    "12295": "2061",  # Białystok
    "12600": "2461",  # Bielsko-Biała
    "12235": "2202",  # Chojnice
    "12550": "2464",  # Częstochowa
    "12160": "2861",  # Elbląg
    "12155": "2261",  # Gdańsk
    "12135": "2211",  # Hel
    "12500": "0261",  # Jelenia Góra
    "12435": "3061",  # Kalisz
    "12560": "2469",  # Katowice
    "12185": "2808",  # Kętrzyn
    "12570": "2661",  # Kielce
    "12520": "0208",  # Kłodzko
    "12345": "3009",  # Koło
    "12100": "3208",  # Kołobrzeg
    "12105": "3261",  # Koszalin
    "12488": "1407",  # Kozienice
    "12566": "1261",  # Kraków
    "12670": "1861",  # Krosno
    "12415": "0262",  # Legnica
    "12690": "1821",  # Lesko
    "12418": "3063",  # Leszno
    "12125": "2208",  # Lębork
    "12495": "0663",  # Lublin
    "12120": "2208",  # Łeba
    "12465": "1061",  # Łódź
    "12280": "2810",  # Mikołajki
    "12270": "1413",  # Mława
    "12660": "1262",  # Nowy Sącz
    "12530": "1661",  # Opole
    "12285": "1461",  # Ostrołęka
    "12230": "3019",  # Piła
    "12360": "1462",  # Płock
    "12330": "3064",  # Poznań
    "12695": "1862",  # Przemyśl
    "12540": "2411",  # Racibórz
    "12210": "3218",  # Resko
    "12580": "1863",  # Rzeszów
    "12585": "2609",  # Sandomierz
    "12385": "1464",  # Siedlce
    "12310": "0805",  # Słubice
    "12469": "1010",  # Sulejów
    "12195": "2063",  # Suwałki
    "12205": "3262",  # Szczecin
    "12215": "3215",  # Szczecinek
    "12200": "3263",  # Świnoujście
    "12575": "1263",  # Tarnów
    "12399": "0601",  # Terespol
    "12250": "0463",  # Toruń
    "12115": "2212",  # Ustka
    "12375": "1465",  # Warszawa
    "12455": "1017",  # Wieluń
    "12497": "0619",  # Włodawa
    "12424": "0264",  # Wrocław
    "12625": "1217",  # Zakopane
    "12595": "0664",  # Zamość
    "12400": "0862",  # Zielona Góra
}

WEATHER_ALERTS_MAP = {
    "brak": "no_alert",
    "burze": "storms",
    "intensywne opady deszczu": "heavy_rainfall",
    "silny deszcz z burzami": "heavy_rain_with_storms",
    "silny wiatr": "strong_wind",
}
HYDROLOGICAL_ALERTS_MAP = {
    "brak": "no_alert",
    "susza hydrologiczna": "hydrological_drought",
    "gwałtowne wzrosty stanów wody": "rapid_water_level_rise",
}
ALERT_LEVEL_MAP = {
    "-1": "none",
    "1": "yellow",
    "2": "orange",
    "3": "red",
}
