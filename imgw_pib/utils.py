"""Utils for imgw-pib."""

import logging
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from .const import (
    DATA_VALIDITY_PERIOD,
    DATE_FORMAT,
    ICON_TO_CONDITION,
    VEGETATION_DIGIT_TO_PERCENT,
)
from .model import SensorData

_WARSAW_TZ = ZoneInfo("Europe/Warsaw")
_LOGGER = logging.getLogger(__name__)

_ICON_MIN_LEN = 6
_PRECIP_CODE_MIN = 50
_PRECIP_RAIN_MIN = 60
_PRECIP_SLEET_MIN = 67
_PRECIP_SNOW_MIN = 70
_PRECIP_HEAVY_MIN = 80
_CLOUD_PARTLY_THRESHOLD = 5


def gen_station_name(station: str, river: str) -> str:
    """Generate station name."""
    if river == "-":
        return station.strip()

    river = re.sub(r"\b[Jj]ez\.\s*", "Jezioro ", river)
    river = re.sub(r"\b[Zz]b\.?\s", "Zbiornik ", river)

    return f"{river} ({station.strip()})"


def get_datetime(date_time: str | None, date_format: str) -> datetime | None:
    """Get datetime object from date-time string."""
    if date_time is None:
        return None

    try:
        return datetime.strptime(date_time, date_format).replace(tzinfo=_WARSAW_TZ)
    except (TypeError, ValueError) as exc:
        _LOGGER.debug("Invalid date-time string '%s', %s", date_time, exc)
        return None


def _precip_type(precip: int) -> str | None:
    if precip >= _PRECIP_HEAVY_MIN:
        return "rain_heavy"
    if precip >= _PRECIP_SNOW_MIN:
        return "snow"
    if precip >= _PRECIP_SLEET_MIN:
        return "sleet"
    if precip >= _PRECIP_RAIN_MIN:
        return "rain"
    if precip >= _PRECIP_CODE_MIN:
        return "drizzle"

    return None


def parse_weather_icon(icon: str) -> str | None:
    """Parse weather icon code to weather condition string.

    Format: n{cloud}z{precip}{d/n} e.g. n4z61d
    """
    if not icon or not isinstance(icon, str) or len(icon) < _ICON_MIN_LEN:
        return None

    try:
        if icon[0] == "n" and icon[2] == "z":
            cloud = int(icon[1])
            precip = int(icon[3:5])
            time_of_day = icon[-1] if icon[-1] in ("d", "n") else "d"
        else:
            return None
    except (ValueError, IndexError):
        return None

    pt = _precip_type(precip)

    if pt is not None:
        return ICON_TO_CONDITION.get((pt, time_of_day), "rainy")

    if cloud <= 1:
        key = ("clear", time_of_day)
    elif cloud <= _CLOUD_PARTLY_THRESHOLD:
        key = ("partly", time_of_day)
    else:
        key = ("cloudy", time_of_day)

    return ICON_TO_CONDITION.get(key, "cloudy")


def create_sensor_data(name: str, value: float | str | None, unit: str) -> SensorData:
    """Create sensor data helper."""
    if value is not None:
        return SensorData(name=name, value=float(value), unit=unit)

    return SensorData(name=name, value=None, unit=None)


def is_data_current(
    measurement_date_str: str | None,
    now: datetime,
    data_validity_period: timedelta = DATA_VALIDITY_PERIOD,
) -> tuple[datetime | None, bool]:
    """Check if data is current."""
    if measurement_date_str is None:
        return None, False

    measurement_date = get_datetime(measurement_date_str, DATE_FORMAT)
    if measurement_date is None:
        return None, False

    return measurement_date, now - measurement_date < data_validity_period


def decode_vegetation_phenomena(
    value: str | None,
) -> tuple[float | None, float | None, float | None]:
    """Decode vegetation phenomena code into submerged, floating, and emergent coverage.

    The code is a 3-digit number where:
    - hundreds digit encodes submerged (bottom) vegetation coverage
    - tens digit encodes floating vegetation coverage
    - units digit encodes emergent vegetation coverage

    Digit values: 0 = none, 1 = 1/3 (~33%), 2 = 2/3 (~67%), 3 = full (100%).
    """
    if not isinstance(value, str) or not value.isdigit():
        _LOGGER.info(
            "Invalid vegetation phenomena code %s; expected a 3-digit string",
            value,
        )
        return None, None, None

    value_int = int(value)
    digits = (value_int // 100, (value_int % 100) // 10, value_int % 10)
    if any(d not in VEGETATION_DIGIT_TO_PERCENT for d in digits):
        _LOGGER.info(
            "Invalid vegetation phenomena code %s (digits: %s); each digit must be 0-3",
            value,
            digits,
        )
        return None, None, None

    submerged = VEGETATION_DIGIT_TO_PERCENT[digits[0]]
    floating = VEGETATION_DIGIT_TO_PERCENT[digits[1]]
    emergent = VEGETATION_DIGIT_TO_PERCENT[digits[2]]

    return submerged, floating, emergent
