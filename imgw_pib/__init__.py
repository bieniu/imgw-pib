"""Python wrapper for IMGW-PIB API."""

import logging
from datetime import UTC, datetime
from http import HTTPStatus
from typing import Any, Self

from aiohttp import ClientSession

from .const import (
    API_HYDROLOGICAL_DETAILS_ENDPOINT,
    API_HYDROLOGICAL_ENDPOINT,
    API_WEATHER_ENDPOINT,
    DATA_VALIDITY_PERIOD,
    HEADERS,
    TIMEOUT,
)
from .exceptions import ApiError
from .model import ApiNames, HydrologicalData, SensorData, Units, WeatherData
from .utils import gen_station_name, get_datetime

_LOGGER = logging.getLogger(__name__)


class ImgwPib:
    """Main class of IMGW-PIB API wrapper."""

    def __init__(
        self: Self,
        session: ClientSession,
        weather_station_id: str | None = None,
        hydrological_station_id: str | None = None,
        hydro_details: bool = True,
    ) -> None:
        """Initialize IMGW-PIB API wrapper."""
        self._session = session
        self._weather_station_list: dict[str, str] = {}
        self._hydrological_station_list: dict[str, str] = {}
        self._alarm_water_level: float | None = None
        self._warning_water_level: float | None = None

        self.weather_station_id = weather_station_id
        self.hydrological_station_id = hydrological_station_id

        self.hydro_details = hydro_details

    @classmethod
    async def create(
        cls: type[Self],
        session: ClientSession,
        weather_station_id: str | None = None,
        hydrological_station_id: str | None = None,
        hydro_details: bool = True,
    ) -> Self:
        """Create a new instance."""
        instance = cls(
            session, weather_station_id, hydrological_station_id, hydro_details
        )
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

        if self.weather_station_id is not None:
            await self.update_weather_stations()

            if self.weather_station_id not in self.weather_stations:
                msg = f"Invalid weather station ID: {self.weather_station_id}"
                raise ApiError(msg)

        if self.hydrological_station_id is not None:
            await self.update_hydrological_stations()

            if self.hydrological_station_id not in self.hydrological_stations:
                msg = f"Invalid hydrological station ID: {self.hydrological_station_id}"
                raise ApiError(msg)

            if self.hydro_details is True:
                await self._update_hydrological_details()

    async def update_weather_stations(self: Self) -> None:
        """Update list of weather stations."""
        url = API_WEATHER_ENDPOINT

        stations_data = await self._http_request(url)

        self._weather_station_list = {
            station[ApiNames.STATION_ID]: station[ApiNames.STATION]
            for station in stations_data
        }

    async def get_weather_data(self: Self) -> WeatherData:
        """Get weather data."""
        if self.weather_station_id is None:
            msg = "Weather station ID is not set"
            raise ApiError(msg)

        url = f"{API_WEATHER_ENDPOINT}/id/{self.weather_station_id}"

        weather_data = await self._http_request(url)

        return self._parse_weather_data(weather_data)

    async def update_hydrological_stations(self: Self) -> None:
        """Update list of hydrological stations."""
        url = API_HYDROLOGICAL_ENDPOINT

        stations_data = await self._http_request(url)

        self._hydrological_station_list = {
            station[ApiNames.STATION_ID]: gen_station_name(
                station[ApiNames.STATION], station[ApiNames.RIVER]
            )
            for station in stations_data
        }

    async def _update_hydrological_details(self: Self) -> None:
        """Update hydrological details."""
        url = API_HYDROLOGICAL_DETAILS_ENDPOINT.format(
            hydrological_station_id=self.hydrological_station_id
        )

        try:
            hydrological_details = await self._http_request(url)
        except ApiError as exc:
            _LOGGER.info("Hydrological details not available: %s", repr(exc))
            return

        if hydrological_details is None:
            _LOGGER.info("Invalid hydrological details format")
            return

        self._warning_water_level = hydrological_details["status"]["warningValue"]
        self._alarm_water_level = hydrological_details["status"]["alarmValue"]

    async def get_hydrological_data(self: Self) -> HydrologicalData:
        """Get hydrological data."""
        if self.hydrological_station_id is None:
            msg = "Hydrological station ID is not set"
            raise ApiError(msg)

        all_stations_data = await self._http_request(API_HYDROLOGICAL_ENDPOINT)

        hydrological_data = next(
            (
                item
                for item in all_stations_data
                if item.get(ApiNames.STATION_ID) == self.hydrological_station_id
            ),
            None,
        )

        if hydrological_data is None:
            msg = f"No hydrological data for station ID: {self.hydrological_station_id}"
            raise ApiError(msg)

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

        if "application/json" not in response.content_type:
            msg = f"Invalid content type: {response.content_type}"
            raise ApiError(msg)

        return await response.json()

    @staticmethod
    def _parse_weather_data(data: dict[str, Any]) -> WeatherData:
        """Parse weather data."""
        temperature = data[ApiNames.TEMPERATURE]
        temperature_sensor = SensorData(
            name="Temperature",
            value=float(temperature) if temperature is not None else None,
            unit=Units.CELSIUS.value if temperature is not None else None,
        )
        humidity = data[ApiNames.HUMIDITY]
        humidity_sensor = SensorData(
            name="Humidity",
            value=float(humidity) if humidity is not None else None,
            unit=Units.PERCENT.value if humidity is not None else None,
        )
        wind_speed = data[ApiNames.WIND_SPEED]
        wind_speed_sensor = SensorData(
            name="Wind Speed",
            value=float(wind_speed) if wind_speed is not None else None,
            unit=Units.METERS_PER_SECOND.value if wind_speed is not None else None,
        )
        wind_direction = data[ApiNames.WIND_DIRECTION]
        wind_direction_sensor = SensorData(
            name="Wind Direction",
            value=float(wind_direction) if wind_direction is not None else None,
            unit=Units.DEGREE.value if wind_direction is not None else None,
        )
        precipitation = data[ApiNames.PRECIPITATION]
        precipitation_sensor = SensorData(
            name="Precipitation",
            value=float(precipitation) if precipitation is not None else None,
            unit=Units.MILLIMETERS.value if precipitation is not None else None,
        )
        pressure = data[ApiNames.PRESSURE]
        pressure_sensor = SensorData(
            name="Pressure",
            value=float(pressure) if pressure is not None else None,
            unit=Units.HPA.value if pressure is not None else None,
        )
        measurement_date = get_datetime(
            f"{data[ApiNames.MEASUREMENT_DATE]} {data[ApiNames.MEASUREMENT_TIME]}",
            "%Y-%m-%d %H",
        )

        return WeatherData(
            temperature=temperature_sensor,
            humidity=humidity_sensor,
            pressure=pressure_sensor,
            wind_speed=wind_speed_sensor,
            wind_direction=wind_direction_sensor,
            precipitation=precipitation_sensor,
            station=data[ApiNames.STATION],
            station_id=data[ApiNames.STATION_ID],
            measurement_date=measurement_date,
        )

    def _parse_hydrological_data(self: Self, data: dict[str, Any]) -> HydrologicalData:
        """Parse hydrological data."""
        water_level_measurement_date = get_datetime(
            data[ApiNames.WATER_LEVEL_MEASUREMENT_DATE],
            "%Y-%m-%d %H:%M:%S",
        )
        if (
            water_level_measurement_date is not None
            and datetime.now(tz=UTC) - water_level_measurement_date
            < DATA_VALIDITY_PERIOD
        ):
            water_level = data[ApiNames.WATER_LEVEL]
        else:
            water_level_measurement_date = None
            water_level = None

        if water_level is None:
            msg = "Invalid water level value"
            raise ApiError(msg)

        water_level_sensor = SensorData(
            name="Water Level",
            value=float(water_level) if water_level is not None else None,
            unit=Units.CENTIMETERS.value if water_level is not None else None,
        )
        flood_warning_level_sensor = SensorData(
            name="Flood Warning Level",
            value=self._warning_water_level,
            unit=Units.CENTIMETERS.value
            if self._warning_water_level is not None
            else None,
        )
        flood_alarm_level_sensor = SensorData(
            name="Flood Alarm Level",
            value=self._alarm_water_level,
            unit=Units.CENTIMETERS.value
            if self._alarm_water_level is not None
            else None,
        )

        water_temperature_measurement_date = get_datetime(
            data[ApiNames.WATER_TEMPERATURE_MEASUREMENT_DATE],
            "%Y-%m-%d %H:%M:%S",
        )
        if (
            water_temperature_measurement_date is not None
            and datetime.now(tz=UTC) - water_temperature_measurement_date
            < DATA_VALIDITY_PERIOD
        ):
            water_temperature = data[ApiNames.WATER_TEMPERATURE]
        else:
            water_temperature_measurement_date = None
            water_temperature = None

        water_temperature_sensor = SensorData(
            name="Water Temperature",
            value=float(water_temperature) if water_temperature is not None else None,
            unit=Units.CELSIUS.value if water_temperature is not None else None,
        )

        return HydrologicalData(
            water_level=water_level_sensor,
            flood_warning_level=flood_warning_level_sensor,
            flood_alarm_level=flood_alarm_level_sensor,
            water_temperature=water_temperature_sensor,
            station=data[ApiNames.STATION],
            river=data[ApiNames.RIVER],
            station_id=data[ApiNames.STATION_ID],
            water_level_measurement_date=water_level_measurement_date,
            water_temperature_measurement_date=water_temperature_measurement_date,
        )
