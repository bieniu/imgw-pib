"""Tests for imgw-pib package."""

from datetime import UTC, datetime
from http import HTTPStatus
from typing import Any

import aiohttp
import pytest
from aiointercept import aiointercept
from freezegun import freeze_time
from syrupy import SnapshotAssertion

from imgw_pib import ImgwPib
from imgw_pib.const import (
    API_HYDROLOGICAL_DETAILS_ENDPOINT,
    API_HYDROLOGICAL_ENDPOINT,
    API_HYDROLOGICAL_WARNINGS_ENDPOINT,
    API_WEATHER_ENDPOINT,
    API_WEATHER_PROXY_ENDPOINT,
    API_WEATHER_WARNINGS_ENDPOINT,
)
from imgw_pib.exceptions import ApiError
from imgw_pib.model import ApiNames
from imgw_pib.utils import decode_vegetation_phenomena

TEST_TIME = datetime(2024, 4, 22, 11, 10, 32, tzinfo=UTC)


@pytest.mark.asyncio
async def test_weather_stations(
    snapshot: SnapshotAssertion, weather_stations: list[dict[str, Any]]
) -> None:
    """Test weather stations."""
    session = aiohttp.ClientSession()

    imgwpib = await ImgwPib.create(session)

    assert len(imgwpib.weather_stations) == 0

    async with aiointercept(mock_external_urls=True) as session_mock:
        session_mock.get(API_WEATHER_ENDPOINT, payload=weather_stations)

        await imgwpib.update_weather_stations()

    await session.close()

    assert len(imgwpib.weather_stations)

    assert imgwpib.weather_stations == snapshot


@pytest.mark.asyncio
async def test_weather_station(
    snapshot: SnapshotAssertion,
    weather_stations: list[dict[str, Any]],
    weather_station: dict[str, Any],
    weather_alerts: list[dict[str, Any]],
) -> None:
    """Test weather station (proxy unavailable, falls back to IMGW)."""
    session = aiohttp.ClientSession()

    proxy_url = API_WEATHER_PROXY_ENDPOINT.with_query(lat=49.821877, lon=19.047007)

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_WEATHER_ENDPOINT, payload=weather_stations)
            session_mock.get(API_WEATHER_WARNINGS_ENDPOINT, payload=weather_alerts)
            session_mock.get(proxy_url, status=HTTPStatus.NOT_FOUND.value)
            session_mock.get(
                f"{API_WEATHER_ENDPOINT}/id/12600", payload=weather_station
            )

            imgwpib = await ImgwPib.create(session, weather_station_id="12600")
            weather_data = await imgwpib.get_weather_data()

    await session.close()

    assert weather_data == snapshot


@pytest.mark.asyncio
async def test_no_weather_alerts(
    weather_stations: list[dict[str, Any]],
    weather_station: dict[str, Any],
) -> None:
    """Test weather station with no alerts."""
    session = aiohttp.ClientSession()

    proxy_url = API_WEATHER_PROXY_ENDPOINT.with_query(lat=49.821877, lon=19.047007)

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_WEATHER_ENDPOINT, payload=weather_stations)
            session_mock.get(
                API_WEATHER_WARNINGS_ENDPOINT, status=HTTPStatus.NOT_FOUND.value
            )
            session_mock.get(proxy_url, status=HTTPStatus.NOT_FOUND.value)
            session_mock.get(
                f"{API_WEATHER_ENDPOINT}/id/12600", payload=weather_station
            )

            imgwpib = await ImgwPib.create(session, weather_station_id="12600")
            weather_data = await imgwpib.get_weather_data()

    await session.close()

    assert weather_data.weather_alert.value == "no_alert"


@pytest.mark.asyncio
async def test_weather_station_proxy(
    snapshot: SnapshotAssertion,
    weather_stations: list[dict[str, Any]],
    weather_station_proxy: dict[str, Any],
) -> None:
    """Test weather station using the proxy endpoint as primary data source."""
    session = aiohttp.ClientSession()

    proxy_url = API_WEATHER_PROXY_ENDPOINT.with_query(lat=49.821877, lon=19.047007)

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_WEATHER_ENDPOINT, payload=weather_stations)
            session_mock.get(
                API_WEATHER_WARNINGS_ENDPOINT, status=HTTPStatus.NOT_FOUND.value
            )
            session_mock.get(proxy_url, payload=weather_station_proxy)

            imgwpib = await ImgwPib.create(session, weather_station_id="12600")
            weather_data = await imgwpib.get_weather_data()

    await session.close()

    assert weather_data == snapshot


@pytest.mark.asyncio
async def test_wrong_weather_station_id(weather_stations: list[dict[str, Any]]) -> None:
    """Test wrong weather station ID."""
    session = aiohttp.ClientSession()

    async with aiointercept(mock_external_urls=True) as session_mock:
        session_mock.get(API_WEATHER_ENDPOINT, payload=weather_stations)

        with pytest.raises(ApiError) as exc_info:
            await ImgwPib.create(session, weather_station_id="abcd1234")

    await session.close()

    assert str(exc_info.value) == "Invalid weather station ID: abcd1234"


@pytest.mark.asyncio
async def test_hydrological_stations(
    snapshot: SnapshotAssertion,
    hydrological_stations: list[dict[str, Any]],
) -> None:
    """Test hydrological stations."""
    session = aiohttp.ClientSession()

    imgwpib = await ImgwPib.create(session)

    assert len(imgwpib.hydrological_stations) == 0

    async with aiointercept(mock_external_urls=True) as session_mock:
        session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)

        await imgwpib.update_hydrological_stations()

    await session.close()

    assert imgwpib.hydrological_stations == snapshot


@pytest.mark.asyncio
async def test_hydrological_station(
    snapshot: SnapshotAssertion,
    hydrological_stations: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
    hydrological_alerts: list[dict[str, Any]],
) -> None:
    """Test hydrological station."""
    session = aiohttp.ClientSession()

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                payload=hydrological_details,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
            hydrological_data = await imgwpib.get_hydrological_data()

    await session.close()

    assert hydrological_data == snapshot


@pytest.mark.asyncio
async def test_no_hydrological_alerts(
    hydrological_stations: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
) -> None:
    """Test hydrological station with no alerts."""
    session = aiohttp.ClientSession()

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                payload=hydrological_details,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, status=HTTPStatus.NOT_FOUND.value
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
            hydrological_data = await imgwpib.get_hydrological_data()

    await session.close()

    assert hydrological_data.hydrological_alert.value == "no_alert"


@pytest.mark.asyncio
async def test_wrong_weather_hydrological_id(
    hydrological_stations: list[dict[str, Any]],
) -> None:
    """Test wrong hydrological station ID."""
    session = aiohttp.ClientSession()

    async with aiointercept(mock_external_urls=True) as session_mock:
        session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)

        with pytest.raises(ApiError) as exc_info:
            await ImgwPib.create(session, hydrological_station_id="abcd1234")

    await session.close()

    assert str(exc_info.value) == "Invalid hydrological station ID: abcd1234"


@pytest.mark.asyncio
async def test_api_error() -> None:
    """Test API error."""
    session = aiohttp.ClientSession()

    async with aiointercept(mock_external_urls=True) as session_mock:
        session_mock.get(
            API_WEATHER_ENDPOINT,
            status=HTTPStatus.BAD_REQUEST.value,
            payload={"errors": [{"code": "badRequest"}]},
        )

        with pytest.raises(ApiError) as exc:
            await ImgwPib.create(session, weather_station_id="12345")

    await session.close()

    assert str(exc.value) == "Invalid response: 400"


@pytest.mark.asyncio
async def test_get_weather_data_without_station_id() -> None:
    """Test get_weather_data() without station ID."""
    session = aiohttp.ClientSession()

    imgwpib = await ImgwPib.create(session)

    with pytest.raises(ApiError) as exc:
        await imgwpib.get_weather_data()

    await session.close()

    assert str(exc.value) == "Weather station ID is not set"


@pytest.mark.asyncio
async def test_get_hydrological_data_without_station_id() -> None:
    """Test get_hydrological_data() without station ID."""
    session = aiohttp.ClientSession()

    imgwpib = await ImgwPib.create(session)

    with pytest.raises(ApiError) as exc:
        await imgwpib.get_hydrological_data()

    await session.close()

    assert str(exc.value) == "Hydrological station ID is not set"


@pytest.mark.asyncio
async def test_invalid_water_level_value(
    hydrological_stations: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
    hydrological_alerts: list[dict[str, Any]],
) -> None:
    """Test invalid water level value."""
    session = aiohttp.ClientSession()

    hydrological_stations[5][ApiNames.WATER_LEVEL] = None

    async with aiointercept(mock_external_urls=True) as session_mock:
        session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
        session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
        session_mock.get(
            API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
            payload=hydrological_details,
        )
        session_mock.get(
            API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
        )

        imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")

        with pytest.raises(ApiError) as exc:
            await imgwpib.get_hydrological_data()

    await session.close()

    assert str(exc.value) == "Invalid water level value"


@pytest.mark.parametrize("date_time", [None, "lorem ipsum", "2024-01-22 09:10:00"])
@pytest.mark.asyncio
async def test_invalid_date(
    hydrological_stations: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
    hydrological_alerts: list[dict[str, Any]],
    date_time: str | None,
) -> None:
    """Test invalid water level value."""
    session = aiohttp.ClientSession()

    hydrological_stations[5][ApiNames.WATER_LEVEL_MEASUREMENT_DATE] = date_time

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                payload=hydrological_details,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")

            with pytest.raises(ApiError) as exc_info:
                await imgwpib.get_hydrological_data()

    await session.close()

    assert str(exc_info.value) == "Invalid water level value"


@pytest.mark.parametrize(
    ("water_level", "flood_warning_level", "expected"),
    [(100.0, 200.0, False), (100.0, 100.0, True), (100.0, 50.0, True)],
)
@pytest.mark.asyncio
async def test_flood_warning(
    hydrological_stations: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
    hydrological_alerts: list[dict[str, Any]],
    water_level: float,
    flood_warning_level: float,
    expected: bool,
) -> None:
    """Test flood warning value."""
    session = aiohttp.ClientSession()

    hydrological_stations[5][ApiNames.WATER_LEVEL] = water_level
    hydrological_details["status"]["warningValue"] = flood_warning_level

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                payload=hydrological_details,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
            result = await imgwpib.get_hydrological_data()

    await session.close()

    assert result.flood_warning == expected


@pytest.mark.parametrize(
    ("water_level", "flood_alarm_level", "expected"),
    [(100.0, 200.0, False), (100.0, 100.0, True), (100.0, 50.0, True)],
)
@pytest.mark.asyncio
async def test_flood_alarm(
    hydrological_stations: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
    hydrological_alerts: list[dict[str, Any]],
    water_level: float,
    flood_alarm_level: float,
    expected: bool,
) -> None:
    """Test flood alarm value."""
    session = aiohttp.ClientSession()

    hydrological_stations[5][ApiNames.WATER_LEVEL] = water_level
    hydrological_details["status"]["alarmValue"] = flood_alarm_level

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                payload=hydrological_details,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
            result = await imgwpib.get_hydrological_data()

    await session.close()

    assert result.flood_alarm == expected


@pytest.mark.asyncio
async def test_water_temperature_not_current(
    hydrological_stations: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
    hydrological_alerts: list[dict[str, Any]],
) -> None:
    """Test water_temperature is not current."""
    session = aiohttp.ClientSession()

    # The measurement was performed more than 6 hours before the test time
    hydrological_stations[5][ApiNames.WATER_TEMPERATURE_MEASUREMENT_DATE] = (
        "2024-04-22 05:00:00"
    )

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                payload=hydrological_details,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
            result = await imgwpib.get_hydrological_data()

    await session.close()

    assert result.water_temperature.value is None
    assert result.water_temperature_measurement_date is None


@pytest.mark.asyncio
async def test_hydrological_data_invalid_content(
    hydrological_stations: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
    hydrological_alerts: list[dict[str, Any]],
) -> None:
    """Test when response has invalid content type."""
    session = aiohttp.ClientSession()

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, content_type="text/html")
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                payload=hydrological_details,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
            with pytest.raises(ApiError) as exc_info:
                await imgwpib.get_hydrological_data()

    await session.close()

    assert str(exc_info.value) == "Invalid content type: text/html"


@pytest.mark.asyncio
async def test_no_hydrological_data(
    hydrological_stations: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
) -> None:
    """Test when response has invalid content type."""
    session = aiohttp.ClientSession()

    incomplete_data = hydrological_stations.copy()
    incomplete_data.pop(5)

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=incomplete_data)
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                payload=hydrological_details,
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
            with pytest.raises(ApiError) as exc_info:
                await imgwpib.get_hydrological_data()

    await session.close()

    assert str(exc_info.value) == "No hydrological data for station ID: 154190050"


@pytest.mark.asyncio
async def test_hydrological_details_is_null(
    snapshot: SnapshotAssertion,
    hydrological_stations: list[dict[str, Any]],
    hydrological_alerts: list[dict[str, Any]],
) -> None:
    """Test when hydrological details is null."""
    session = aiohttp.ClientSession()

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                payload=None,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
            hydrological_data = await imgwpib.get_hydrological_data()

    await session.close()

    assert hydrological_data == snapshot


@pytest.mark.asyncio
async def test_hydrological_details_returns_403(
    snapshot: SnapshotAssertion,
    hydrological_stations: list[dict[str, Any]],
    hydrological_alerts: list[dict[str, Any]],
) -> None:
    """Test when hydrological details returns 403."""
    session = aiohttp.ClientSession()

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                status=HTTPStatus.FORBIDDEN.value,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
            hydrological_data = await imgwpib.get_hydrological_data()

    await session.close()

    assert hydrological_data == snapshot


@pytest.mark.asyncio
async def test_hydrological_details_is_false(
    snapshot: SnapshotAssertion,
    hydrological_stations: list[dict[str, Any]],
    hydrological_alerts: list[dict[str, Any]],
) -> None:
    """Test when hydrological_details is False."""
    session = aiohttp.ClientSession()

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(
                session, hydrological_station_id="154190050", hydrological_details=False
            )
            hydrological_data = await imgwpib.get_hydrological_data()

    await session.close()

    assert hydrological_data == snapshot


@pytest.mark.asyncio
async def test_hydrological_station_no_location(
    snapshot: SnapshotAssertion,
    hydrological_station_no_location: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
    hydrological_alerts: list[dict[str, Any]],
) -> None:
    """Test hydrological station."""
    session = aiohttp.ClientSession()

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(
                API_HYDROLOGICAL_ENDPOINT, payload=hydrological_station_no_location
            )
            session_mock.get(
                API_HYDROLOGICAL_ENDPOINT, payload=hydrological_station_no_location
            )
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="153190020"),
                payload=hydrological_details,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="153190020")
            hydrological_data = await imgwpib.get_hydrological_data()

    await session.close()

    assert hydrological_data == snapshot


@pytest.mark.parametrize(
    ("raw_value", "expected_submerged", "expected_floating", "expected_emergent"),
    [
        ("0", 0, 0, 0),
        ("1", 0, 0, 33),
        ("2", 0, 0, 67),
        ("3", 0, 0, 100),
        ("10", 0, 33, 0),
        ("23", 0, 67, 100),
        ("100", 33, 0, 0),
        ("101", 33, 0, 33),
        ("111", 33, 33, 33),
        ("122", 33, 67, 67),
        ("200", 67, 0, 0),
        ("201", 67, 0, 33),
        ("211", 67, 33, 33),
        ("221", 67, 67, 33),
        ("321", 100, 67, 33),
        ("333", 100, 100, 100),
    ],
)
def test_decode_vegetation_phenomena(
    raw_value: str,
    expected_submerged: int,
    expected_floating: int,
    expected_emergent: int,
) -> None:
    """Test decode_vegetation_phenomena decodes all digit positions correctly."""
    submerged, floating, emergent = decode_vegetation_phenomena(raw_value)
    assert submerged == expected_submerged
    assert floating == expected_floating
    assert emergent == expected_emergent


def test_decode_vegetation_phenomena_none() -> None:
    """Test decode_vegetation_phenomena returns Nones for None input."""
    assert decode_vegetation_phenomena(None) == (None, None, None)


@pytest.mark.parametrize("invalid_value", ["4", "9", "104", "410", "999", "abc", ""])
def test_decode_vegetation_phenomena_invalid(invalid_value: str) -> None:
    """Test decode_vegetation_phenomena returns Nones for invalid values."""
    assert decode_vegetation_phenomena(invalid_value) == (None, None, None)


@pytest.mark.asyncio
async def test_vegetation_phenomena_current(
    hydrological_stations: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
    hydrological_alerts: list[dict[str, Any]],
) -> None:
    """Test vegetation phenomena when measurement is current."""
    session = aiohttp.ClientSession()

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                payload=hydrological_details,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
            result = await imgwpib.get_hydrological_data()

    await session.close()

    assert result.submerged_vegetation_cover.value == 33.0
    assert result.floating_vegetation_cover.value == 67.0
    assert result.emergent_vegetation_cover.value == 100.0
    assert str(result.vegetation_phenomena_measurement_date) == (
        "2024-04-21 09:07:00+02:00"
    )


@pytest.mark.asyncio
async def test_vegetation_phenomena_not_current(
    hydrological_stations: list[dict[str, Any]],
    hydrological_details: dict[str, Any],
    hydrological_alerts: list[dict[str, Any]],
) -> None:
    """Test vegetation phenomena when measurement is outdated."""
    session = aiohttp.ClientSession()

    hydrological_stations[5][ApiNames.VEGETATION_PHENOMENA] = "333"
    hydrological_stations[5][ApiNames.VEGETATION_PHENOMENA_MEASUREMENT_DATE] = (
        "2020-01-01 00:00:00"
    )

    with freeze_time(TEST_TIME):
        async with aiointercept(mock_external_urls=True) as session_mock:
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(API_HYDROLOGICAL_ENDPOINT, payload=hydrological_stations)
            session_mock.get(
                API_HYDROLOGICAL_DETAILS_ENDPOINT.with_query(id="154190050"),
                payload=hydrological_details,
            )
            session_mock.get(
                API_HYDROLOGICAL_WARNINGS_ENDPOINT, payload=hydrological_alerts
            )

            imgwpib = await ImgwPib.create(session, hydrological_station_id="154190050")
            result = await imgwpib.get_hydrological_data()

    await session.close()

    assert result.submerged_vegetation_cover.value is None
    assert result.floating_vegetation_cover.value is None
    assert result.emergent_vegetation_cover.value is None
    assert result.vegetation_phenomena_measurement_date is None
