"""Python wrapper for IMGW-PIB API."""

import logging
from datetime import UTC, datetime
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Self

from aiohttp import ClientSession
from yarl import URL

from .const import (
    ALERT_LEVEL_MAP,
    API_HYDROLOGICAL_DETAILS_ENDPOINT,
    API_HYDROLOGICAL_ENDPOINT,
    API_HYDROLOGICAL_ENDPOINT_2,
    API_WEATHER_ENDPOINT,
    API_WEATHER_WARNINGS_ENDPOINT,
    DATA_VALIDITY_PERIOD,
    DATE_FORMAT,
    HEADERS,
    ID_TO_TERYT_MAP,
    RIVER_NAMES,
    TIMEOUT,
    WEATHER_ALERTS_MAP,
)
from .exceptions import ApiError
from .model import (
    ApiNames,
    HydrologicalData,
    SensorData,
    Units,
    WeatherAlert,
    WeatherData,
)
from .utils import gen_station_name, get_datetime

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
        self._use_hydrological_endpoint_2 = False

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

        weather_alert = None

        if teryt := ID_TO_TERYT_MAP.get(self.weather_station_id):
            weather_alerts = await self._http_request(API_WEATHER_WARNINGS_ENDPOINT)
            weather_alert = self._extract_weather_alert(weather_alerts, teryt)

        _LOGGER.debug("Weather alert: %s", weather_alert)

        return self._parse_weather_data(weather_data, weather_alert)

    def _extract_weather_alert(
        self, weather_alerts: list[dict[str, Any]], teryt: str
    ) -> WeatherAlert | None:
        """Extract weather alert for a given TERYT."""
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
                return WeatherAlert(
                    event=WEATHER_ALERTS_MAP.get(event, event),
                    valid_from=from_date,
                    valid_to=to_date,
                    probability=alert[ApiNames.PROBABILITY],
                    level=ALERT_LEVEL_MAP[alert[ApiNames.ALERT_LEVEL]],
                )

        return None

    async def update_hydrological_stations(self: Self) -> None:
        """Update list of hydrological stations."""
        stations_data = await self._http_request(API_HYDROLOGICAL_ENDPOINT)

        self._hydrological_station_list = {
            station[ApiNames.STATION_ID]: gen_station_name(
                station[ApiNames.STATION], station[ApiNames.RIVER]
            )
            for station in stations_data
        }

        stations_data = await self._http_request(API_HYDROLOGICAL_ENDPOINT_2)

        hydrological_station_list_2 = {}
        hydrological_station_list_2.update(
            {
                station_id: gen_station_name(
                    station[ApiNames.STATION_NAME].title(), river_name
                )
                for station in stations_data
                if (station_id := station[ApiNames.STATION_CODE])
                not in self._hydrological_station_list
                and (river_name := RIVER_NAMES.get(station_id))
            }
        )

        if self.hydrological_station_id in hydrological_station_list_2:
            self._use_hydrological_endpoint_2 = True

        self._hydrological_station_list.update(hydrological_station_list_2)

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

        if self._use_hydrological_endpoint_2 is False:
            all_stations_data = await self._http_request(API_HYDROLOGICAL_ENDPOINT)

            hydrological_data = next(
                (
                    item
                    for item in all_stations_data
                    if item.get(ApiNames.STATION_ID) == self.hydrological_station_id
                ),
                None,
            )
        else:
            all_stations_data = await self._http_request(API_HYDROLOGICAL_ENDPOINT_2)

            hydrological_data = next(
                (
                    item
                    for item in all_stations_data
                    if item.get(ApiNames.STATION_CODE) == self.hydrological_station_id
                    and item.get(ApiNames.STATION_CODE) in RIVER_NAMES
                ),
                None,
            )

        if hydrological_data is None:
            msg = f"No hydrological data for station ID: {self.hydrological_station_id}"
            raise ApiError(msg)

        _LOGGER.debug("Hydrological data: %s", hydrological_data)

        return self._parse_hydrological_data(hydrological_data)

    async def _http_request(self: Self, url: URL) -> Any:  # noqa: ANN401
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
    def _parse_weather_data(
        data: dict[str, Any], alert: WeatherAlert | None
    ) -> WeatherData:
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
            alert=alert,
        )

    def _parse_hydrological_data(self: Self, data: dict[str, Any]) -> HydrologicalData:
        """Parse hydrological data."""
        now = datetime.now(tz=UTC)

        water_level_measurement_date = get_datetime(
            data.get(ApiNames.WATER_LEVEL_MEASUREMENT_DATE)
            or data.get(ApiNames.STATE_DATE),
            DATE_FORMAT,
        )
        if (
            water_level_measurement_date is not None
            and now - water_level_measurement_date < DATA_VALIDITY_PERIOD
        ):
            water_level = data.get(ApiNames.WATER_LEVEL) or data.get(ApiNames.STATE)
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
            data.get(ApiNames.WATER_TEMPERATURE_MEASUREMENT_DATE),
            DATE_FORMAT,
        )
        if (
            water_temperature_measurement_date is not None
            and now - water_temperature_measurement_date < DATA_VALIDITY_PERIOD
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

        water_flow_measurement_date = get_datetime(
            data.get(ApiNames.WATER_FLOW_MEASUREMENT_DATE),
            DATE_FORMAT,
        )
        if (
            water_flow_measurement_date is not None
            and now - water_flow_measurement_date < DATA_VALIDITY_PERIOD
        ):
            water_flow = data.get(ApiNames.WATER_FLOW)
        else:
            water_flow_measurement_date = None
            water_flow = None

        water_flow_sensor = SensorData(
            name="Water Flow",
            value=float(water_flow) if water_flow is not None else None,
            unit=Units.CUBIC_METERS_PER_SECOND.value
            if water_flow is not None
            else None,
        )

        return HydrologicalData(
            flood_alarm_level=flood_alarm_level_sensor,
            flood_warning_level=flood_warning_level_sensor,
            latitude=float(data[ApiNames.LATITUDE]),
            longitude=float(data[ApiNames.LONGITUDE]),
            river=data.get(ApiNames.RIVER) or RIVER_NAMES[data[ApiNames.STATION_CODE]],
            station_id=data.get(ApiNames.STATION_ID) or data[ApiNames.STATION_CODE],
            station=(
                data.get(ApiNames.STATION) or data[ApiNames.STATION_NAME].title()
            ).strip(),
            water_flow=water_flow_sensor,
            water_flow_measurement_date=water_flow_measurement_date,
            water_level_measurement_date=water_level_measurement_date,
            water_level=water_level_sensor,
            water_temperature_measurement_date=water_temperature_measurement_date,
            water_temperature=water_temperature_sensor,
        )
