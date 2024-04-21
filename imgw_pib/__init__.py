"""Python wrapper for IMGW-PIB API."""

import logging
from datetime import UTC, datetime
from http import HTTPStatus
from typing import Any, Self

from aiohttp import ClientSession

from .const import API_ENDPOINT, HEADERS
from .exceptions import ApiError
from .model import SensorData, WeatherData, WeatherStation

_LOGGER = logging.getLogger(__name__)


class ImgwPib:
    """Main class of IMGW-PIB API wrapper."""

    def __init__(self: Self, session: ClientSession) -> None:
        """Initialize IMGW-PIB API wrapper."""
        self._session = session
        self._station_list: list[WeatherStation] = []

    @classmethod
    async def create(cls: type[Self], session: ClientSession) -> Self:
        """Create a new instance."""
        instance = cls(session)
        await instance.initialize()

        return instance

    @property
    def stations(self: Self) -> list[WeatherStation]:
        """Return list of stations."""
        return self._station_list

    async def initialize(self: Self) -> None:
        """Initialize."""
        _LOGGER.debug("Initializing IMGW-PIB")
        self._station_list = await self.get_weather_stations()

    async def get_weather_stations(self: Self) -> list[WeatherStation]:
        """Get list of weather stations."""
        url = API_ENDPOINT

        stations_data = await self._http_request(url)

        return [
            WeatherStation(station["id_stacji"], station["stacja"])
            for station in stations_data
        ]

    async def get_weather_data(self: Self, station_id: str) -> WeatherData:
        """Get weather data."""
        url = f"{API_ENDPOINT}/id/{station_id}"

        weather_data = await self._http_request(url)

        temperature_sensor = SensorData(
            name="Temperature", value=float(weather_data["temperatura"]), unit="°C"
        )
        humidity_sensor = SensorData(
            name="Humidity", value=float(weather_data["wilgotnosc_wzgledna"]), unit="%"
        )
        wind_speed_sensor = SensorData(
            name="Wind Speed", value=float(weather_data["predkosc_wiatru"]), unit="m/s"
        )
        wind_direction_sensor = SensorData(
            name="Wind Direction",
            value=float(weather_data["kierunek_wiatru"]),
            unit="°",
        )
        precipitation_sensor = SensorData(
            name="Precipitation", value=float(weather_data["suma_opadu"]), unit="mm"
        )
        pressure_sensor = SensorData(
            name="Pressure",
            value=None,
            unit=None if weather_data["cisnienie"] is None else "hPa",
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
