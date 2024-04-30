"""Utils for imgw-pib."""

import logging
from datetime import UTC, datetime

_LOGGER = logging.getLogger(__name__)


def gen_station_name(station: str, river: str) -> str:
    """Generate station name."""
    if river == "-":
        return station

    return f"{river} ({station})"


def get_datetime(date_time: str | None, date_format: str) -> datetime | None:
    """Get datetime object from date-time string."""
    if date_time is None:
        return None

    try:
        return datetime.strptime(date_time, date_format).replace(tzinfo=UTC)
    except (TypeError, ValueError) as exc:
        _LOGGER.debug("Invalid date-time string '%s', %s", date_time, exc)
        return None
