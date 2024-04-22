"""Tests for imgw-pib package."""

from http import HTTPStatus
from typing import Any

import aiohttp
import pytest
from aioresponses import aioresponses
from syrupy import SnapshotAssertion

from imgw_pib import ImgwPib
from imgw_pib.const import API_ENDPOINT
from imgw_pib.exceptions import ApiError


@pytest.mark.asyncio()
async def test_weather_stations(
    snapshot: SnapshotAssertion, weather_stations: list[dict[str, Any]]
) -> None:
    """Test weather stations."""
    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(API_ENDPOINT, payload=weather_stations)

        imgwpib = await ImgwPib.create(session)

    await session.close()

    assert imgwpib.stations == snapshot


@pytest.mark.asyncio()
async def test_weather_station(
    snapshot: SnapshotAssertion,
    weather_stations: list[dict[str, Any]],
    weather_station: dict[str, Any],
) -> None:
    """Test weather station."""
    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(API_ENDPOINT, payload=weather_stations)
        session_mock.get(f"{API_ENDPOINT}/id/12295", payload=weather_station)

        imgwpib = await ImgwPib.create(session, "12295")
        weather = await imgwpib.get_weather_data()

    await session.close()

    assert weather == snapshot


@pytest.mark.asyncio()
async def test_wrong_weather_station_id(weather_stations: list[dict[str, Any]]) -> None:
    """Test wrong weather station ID."""
    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(API_ENDPOINT, payload=weather_stations)

        with pytest.raises(ApiError) as exc_info:
            await ImgwPib.create(session, "abcd1234")

    await session.close()

    assert str(exc_info.value) == "Invalid weather station ID: abcd1234"


@pytest.mark.asyncio()
async def test_api_error() -> None:
    """Test API error."""
    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(
            API_ENDPOINT,
            status=HTTPStatus.BAD_REQUEST.value,
            payload={"errors": [{"code": "badRequest"}]},
        )

        with pytest.raises(ApiError) as exc:
            await ImgwPib.create(session)

    await session.close()

    assert str(exc.value) == "Invalid response: 400"
