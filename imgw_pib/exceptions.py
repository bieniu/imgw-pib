"""IMDB-PIB exceptions."""

from typing import Self


class ImgwPibError(Exception):
    """Base class for imgw-pib errors."""


class ApiError(ImgwPibError):
    """Raised to indicate API error."""

    def __init__(self: Self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status
