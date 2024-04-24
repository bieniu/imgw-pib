"""Utils for imgw-pib."""

from datetime import UTC, datetime


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
        return None
