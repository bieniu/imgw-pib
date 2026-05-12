"""Utils for imgw-pib."""

import logging
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from .const import DATA_VALIDITY_PERIOD, DATE_FORMAT, VEGETATION_DIGIT_TO_PERCENT
from .model import SensorData

_WARSAW_TZ = ZoneInfo("Europe/Warsaw")
_LOGGER = logging.getLogger(__name__)


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
    value: int | None,
) -> tuple[float | None, float | None, float | None]:
    """Decode vegetation phenomena code into submerged, floating, and emergent coverage.

    The code is a 3-digit number where:
    - hundreds digit encodes submerged (bottom) vegetation coverage
    - tens digit encodes floating vegetation coverage
    - units digit encodes emergent vegetation coverage

    Digit values: 0 = none, 1 = 1/3 (~33%), 2 = 2/3 (~67%), 3 = full (100%).
    """
    if value is None:
        return None, None, None

    submerged = VEGETATION_DIGIT_TO_PERCENT.get(value // 100, 0)
    floating = VEGETATION_DIGIT_TO_PERCENT.get((value % 100) // 10, 0)
    emergent = VEGETATION_DIGIT_TO_PERCENT.get(value % 10, 0)

    return submerged, floating, emergent
