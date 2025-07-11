"""Set up some common test helper things."""

import json
from pathlib import Path
from typing import Any, Self, cast

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.location import PyTestLocation


@pytest.fixture
def weather_stations() -> list[dict[str, Any]]:
    """Return weather stations data from the fixture file."""
    with Path.open("tests/fixtures/weather_stations.json", encoding="utf-8") as file:
        return cast(list[dict[str, Any]], json.load(file))


@pytest.fixture
def weather_station() -> dict[str, Any]:
    """Return weather station data from the fixture file."""
    with Path.open("tests/fixtures/weather_station.json", encoding="utf-8") as file:
        return cast(dict[str, Any], json.load(file))


@pytest.fixture
def weather_alerts() -> list[dict[str, Any]]:
    """Return weather alert data from the fixture file."""
    with Path.open("tests/fixtures/weather_alerts.json", encoding="utf-8") as file:
        return cast(list[dict[str, Any]], json.load(file))


@pytest.fixture
def hydrological_stations() -> list[dict[str, Any]]:
    """Return hydrological stations data from the fixture file."""
    with Path.open(
        "tests/fixtures/hydrological_stations.json", encoding="utf-8"
    ) as file:
        return cast(list[dict[str, Any]], json.load(file))


@pytest.fixture
def hydrological_stations_2() -> list[dict[str, Any]]:
    """Return hydrological stations data from the fixture file."""
    with Path.open(
        "tests/fixtures/hydrological_stations_2.json", encoding="utf-8"
    ) as file:
        return cast(list[dict[str, Any]], json.load(file))


@pytest.fixture
def hydrological_details() -> dict[str, Any]:
    """Return hydrological details from the fixture file."""
    with Path.open(
        "tests/fixtures/hydrological_details.json", encoding="utf-8"
    ) as file:
        return cast(dict[str, Any], json.load(file))


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
