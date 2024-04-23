"""Tests for imgw-pib package."""

from http import HTTPStatus
from typing import Any

import aiohttp
import pytest
from aioresponses import aioresponses
from syrupy import SnapshotAssertion

from imgw_pib import ImgwPib
from imgw_pib.const import API_HYDROLOGICAL_ENDPOINT, API_WEATHER_ENDPOINT
from imgw_pib.exceptions import ApiError


@pytest.mark.asyncio()
async def test_weather_stations(
    snapshot: SnapshotAssertion, weather_stations: list[dict[str, Any]]
) -> None:
    """Test weather stations."""
    session = aiohttp.ClientSession()

    imgwpib = await ImgwPib.create(session)

    assert len(imgwpib.weather_stations) == 0

    with aioresponses() as session_mock:
        session_mock.get(API_WEATHER_ENDPOINT, payload=weather_stations)

        await imgwpib.update_weather_stations()

    await session.close()

    assert len(imgwpib.weather_stations)

    assert imgwpib.weather_stations == snapshot


@pytest.mark.asyncio()
async def test_weather_station(
    snapshot: SnapshotAssertion,
    weather_stations: list[dict[str, Any]],
    weather_station: dict[str, Any],
) -> None:
    """Test weather station."""
    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(API_WEATHER_ENDPOINT, payload=weather_stations)
        session_mock.get(f"{API_WEATHER_ENDPOINT}/id/12295", payload=weather_station)

        imgwpib = await ImgwPib.create(session, weather_station_id="12295")
        weather_data = await imgwpib.get_weather_data()

    await session.close()

    assert weather_data == snapshot


@pytest.mark.asyncio()
async def test_wrong_weather_station_id(weather_stations: list[dict[str, Any]]) -> None:
    """Test wrong weather station ID."""
    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(API_WEATHER_ENDPOINT, payload=weather_stations)

        with pytest.raises(ApiError) as exc_info:
            await ImgwPib.create(session, weather_station_id="abcd1234")

    await session.close()

    assert str(exc_info.value) == "Invalid weather station ID: abcd1234"


@pytest.mark.asyncio()
async def test_hydrological_stations(
    snapshot: SnapshotAssertion, hydrological_stations: list[dict[str, Any]]
) -> None:
    """Test hydrological stations."""
    session = aiohttp.ClientSession()

    imgwpib = await ImgwPib.create(session)

    assert len(imgwpib.hydrological_stations) == 0

    with aioresponses() as session_mock:
        session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)

        await imgwpib.update_hydrological_stations()

    await session.close()

    assert imgwpib.hydrological_stations == snapshot


@pytest.mark.asyncio()
async def test_hydrological_station(
    snapshot: SnapshotAssertion,
    hydrological_stations: list[dict[str, Any]],
    hydrological_station: dict[str, Any],
) -> None:
    """Test weather station."""
    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
        session_mock.get(
            f"{API_HYDROLOGICAL_ENDPOINT}/id/154190050", payload=hydrological_station
        )

        imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
        hydrological_data = await imgwpib.get_hydrological_data()

    await session.close()

    assert hydrological_data == snapshot


@pytest.mark.asyncio()
async def test_wrong_weather_hydrological_id(
    hydrological_stations: list[dict[str, Any]],
) -> None:
    """Test wrong hydrological station ID."""
    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)

        with pytest.raises(ApiError) as exc_info:
            await ImgwPib.create(session, hydrological_station_id="abcd1234")

    await session.close()

    assert str(exc_info.value) == "Invalid hydrological station ID: abcd1234"


@pytest.mark.asyncio()
async def test_api_error() -> None:
    """Test API error."""
    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(
            API_WEATHER_ENDPOINT,
            status=HTTPStatus.BAD_REQUEST.value,
            payload={"errors": [{"code": "badRequest"}]},
        )

        with pytest.raises(ApiError) as exc:
            await ImgwPib.create(session, weather_station_id="12345")

    await session.close()

    assert str(exc.value) == "Invalid response: 400"
