"""Check for new IMGW-PIB alerts not yet mapped in const.py."""

import json
import os
import sys
from http.client import HTTPSConnection
from pathlib import Path
from urllib.parse import urlparse

from imgw_pib.const import HYDROLOGICAL_ALERTS_MAP, WEATHER_ALERTS_MAP

HYDRO_URL = "https://danepubliczne.imgw.pl/api/data/warningshydro"
METEO_URL = "https://danepubliczne.imgw.pl/api/data/warningsmeteo"


def fetch_json(url: str) -> list | dict:
    """Fetch JSON from URL using only stdlib."""
    parsed = urlparse(url)
    if not parsed.hostname:
        msg = f"Invalid URL: {url}"
        raise ValueError(msg)
    conn = HTTPSConnection(parsed.hostname, timeout=10)
    conn.request("GET", parsed.path, headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return json.loads(data)


def get_hydro_alerts() -> set[str]:
    """Get unique hydrological alert names from API."""
    response = fetch_json(HYDRO_URL)
    alerts: set[str] = set()
    if isinstance(response, dict) and response.get("status") is False:
        return alerts
    for alert in response:
        if isinstance(alert, dict) and (name := alert.get("zdarzenie")):
            alerts.add(name.lower())
    return alerts


def get_meteo_alerts() -> set[str]:
    """Get unique weather alert names from API."""
    response = fetch_json(METEO_URL)
    alerts: set[str] = set()
    if isinstance(response, dict) and response.get("status") is False:
        return alerts
    for alert in response:
        if isinstance(alert, dict) and (name := alert.get("nazwa_zdarzenia")):
            alerts.add(name.lower())
    return alerts


def main() -> None:
    """Check for new alerts and set GitHub Actions outputs."""
    print("Fetching hydrological alerts...")
    hydro_alerts = get_hydro_alerts()
    print(f"  Found: {hydro_alerts or '(none)'}")

    print("Fetching weather alerts...")
    meteo_alerts = get_meteo_alerts()
    print(f"  Found: {meteo_alerts or '(none)'}")

    known_hydro = {k.lower() for k in HYDROLOGICAL_ALERTS_MAP}
    known_meteo = {k.lower() for k in WEATHER_ALERTS_MAP}

    new_hydro = hydro_alerts - known_hydro
    new_meteo = meteo_alerts - known_meteo

    if new_hydro:
        print(f"New hydrological alerts: {new_hydro}")
    if new_meteo:
        print(f"New weather alerts: {new_meteo}")

    if not new_hydro and not new_meteo:
        print("No new alerts found.")
        return

    # Build issue body
    lines = [
        "New alerts detected from IMGW-PIB API"
        " that are not mapped in `imgw_pib/const.py`.\n"
    ]

    if new_hydro:
        lines.append("## New hydrological alerts (`HYDROLOGICAL_ALERTS_MAP`)\n")
        lines.extend(f"- `{alert}`" for alert in sorted(new_hydro))
        lines.append("")

    if new_meteo:
        lines.append("## New weather alerts (`WEATHER_ALERTS_MAP`)\n")
        lines.extend(f"- `{alert}`" for alert in sorted(new_meteo))
        lines.append("")

    body = "\n".join(lines)

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with Path(github_output).open("a") as f:
            f.write("new_alerts=true\n")
            # Use delimiter for multiline value
            f.write("issue_body<<EOF\n")
            f.write(body)
            f.write("\nEOF\n")
        print("GitHub Actions outputs set.")
    else:
        print("\nIssue body would be:")
        print(body)
        sys.exit(1)


if __name__ == "__main__":
    main()
