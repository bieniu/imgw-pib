"""Python wrapper for IMGW-PIB API."""

import logging
from datetime import UTC, datetime
from http import HTTPStatus
from typing import Any, Self

from aiohttp import ClientSession

from .const import API_ENDPOINT, HEADERS
from .exceptions import ApiError
from .model import SensorData, WeatherData

_LOGGER = logging.getLogger(__name__)


class ImgwPib:
    """Main class of IMGW-PIB API wrapper."""

    def __init__(
        self: Self, session: ClientSession, weather_station_id: str | None = None
    ) -> None:
        """Initialize IMGW-PIB API wrapper."""
        self._session = session
        self._station_list: dict[str, str] = {}

        self.weather_station_id = weather_station_id

    @classmethod
    async def create(
        cls: type[Self], session: ClientSession, weather_station_id: str | None = None
    ) -> Self:
        """Create a new instance."""
        instance = cls(session, weather_station_id)
        await instance.initialize()

        return instance

    @property
    def stations(self: Self) -> dict[str, str]:
        """Return list of stations."""
        return self._station_list

    async def initialize(self: Self) -> None:
        """Initialize."""
        _LOGGER.debug("Initializing IMGW-PIB")
        self._station_list = await self.get_weather_stations()

        if (
            self.weather_station_id is not None
            and self.weather_station_id not in self._station_list
        ):
            msg = f"Invalid weather station ID: {self.weather_station_id}"
            raise ApiError(msg)

    async def get_weather_stations(self: Self) -> dict[str, str]:
        """Get list of weather stations."""
        url = API_ENDPOINT

        stations_data = await self._http_request(url)

        return {station["id_stacji"]: station["stacja"] for station in stations_data}

    async def get_weather_data(self: Self) -> WeatherData:
        """Get weather data."""
        url = f"{API_ENDPOINT}/id/{self.weather_station_id}"

        weather_data = await self._http_request(url)

        temperature_sensor = SensorData(
            name="Temperature",
            value=float(weather_data["temperatura"])
            if weather_data["temperatura"] is not None
            else None,
            unit="°C" if weather_data["temperatura"] is not None else None,
        )
        humidity_sensor = SensorData(
            name="Humidity",
            value=float(weather_data["wilgotnosc_wzgledna"])
            if weather_data["wilgotnosc_wzgledna"] is not None
            else None,
            unit="%" if weather_data["wilgotnosc_wzgledna"] is not None else None,
        )
        wind_speed_sensor = SensorData(
            name="Wind Speed",
            value=float(weather_data["predkosc_wiatru"])
            if weather_data["predkosc_wiatru"] is not None
            else None,
            unit="m/s" if weather_data["predkosc_wiatru"] is not None else None,
        )
        wind_direction_sensor = SensorData(
            name="Wind Direction",
            value=float(weather_data["kierunek_wiatru"])
            if weather_data["kierunek_wiatru"] is not None
            else None,
            unit="°" if weather_data["kierunek_wiatru"] is not None else None,
        )
        precipitation_sensor = SensorData(
            name="Precipitation",
            value=float(weather_data["suma_opadu"])
            if weather_data["suma_opadu"] is not None
            else None,
            unit="mm" if weather_data["suma_opadu"] is not None else None,
        )
        pressure_sensor = SensorData(
            name="Pressure",
            value=float(weather_data["cisnienie"])
            if weather_data["cisnienie"] is not None
            else None,
            unit="hPa" if weather_data["cisnienie"] is not None else None,
        )
        measurement_time = datetime.strptime(
            f"{weather_data["data_pomiaru"]} {weather_data["godzina_pomiaru"]}",
            "%Y-%m-%d %H",
        ).replace(tzinfo=UTC)

        return WeatherData(
            temperature=temperature_sensor,
            humidity=humidity_sensor,
            pressure=pressure_sensor,
            wind_speed=wind_speed_sensor,
            wind_direction=wind_direction_sensor,
            precipitation=precipitation_sensor,
            station=weather_data["stacja"],
            station_id=weather_data["id_stacji"],
            measurement_time=measurement_time,
        )

    async def _http_request(self: Self, url: str) -> Any:  # noqa: ANN401
        """Make an HTTP request."""
        _LOGGER.debug("Requesting %s", url)

        response = await self._session.request("get", url, headers=HEADERS)

        _LOGGER.debug("Response status: %s", response.status)

        if response.status != HTTPStatus.OK.value:
            msg = f"Invalid response: {response.status}"
            raise ApiError(msg)

        return await response.json()
