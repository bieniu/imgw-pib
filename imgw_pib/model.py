"""Type definitions for IMGW-PIB."""

from dataclasses import dataclass
from datetime import datetime


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
    measurement_time: datetime
