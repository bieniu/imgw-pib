"""Type definitions for IMGW-PIB."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Self


@dataclass
class ImgwPibData:
    """IMGW-PIB data class."""


@dataclass
class SensorData:
    """Data class for sensor."""

    name: str
    value: float | None = None
    unit: str | None = None


@dataclass
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
    measurement_date: datetime | None


@dataclass
class HydrologicalData(ImgwPibData):
    """Hudrological Data class for IMGW-PIB."""

    water_level: SensorData
    warning_water_level: SensorData
    alarm_water_level: SensorData
    water_temperature: SensorData
    station: str
    river: str
    station_id: str
    water_level_measurement_date: datetime | None
    water_temperature_measurement_date: datetime | None
    alarm_level: bool | None = None
    warning_level: bool | None = None

    def __post_init__(self: Self) -> None:
        """Call after initialization."""
        if self.water_level.value is not None:
            if self.alarm_water_level.value is not None:
                self.alarm_level = (
                    self.water_level.value >= self.alarm_water_level.value
                )
            if self.warning_water_level.value is not None:
                self.warning_level = (
                    self.water_level.value >= self.warning_water_level.value
                )


class ApiNames(StrEnum):
    """Names type for API."""

    HUMIDITY = "wilgotnosc_wzgledna"
    MEASUREMENT_DATE = "data_pomiaru"
    MEASUREMENT_TIME = "godzina_pomiaru"
    PRECIPITATION = "suma_opadu"
    PRESSURE = "cisnienie"
    RIVER = "rzeka"
    STATION = "stacja"
    STATION_ID = "id_stacji"
    TEMPERATURE = "temperatura"
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
    DEGREE = "°"
    HPA = "hPa"
    METERS_PER_SECOND = "m/s"
    MILLIMETERS = "mm"
    PERCENT = "%"
