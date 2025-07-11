"""Utils for imgw-pib."""

import logging
import re
from datetime import datetime
from zoneinfo import ZoneInfo

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
        return datetime.strptime(date_time, date_format).replace(
            tzinfo=ZoneInfo("Europe/Warsaw")
        )
    except (TypeError, ValueError) as exc:
        _LOGGER.debug("Invalid date-time string '%s', %s", date_time, exc)
        return None
