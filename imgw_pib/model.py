"""Type definitions for IMGW-PIB."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Self


@dataclass
class ImgwPibData:
    """IMGW-PIB data class."""


@dataclass(kw_only=True, slots=True)
class SensorData:
    """Data class for sensor."""

    name: str
    value: float | None = None
    unit: str | None = None


@dataclass(kw_only=True, slots=True)
class Alert:
    """Data class for alert."""

    value: str
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    probability: int | None = None
    level: str | None = None


@dataclass(kw_only=True, slots=True)
class WeatherData(ImgwPibData):
    """Weather Data class for IMGW-PIB."""

    temperature: SensorData
    humidity: SensorData
    pressure: SensorData
    wind_speed: SensorData
    wind_direction: SensorData
    precipitation: SensorData

    station: str
    station_id: str
    latitude: float | None = None
    longitude: float | None = None

    measurement_date: datetime | None

    weather_alert: Alert


@dataclass(kw_only=True, slots=True)
class HydrologicalData(ImgwPibData):
    """Hydrological Data class for IMGW-PIB."""

    water_level: SensorData
    water_level_measurement_date: datetime | None
    water_temperature: SensorData
    water_temperature_measurement_date: datetime | None
    water_flow: SensorData
    water_flow_measurement_date: datetime | None

    flood_alarm: bool | None = None
    flood_alarm_level: SensorData
    flood_warning: bool | None = None
    flood_warning_level: SensorData

    river: str
    station_id: str
    station: str
    latitude: float | None = None
    longitude: float | None = None

    hydrological_alert: Alert

    def __post_init__(self: Self) -> None:
        """Call after initialization."""
        if self.water_level.value is not None:
            if self.flood_alarm_level.value is not None:
                self.flood_alarm = (
                    self.water_level.value >= self.flood_alarm_level.value
                )
            if self.flood_warning_level.value is not None:
                self.flood_warning = (
                    self.water_level.value >= self.flood_warning_level.value
                )


class ApiNames(StrEnum):
    """Names type for API."""

    ALERT_LEVEL = "stopien"
    ALERT_LEVEL_HYDROLOGICAL = "stopień"
    AREA = "obszar"
    DATE_FROM = "data_od"
    DATE_TO = "data_do"
    EVENT = "zdarzenie"
    EVENT_NAME = "nazwa_zdarzenia"
    HUMIDITY = "wilgotnosc_wzgledna"
    LATITUDE = "lat"
    LONGITUDE = "lon"
    MEASUREMENT_DATE = "data_pomiaru"
    MEASUREMENT_TIME = "godzina_pomiaru"
    PRECIPITATION = "suma_opadu"
    PRESSURE = "cisnienie"
    PROBABILITY = "prawdopodobienstwo"
    RIVER = "rzeka"
    STATE = "stan"
    STATE_DATE = "stan_data"
    STATION = "stacja"
    STATION_CODE = "kod_stacji"
    STATION_ID = "id_stacji"
    STATION_NAME = "nazwa_stacji"
    TEMPERATURE = "temperatura"
    TERRITORY = "teryt"
    VALID_FROM = "obowiazuje_od"
    VALID_TO = "obowiazuje_do"
    PROVINCE = "wojewodztwo"
    WATER_FLOW = "przelyw"
    WATER_FLOW_MEASUREMENT_DATE = "przeplyw_data"
    WATER_LEVEL = "stan_wody"
    WATER_LEVEL_MEASUREMENT_DATE = "stan_wody_data_pomiaru"
    WATER_TEMPERATURE = "temperatura_wody"
    WATER_TEMPERATURE_MEASUREMENT_DATE = "temperatura_wody_data_pomiaru"
    WIND_DIRECTION = "kierunek_wiatru"
    WIND_SPEED = "predkosc_wiatru"


class Units(StrEnum):
    """Units."""

    CELSIUS = "°C"
    CENTIMETERS = "cm"
    CUBIC_METERS_PER_SECOND = "m³/s"
    DEGREE = "°"
    HPA = "hPa"
    METERS_PER_SECOND = "m/s"
    MILLIMETERS = "mm"
    PERCENT = "%"
