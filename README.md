[![GitHub Release][releases-shield]][releases]
[![PyPI][pypi-releases-shield]][pypi-releases]
[![PyPI - Downloads][pypi-downloads]][pypi-statistics]
[![Buy me a coffee][buy-me-a-coffee-shield]][buy-me-a-coffee]
[![PayPal_Me][paypal-me-shield]][paypal-me]
[![Revolut.Me][revolut-me-shield]][revolut-me]

# imgw-pib

Python async wrapper for IMGW-PIB API.

## Installation

You can install the library with pip:

```
pip install imgw-pib
```

## How to use the library

```python
"""Example of usage IMGW-PIB."""

import asyncio
import logging

from aiohttp import ClientError, ClientSession

from imgw_pib import ApiError, ImgwPib

logging.basicConfig(level=logging.DEBUG)

WEATHER_STATION_ID = "12200"
HYDROLOGICAL_STATION_ID = "154190050"


async def main() -> None:
    """Run main function."""
    async with ClientSession() as websession:
        try:
            imgwpib = await ImgwPib.create(
                websession,
                weather_station_id=WEATHER_STATION_ID,
                hydrological_station_id=HYDROLOGICAL_STATION_ID,
            )
            weather_data = await imgwpib.get_weather_data()
            hydrological_data = await imgwpib.get_hydrological_data()
        except ApiError as error:
            print(f"API Error: {error.status}")
        except ClientError as error:
            print(f"ClientError: {error}")
        except TimeoutError as error:
            print(f"TimeoutError: {error}")
        else:
            print(f"Weather stations: {imgwpib.weather_stations}")
            print(f"Weather data: {weather_data}")
            print(f"Hydrological stations: {imgwpib.hydrological_stations}")
            print(f"Hydrological data: {hydrological_data}")


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
```

## Error handling

The library raises `ApiError` when the IMGW-PIB API returns an error, `ClientError` for network-related errors, and `TimeoutError` when a request times out.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

[releases]: https://github.com/bieniu/imgw-pib/releases
[releases-shield]: https://img.shields.io/github/release/bieniu/imgw-pib.svg?style=popout
[pypi-releases]: https://pypi.org/project/imgw-pib/
[pypi-statistics]: https://pepy.tech/project/imgw-pib
[pypi-releases-shield]: https://img.shields.io/pypi/v/imgw-pib
[pypi-downloads]: https://pepy.tech/badge/imgw-pib/month
[buy-me-a-coffee-shield]: https://img.shields.io/static/v1.svg?label=%20&message=Buy%20me%20a%20coffee&color=6f4e37&logo=buy%20me%20a%20coffee&logoColor=white
[buy-me-a-coffee]: https://www.buymeacoffee.com/QnLdxeaqO
[paypal-me-shield]: https://img.shields.io/static/v1.svg?label=%20&message=PayPal.Me&logo=paypal
[paypal-me]: https://www.paypal.me/bieniu79
[revolut-me-shield]: https://img.shields.io/static/v1.svg?label=%20&message=Revolut&logo=revolut
[revolut-me]: https://revolut.me/maciejbieniek
