"""Example of usage IMGW-PIB."""

import asyncio
import logging

from aiohttp import ClientConnectorError, ClientSession

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
        except ClientConnectorError as error:
            print(f"ClientConnectorError: {error}")
        else:
            print(imgwpib.stations)
            print(weather_data)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
