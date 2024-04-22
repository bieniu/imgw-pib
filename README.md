[![GitHub Release][releases-shield]][releases]
[![PyPI][pypi-releases-shield]][pypi-releases]
[![PyPI - Downloads][pypi-downloads]][pypi-statistics]
[![PayPal_Me][paypal-me-shield]][paypal-me]

# imgw-pib

Python async wrapper for IMGW-PIB API.


## How to use package

```python
"""Example of usage IMGW-PIB."""

import asyncio
import logging

from aiohttp import ClientError, ClientSession

from imgw_pib import ApiError, ImgwPib

logging.basicConfig(level=logging.DEBUG)

WEATHER_STATION_ID = "12200"


async def main() -> None:
    """Run main function."""
    async with ClientSession() as websession:
        try:
            imgwpib = await ImgwPib.create(websession, WEATHER_STATION_ID)
            weather_data = await imgwpib.get_weather_data()
        except ApiError as error:
            print(f"API Error: {error.status}")
        except ClientError as error:
            print(f"ClientError: {error}")
        except TimeoutError as error:
            print(f"TimeoutError: {error}")
        else:
            print(imgwpib.weather_stations)
            print(weather_data)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()

```

[releases]: https://github.com/bieniu/imgw-pib/releases
[releases-shield]: https://img.shields.io/github/release/bieniu/imgw-pib.svg?style=popout
[pypi-releases]: https://pypi.org/project/imgw-pib/
[pypi-statistics]: https://pepy.tech/project/imgw-pib
[pypi-releases-shield]: https://img.shields.io/pypi/v/imgw-pib
[pypi-downloads]: https://pepy.tech/badge/imgw-pib/month
[paypal-me-shield]: https://img.shields.io/static/v1.svg?label=%20&message=PayPal.Me&logo=paypal
[paypal-me]: https://www.paypal.me/bieniu79
