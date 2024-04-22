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
