"""Python wrapper for IMGW-PIB API."""

import logging
from datetime import UTC, datetime
from http import HTTPStatus
from typing import Any, Self

from aiohttp import ClientSession

from .const import (
    API_HUMIDITY,
    API_HYDROLOGICAL_ENDPOINT,
    API_MEASUREMENT_DATE,
    API_MEASUREMENT_TIME,
    API_PRECIPITATION,
    API_PRESSURE,
    API_RIVER,
    API_STATION,
    API_STATION_ID,
    API_TEMPERATURE,
    API_WATER_LEVEL,
    API_WATER_LEVEL_MEASUREMENT_DATE,
    API_WATER_TEMPERATURE,
    API_WATER_TEMPERATURE_MEASUREMENT_DATE,
    API_WEATHER_ENDPOINT,
    API_WIND_DIRECTION,
    API_WIND_SPEED,
    HEADERS,
    TIMEOUT,
    UNIT_CELSIUS,
    UNIT_CENTIMETERS,
    UNIT_DEGREE,
    UNIT_HPA,
    UNIT_METERS_PER_SECOND,
    UNIT_MILLIMETERS,
    UNIT_PERCENT,
)
from .exceptions import ApiError
from .model import HydrologicalData, SensorData, WeatherData

_LOGGER = logging.getLogger(__name__)


class ImgwPib:
    """Main class of IMGW-PIB API wrapper."""

    def __init__(
        self: Self,
        session: ClientSession,
        weather_station_id: str | None = None,
        hydrological_station_id: str | None = None,
    ) -> None:
        """Initialize IMGW-PIB API wrapper."""
        self._session = session
        self._weather_station_list: dict[str, str] = {}
        self._hydrological_station_list: dict[str, str] = {}

        self.weather_station_id = weather_station_id
        self.hydrological_station_id = hydrological_station_id

    @classmethod
    async def create(
        cls: type[Self],
        session: ClientSession,
        weather_station_id: str | None = None,
        hydrological_station_id: str | None = None,
    ) -> Self:
        """Create a new instance."""
        instance = cls(session, weather_station_id, hydrological_station_id)
        await instance.initialize()

        return instance

    @property
    def weather_stations(self: Self) -> dict[str, str]:
        """Return list of weather stations."""
        return self._weather_station_list

    @property
    def hydrological_stations(self: Self) -> dict[str, str]:
        """Return list of hydrological stations."""
        return self._hydrological_station_list

    async def initialize(self: Self) -> None:
        """Initialize."""
        _LOGGER.debug("Initializing IMGW-PIB")
        self._weather_station_list = await self.get_weather_stations()
        self._hydrological_station_list = await self.get_hydrological_stations()

        if (
            self.weather_station_id is not None
            and self.weather_station_id not in self.weather_stations
        ):
            msg = f"Invalid weather station ID: {self.weather_station_id}"
            raise ApiError(msg)
        if (
            self.hydrological_station_id is not None
            and self.hydrological_station_id not in self.hydrological_stations
        ):
            msg = f"Invalid hydrological station ID: {self.hydrological_station_id}"
            raise ApiError(msg)

    async def get_weather_stations(self: Self) -> dict[str, str]:
        """Get list of weather stations."""
        url = API_WEATHER_ENDPOINT

        stations_data = await self._http_request(url)

        return {
            station[API_STATION_ID]: station[API_STATION] for station in stations_data
        }

    async def get_weather_data(self: Self) -> WeatherData:
        """Get weather data."""
        url = f"{API_WEATHER_ENDPOINT}/id/{self.weather_station_id}"

        weather_data = await self._http_request(url)

        return self._parse_weather_data(weather_data)

    async def get_hydrological_stations(self: Self) -> dict[str, str]:
        """Get list of hydrological stations."""
        url = API_HYDROLOGICAL_ENDPOINT

        stations_data = await self._http_request(url)

        return {
            station[API_STATION_ID]: f"{station[API_STATION]} ({station[API_RIVER]})"
            for station in stations_data
        }

    async def get_hydrological_data(self: Self) -> HydrologicalData:
        """Get hydrological data."""
        url = f"{API_HYDROLOGICAL_ENDPOINT}/id/{self.hydrological_station_id}"

        hydrological_data = await self._http_request(url)

        return self._parse_hydrological_data(hydrological_data)

    async def _http_request(self: Self, url: str) -> Any:  # noqa: ANN401
        """Make an HTTP request."""
        _LOGGER.debug("Requesting %s", url)

        response = await self._session.request(
            "get", url, headers=HEADERS, timeout=TIMEOUT
        )

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
            unit=UNIT_CELSIUS if temperature is not None else None,
        )
        humidity = data[API_HUMIDITY]
        humidity_sensor = SensorData(
            name="Humidity",
            value=float(humidity) if humidity is not None else None,
            unit=UNIT_PERCENT if humidity is not None else None,
        )
        wind_speed = data[API_WIND_SPEED]
        wind_speed_sensor = SensorData(
            name="Wind Speed",
            value=float(wind_speed) if wind_speed is not None else None,
            unit=UNIT_METERS_PER_SECOND if wind_speed is not None else None,
        )
        wind_direction = data[API_WIND_DIRECTION]
        wind_direction_sensor = SensorData(
            name="Wind Direction",
            value=float(wind_direction) if wind_direction is not None else None,
            unit=UNIT_DEGREE if wind_direction is not None else None,
        )
        precipitation = data[API_PRECIPITATION]
        precipitation_sensor = SensorData(
            name="Precipitation",
            value=float(precipitation) if precipitation is not None else None,
            unit=UNIT_MILLIMETERS if precipitation is not None else None,
        )
        pressure = data[API_PRESSURE]
        pressure_sensor = SensorData(
            name="Pressure",
            value=float(pressure) if pressure is not None else None,
            unit=UNIT_HPA if pressure is not None else None,
        )
        measurement_date = datetime.strptime(
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
            measurement_date=measurement_date,
        )

    @staticmethod
    def _parse_hydrological_data(data: dict[str, Any]) -> HydrologicalData:
        """Parse hydrological data."""
        water_level = data[API_WATER_LEVEL]
        water_level_sensor = SensorData(
            name="Water Level",
            value=float(water_level) if water_level is not None else None,
            unit=UNIT_CENTIMETERS if water_level is not None else None,
        )
        water_level_measurement_date = datetime.strptime(
            f"{data[API_WATER_LEVEL_MEASUREMENT_DATE]}",
            "%Y-%m-%d %H:%M:%S",
        ).replace(tzinfo=UTC)
        water_temperature = data[API_WATER_TEMPERATURE]
        water_temperature_sensor = SensorData(
            name="Water Temperature",
            value=float(water_temperature) if water_temperature is not None else None,
            unit=UNIT_CELSIUS if water_temperature is not None else None,
        )
        water_temperature_measurement_date = datetime.strptime(
            f"{data[API_WATER_TEMPERATURE_MEASUREMENT_DATE]}",
            "%Y-%m-%d %H:%M:%S",
        ).replace(tzinfo=UTC)

        return HydrologicalData(
            water_level=water_level_sensor,
            water_temperature=water_temperature_sensor,
            station=data[API_STATION],
            river=data[API_RIVER],
            station_id=data[API_STATION_ID],
            water_level_measurement_date=water_level_measurement_date,
            water_temperature_measurement_date=water_temperature_measurement_date,
        )
