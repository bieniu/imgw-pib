"""Python wrapper for IMGW-PIB API."""

import logging
from datetime import UTC, datetime
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Self

import aiofiles
import orjson
from aiohttp import ClientSession
from yarl import URL

from .const import (
    ALERT_LEVEL_MAP,
    API_HYDROLOGICAL_DETAILS_ENDPOINT,
    API_HYDROLOGICAL_ENDPOINT,
    API_HYDROLOGICAL_WARNINGS_ENDPOINT,
    API_WEATHER_ENDPOINT,
    API_WEATHER_WARNINGS_ENDPOINT,
    DATA_VALIDITY_PERIOD,
    DATE_FORMAT,
    HEADERS,
    HYDROLOGICAL_ALERTS_MAP,
    NO_ALERT,
    TIMEOUT,
    WEATHER_ALERTS_MAP,
    WEATHER_STATIONS_INFO_FILE,
)
from .exceptions import ApiError
from .model import Alert, ApiNames, HydrologicalData, SensorData, Units, WeatherData
from .utils import create_sensor_data, gen_station_name, get_datetime, is_data_current

__all__ = ["ImgwPib", "SensorData"]

_LOGGER = logging.getLogger(__name__)


class ImgwPib:
    """Main class of IMGW-PIB API wrapper."""

    def __init__(
        self: Self,
        session: ClientSession,
        weather_station_id: str | None = None,
        hydrological_station_id: str | None = None,
        hydrological_details: bool = True,
    ) -> None:
        """Initialize IMGW-PIB API wrapper."""
        self._session = session
        self._weather_station_list: dict[str, str] = {}
        self._hydrological_station_list: dict[str, str] = {}
        self._alarm_water_level: float | None = None
        self._warning_water_level: float | None = None

        self.weather_station_id = weather_station_id
        self.hydrological_station_id = hydrological_station_id

        self._hydrological_details = hydrological_details

        self._weather_stations_info: dict[str, dict[str, Any]] = {}

    @classmethod
    async def create(
        cls: type[Self],
        session: ClientSession,
        weather_station_id: str | None = None,
        hydrological_station_id: str | None = None,
        hydrological_details: bool = True,
    ) -> Self:
        """Create a new instance."""
        instance = cls(
            session, weather_station_id, hydrological_station_id, hydrological_details
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
            _LOGGER.debug("Using weather station ID: %s", self.weather_station_id)
            await self.update_weather_stations()

            if self.weather_station_id not in self.weather_stations:
                msg = f"Invalid weather station ID: {self.weather_station_id}"
                raise ApiError(msg)

            async with aiofiles.open(WEATHER_STATIONS_INFO_FILE, mode="rb") as file:
                content = await file.read()
            self._weather_stations_info = orjson.loads(content)

        if self.hydrological_station_id is not None:
            _LOGGER.debug(
                "Using hydrological station ID: %s", self.hydrological_station_id
            )

            await self.update_hydrological_stations()

            if self.hydrological_station_id not in self.hydrological_stations:
                msg = f"Invalid hydrological station ID: {self.hydrological_station_id}"
                raise ApiError(msg)

            if self._hydrological_details is True:
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

        url = API_WEATHER_ENDPOINT / "id" / self.weather_station_id
        weather_data = await self._http_request(url)

        _LOGGER.debug("Weather data: %s", weather_data)

        weather_alerts = []
        if (
            teryt := self._weather_stations_info.get(self.weather_station_id, {}).get(
                "teryt"
            )
        ) and (
            result := await self._http_request(API_WEATHER_WARNINGS_ENDPOINT, False)
        ):
            weather_alerts = result

        weather_alert = self._extract_weather_alert(weather_alerts, teryt)

        _LOGGER.debug("Weather alert: %s", weather_alert)

        return self._parse_weather_data(weather_data, weather_alert)

    def _extract_weather_alert(
        self, weather_alerts: list[dict[str, Any]], teryt: str | None
    ) -> Alert:
        """Extract weather alert for a given TERYT."""
        if teryt is None:
            return Alert(value=NO_ALERT)

        now = datetime.now(tz=UTC)

        for alert in reversed(weather_alerts):
            territories = alert[ApiNames.TERRITORY]

            if teryt not in territories:
                continue

            from_date = get_datetime(alert[ApiNames.VALID_FROM], DATE_FORMAT)
            to_date = get_datetime(alert[ApiNames.VALID_TO], DATE_FORMAT)

            if from_date is None or to_date is None:
                continue

            if (from_date - DATA_VALIDITY_PERIOD) <= now <= to_date:
                event = alert[ApiNames.EVENT_NAME].lower()
                return Alert(
                    value=WEATHER_ALERTS_MAP.get(event, event),
                    valid_from=from_date,
                    valid_to=to_date,
                    probability=alert[ApiNames.PROBABILITY],
                    level=ALERT_LEVEL_MAP[alert[ApiNames.ALERT_LEVEL]],
                )

        return Alert(value=NO_ALERT)

    async def update_hydrological_stations(self: Self) -> None:
        """Update list of hydrological stations."""
        stations_data = await self._http_request(API_HYDROLOGICAL_ENDPOINT)

        self._hydrological_station_list = {
            station[ApiNames.STATION_ID]: gen_station_name(
                station[ApiNames.STATION], station[ApiNames.RIVER]
            )
            for station in stations_data
        }

    async def _update_hydrological_details(self: Self) -> None:
        """Update hydrological details."""
        if TYPE_CHECKING:
            assert self.hydrological_station_id

        url = API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(
            id=self.hydrological_station_id
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

        hydrological_data = None
        for item in all_stations_data:
            if item.get(ApiNames.STATION_ID) == self.hydrological_station_id:
                hydrological_data = item
                break

        if hydrological_data is None:
            msg = f"No hydrological data for station ID: {self.hydrological_station_id}"
            raise ApiError(msg)

        _LOGGER.debug("Hydrological data: %s", hydrological_data)

        hydrological_alerts = []

        if result := await self._http_request(
            API_HYDROLOGICAL_WARNINGS_ENDPOINT, False
        ):
            hydrological_alerts = result

        return self._parse_hydrological_data(hydrological_data, hydrological_alerts)

    async def _http_request(self: Self, url: URL, required: bool = True) -> Any:  # noqa: ANN401
        """Make an HTTP request."""
        _LOGGER.debug("Requesting %s", url)

        response = await self._session.request(
            "get", url, headers=HEADERS, timeout=TIMEOUT
        )

        _LOGGER.debug("Response status: %s", response.status)

        if response.status != HTTPStatus.OK.value:
            msg = f"Invalid response: {response.status}"
            if required:
                raise ApiError(msg)

            return None

        if "application/json" not in response.content_type:
            msg = f"Invalid content type: {response.content_type}"
            raise ApiError(msg)

        return await response.json()

    def _parse_weather_data(self, data: dict[str, Any], alert: Alert) -> WeatherData:
        """Parse weather data."""
        temperature_sensor = create_sensor_data(
            "Temperature", data[ApiNames.TEMPERATURE], Units.CELSIUS.value
        )
        humidity_sensor = create_sensor_data(
            "Humidity", data[ApiNames.HUMIDITY], Units.PERCENT.value
        )
        wind_speed_sensor = create_sensor_data(
            "Wind Speed", data[ApiNames.WIND_SPEED], Units.METERS_PER_SECOND.value
        )
        wind_direction_sensor = create_sensor_data(
            "Wind Direction", data[ApiNames.WIND_DIRECTION], Units.DEGREE.value
        )
        precipitation_sensor = create_sensor_data(
            "Precipitation", data[ApiNames.PRECIPITATION], Units.MILLIMETERS.value
        )
        pressure_sensor = create_sensor_data(
            "Pressure", data[ApiNames.PRESSURE], Units.HPA.value
        )
        measurement_date = get_datetime(
            f"{data[ApiNames.MEASUREMENT_DATE]} {data[ApiNames.MEASUREMENT_TIME]}",
            "%Y-%m-%d %H",
        )

        if TYPE_CHECKING:
            assert self.weather_station_id

        station = self._weather_stations_info.get(self.weather_station_id, {})

        return WeatherData(
            temperature=temperature_sensor,
            humidity=humidity_sensor,
            pressure=pressure_sensor,
            wind_speed=wind_speed_sensor,
            wind_direction=wind_direction_sensor,
            precipitation=precipitation_sensor,
            station=data[ApiNames.STATION],
            latitude=station.get(ApiNames.LATITUDE),
            longitude=station.get(ApiNames.LONGITUDE),
            station_id=self.weather_station_id,
            measurement_date=measurement_date,
            weather_alert=alert,
        )

    def _parse_hydrological_data(
        self: Self, data: dict[str, Any], alerts: list[dict[str, Any]]
    ) -> HydrologicalData:
        """Parse hydrological data."""
        now = datetime.now(tz=UTC)

        water_level_measurement_date = get_datetime(
            data[ApiNames.WATER_LEVEL_MEASUREMENT_DATE],
            DATE_FORMAT,
        )
        water_level_measurement_date, water_level_current = is_data_current(
            data[ApiNames.WATER_LEVEL_MEASUREMENT_DATE], now
        )
        water_level = data[ApiNames.WATER_LEVEL] if water_level_current else None

        if water_level is None:
            msg = "Invalid water level value"
            raise ApiError(msg)

        water_level_sensor = create_sensor_data(
            "Water Level", water_level, Units.CENTIMETERS.value
        )
        flood_warning_level_sensor = create_sensor_data(
            "Flood Warning Level",
            self._warning_water_level,
            Units.CENTIMETERS.value,
        )
        flood_alarm_level_sensor = create_sensor_data(
            "Flood Alarm Level", self._alarm_water_level, Units.CENTIMETERS.value
        )

        water_temperature_measurement_date, water_temperature_current = is_data_current(
            data[ApiNames.WATER_TEMPERATURE_MEASUREMENT_DATE], now
        )
        water_temperature = (
            data[ApiNames.WATER_TEMPERATURE] if water_temperature_current else None
        )
        if not water_temperature_current:
            water_temperature_measurement_date = None

        water_temperature_sensor = create_sensor_data(
            "Water Temperature", water_temperature, Units.CELSIUS.value
        )

        water_flow_measurement_date, water_flow_current = is_data_current(
            data[ApiNames.WATER_FLOW_MEASUREMENT_DATE], now
        )

        water_flow = data[ApiNames.WATER_FLOW] if water_flow_current else None
        if not water_flow_current:
            water_flow_measurement_date = None

        water_flow_sensor = create_sensor_data(
            "Water Flow", water_flow, Units.CUBIC_METERS_PER_SECOND.value
        )

        river = data[ApiNames.RIVER]

        hydrological_alert = self._extract_hydrological_alert(
            alerts, river, data[ApiNames.PROVINCE]
        )

        _LOGGER.debug("Hydrological alert: %s", hydrological_alert)

        if TYPE_CHECKING:
            assert self.hydrological_station_id

        return HydrologicalData(
            flood_alarm_level=flood_alarm_level_sensor,
            flood_warning_level=flood_warning_level_sensor,
            latitude=float(data[ApiNames.LATITUDE]),
            longitude=float(data[ApiNames.LONGITUDE]),
            river=river,
            station_id=self.hydrological_station_id,
            station=data[ApiNames.STATION].strip(),
            water_flow=water_flow_sensor,
            water_flow_measurement_date=water_flow_measurement_date,
            water_level_measurement_date=water_level_measurement_date,
            water_level=water_level_sensor,
            water_temperature_measurement_date=water_temperature_measurement_date,
            water_temperature=water_temperature_sensor,
            hydrological_alert=hydrological_alert,
        )

    def _extract_hydrological_alert(
        self,
        hydrological_alerts: list[dict[str, Any]],
        river: str,
        province: str,
    ) -> Alert:
        """Extract hydrological alert for a given river."""
        now = datetime.now(tz=UTC)
        river_key = river.rsplit(" ", maxsplit=1)[-1][:-1].lower()
        province_key = province.lower()

        for alert in reversed(hydrological_alerts):
            areas = alert[ApiNames.AREAS]
            province_match = False
            river_match = False

            for area in areas:
                if (
                    not province_match
                    and area[ApiNames.PROVINCE].lower() == province_key
                ):
                    province_match = True
                if not river_match and river_key in area[ApiNames.DESCRIPTION].lower():
                    river_match = True
                # Early exit if both conditions are met
                if province_match and river_match:
                    break

            if not (province_match and river_match):
                continue

            from_date = get_datetime(alert[ApiNames.DATE_FROM], DATE_FORMAT)
            to_date = get_datetime(alert[ApiNames.DATE_TO], DATE_FORMAT)

            if from_date is None or to_date is None:
                continue

            if from_date <= now <= to_date:
                event = alert[ApiNames.EVENT].lower()
                return Alert(
                    value=HYDROLOGICAL_ALERTS_MAP.get(event, event),
                    valid_from=from_date,
                    valid_to=to_date,
                    probability=alert[ApiNames.PROBABILITY],
                    level=ALERT_LEVEL_MAP[alert[ApiNames.ALERT_LEVEL_HYDROLOGICAL]],
                )

        return Alert(value=NO_ALERT)
