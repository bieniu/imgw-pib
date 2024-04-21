"""IMDB-PIB exceptions."""

from typing import Self


class ImdbPibError(Exception):
    """Base class for imdb-pib errors."""


class ApiError(ImdbPibError):
    """Raised to indicate API error."""

    def __init__(self: Self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status
