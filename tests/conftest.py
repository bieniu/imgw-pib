"""Set up some common test helper things."""

import json
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Self, cast

import pytest
from freezegun import freeze_time
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.location import PyTestLocation

TEST_TIME = datetime(2024, 4, 22, 11, 10, 32, tzinfo=UTC)


@pytest.fixture
def frozen_time() -> Iterator[None]:
    """Freeze time at a fixed point for deterministic tests."""
    with freeze_time(TEST_TIME):
        yield


@pytest.fixture
def weather_stations() -> list[dict[str, Any]]:
    """Return weather stations data from the fixture file."""
    with Path("tests/fixtures/weather_stations.json").open(encoding="utf-8") as file:
        return cast(list[dict[str, Any]], json.load(file))


@pytest.fixture
def weather_station() -> dict[str, Any]:
    """Return weather station data from the fixture file."""
    with Path("tests/fixtures/weather_station.json").open(encoding="utf-8") as file:
        return cast(dict[str, Any], json.load(file))


@pytest.fixture
def weather_alerts() -> list[dict[str, Any]]:
    """Return weather alert data from the fixture file."""
    with Path("tests/fixtures/weather_alerts.json").open(encoding="utf-8") as file:
        return cast(list[dict[str, Any]], json.load(file))


@pytest.fixture
def weather_station_proxy() -> dict[str, Any]:
    """Return proxy weather station data from the fixture file."""
    with Path("tests/fixtures/weather_station_proxy.json").open(
        encoding="utf-8"
    ) as file:
        return cast(dict[str, Any], json.load(file))


@pytest.fixture
def hydrological_stations() -> list[dict[str, Any]]:
    """Return hydrological stations data from the fixture file."""
    with Path("tests/fixtures/hydrological_stations.json").open(
        encoding="utf-8"
    ) as file:
        return cast(list[dict[str, Any]], json.load(file))


@pytest.fixture
def hydrological_details() -> dict[str, Any]:
    """Return hydrological details from the fixture file."""
    with Path("tests/fixtures/hydrological_details.json").open(
        encoding="utf-8"
    ) as file:
        return cast(dict[str, Any], json.load(file))


@pytest.fixture
def hydrological_alerts() -> list[dict[str, Any]]:
    """Return hydrological alert data from the fixture file."""
    with Path("tests/fixtures/hydrological_alerts.json").open(encoding="utf-8") as file:
        return cast(list[dict[str, Any]], json.load(file))


@pytest.fixture
def hydrological_station_no_location() -> list[dict[str, Any]]:
    """Return hydrological station data with no lat/lon/province."""
    with Path("tests/fixtures/hydrological_station_no_location.json").open(
        encoding="utf-8"
    ) as file:
        return cast(list[dict[str, Any]], json.load(file))


@pytest.fixture
def snapshot(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture."""
    return snapshot.use_extension(SnapshotExtension)


class SnapshotExtension(AmberSnapshotExtension):
    """Extension for Syrupy."""

    @classmethod
    def dirname(cls: Self, *, test_location: PyTestLocation) -> str:
        """Return the directory for the snapshot files."""
        test_dir = Path(test_location.filepath).parent
        return str(test_dir.joinpath("snapshots"))
