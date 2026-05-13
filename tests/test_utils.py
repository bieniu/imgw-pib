"""Tests for imgw_pib.utils module."""

import pytest

from imgw_pib.utils import parse_weather_icon


@pytest.mark.parametrize(
    ("icon", "expected"),
    [
        ("n4z80d", "pouring"),
        ("n4z99n", "pouring"),
        ("n4z70d", "snowy"),
        ("n4z75n", "snowy"),
        ("n4z67d", "snowy-rainy"),
        ("n4z69n", "snowy-rainy"),
        ("n4z60d", "rainy"),
        ("n4z66n", "rainy"),
        ("n4z50d", "rainy"),
        ("n4z59n", "rainy"),
        ("n0z00d", "sunny"),
        ("n1z00n", "clear-night"),
        ("n3z00d", "partlycloudy"),
        ("n5z00n", "partlycloudy"),
        ("n6z00d", "cloudy"),
        ("n8z00n", "cloudy"),
        ("x4z61d", None),
        ("n4a61d", None),
        ("n4z6", None),
        ("", None),
    ],
)
def test_parse_weather_icon(icon: str, expected: str | None) -> None:
    """Test parse_weather_icon for all precip types and cloud levels."""
    assert parse_weather_icon(icon) == expected


def test_parse_weather_icon_non_string() -> None:
    """Test parse_weather_icon with a non-string input."""
    assert parse_weather_icon(None) is None  # ty: ignore[invalid-argument-type]


def test_parse_weather_icon_invalid_digits() -> None:
    """Test parse_weather_icon when cloud/precip digits are non-numeric."""
    assert parse_weather_icon("nXzYYd") is None
