"""Utils for imgw-pib."""

import logging
from datetime import UTC, datetime

_LOGGER = logging.getLogger(__name__)


def gen_station_name(station: str, river: str) -> str:
    """Generate station name."""
    if river == "-":
        return station

    return f"{river} ({station})"


def get_datetime(date_time: str, date_format: str) -> datetime | None:
    """Get datetime object from date-time string."""
    try:
        return datetime.strptime(date_time, date_format).replace(tzinfo=UTC)
    except (TypeError, ValueError):
        _LOGGER.debug("Invalid date-time string: %s", date_time)
        return None
