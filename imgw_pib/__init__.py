"""Python wrapper for IMGW-PIB API."""

import logging
from datetime import UTC, datetime
from http import HTTPStatus
from typing import Any, Self

from aiohttp import ClientSession

from .const import (
    API_ENDPOINT,
    API_HUMIDITY,
    API_MEASUREMENT_DATE,
    API_MEASUREMENT_TIME,
    API_PRECIPITATION,
    API_PRESSURE,
    API_STATION,
    API_STATION_ID,
    API_TEMPERATURE,
    API_WIND_DIRECTION,
    API_WIND_SPEED,
    HEADERS,
)
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

        return {
            station[API_STATION_ID]: station[API_STATION] for station in stations_data
        }

    async def get_weather_data(self: Self) -> WeatherData:
        """Get weather data."""
        url = f"{API_ENDPOINT}/id/{self.weather_station_id}"

        weather_data = await self._http_request(url)

        return self._parse_weather_data(weather_data)

    async def _http_request(self: Self, url: str) -> Any:  # noqa: ANN401
        """Make an HTTP request."""
        _LOGGER.debug("Requesting %s", url)

        response = await self._session.request("get", url, headers=HEADERS)

        _LOGGER.debug("Response status: %s", response.status)

        if response.status != HTTPStatus.OK.value:
            msg = f"Invalid response: {response.status}"
            raise ApiError(msg)

        return await response.json()

    @staticmethod
    def _parse_weather_data(data: dict[str, Any]) -> WeatherData:
        """Parse weather data."""
        temperature = data[API_TEMPERATURE]
        temperature_sensor = SensorData(
            name="Temperature",
            value=float(temperature) if temperature is not None else None,
            unit="°C" if temperature is not None else None,
        )
        humidity = data[API_HUMIDITY]
        humidity_sensor = SensorData(
            name="Humidity",
            value=float(humidity) if humidity is not None else None,
            unit="%" if humidity is not None else None,
        )
        wind_speed = data[API_WIND_SPEED]
        wind_speed_sensor = SensorData(
            name="Wind Speed",
            value=float(wind_speed) if wind_speed is not None else None,
            unit="m/s" if wind_speed is not None else None,
        )
        wind_direction = data[API_WIND_DIRECTION]
        wind_direction_sensor = SensorData(
            name="Wind Direction",
            value=float(wind_direction) if wind_direction is not None else None,
            unit="°" if wind_direction is not None else None,
        )
        precipitation = data[API_PRECIPITATION]
        precipitation_sensor = SensorData(
            name="Precipitation",
            value=float(precipitation) if precipitation is not None else None,
            unit="mm" if precipitation is not None else None,
        )
        pressure = data[API_PRESSURE]
        pressure_sensor = SensorData(
            name="Pressure",
            value=float(pressure) if pressure is not None else None,
            unit="hPa" if pressure is not None else None,
        )
        measurement_time = datetime.strptime(
            f"{data[API_MEASUREMENT_DATE]} {data[API_MEASUREMENT_TIME]}",
            "%Y-%m-%d %H",
        ).replace(tzinfo=UTC)

        return WeatherData(
            temperature=temperature_sensor,
            humidity=humidity_sensor,
            pressure=pressure_sensor,
            wind_speed=wind_speed_sensor,
            wind_direction=wind_direction_sensor,
            precipitation=precipitation_sensor,
            station=data[API_STATION],
            station_id=data[API_STATION_ID],
            measurement_time=measurement_time,
        )
