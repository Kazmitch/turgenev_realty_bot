import requests
import xmltodict
import asyncio
import aiohttp
from datetime import datetime


async def get_xml(url: str):
    """Получаем данные в формате xml."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            return data


async def get_max_floor_yan(xml: dict) -> int:
    max_floor = int(xml['realty-feed']['offer'][0]['floors-total'])
    return max_floor


async def get_offers_yan(url: str, area_data: str, price_data: str, year_data: str, rooms_data: str, floor_data: str):
    """Отбираем лоты по критериям."""
    xml = await get_xml(url)
    data = xmltodict.parse(xml)

    area = [int(n) for n in area_data.split(',')]
    price = [int(n) for n in price_data.split(',')]
    max_floor = await get_max_floor_yan(data)
    year_now = datetime.now().year

    good_offers = []

    for offer in data['realty-feed']['offer']:
        if float(area[0]) <= float(offer['area']['value']) < float(area[1]) and float(price[0]) <= float(offer['price']['value']) < float(price[1]):
            if year_data == 'hand_over' and int(offer['built-year']) < year_now:
                good_offers.append(offer)
            elif year_data == 'now_year' and int(offer['built-year']) <= year_now:
                good_offers.append(offer)
            elif year_data == '0' and int(offer['built-year']) > 2000:
                good_offers.append(offer)
            elif rooms_data == '1' and int(offer['rooms']) == 1:
                good_offers.append(offer)
            elif rooms_data == '2' and int(offer['rooms']) == 2:
                good_offers.append(offer)
            elif rooms_data == '3' and int(offer['rooms']) >= 3:
                good_offers.append(offer)
            elif rooms_data == '0' and int(offer['rooms']) >= 1:
                good_offers.append(offer)
            elif floor_data == 'non_first' and int(offer['floor']) > 1:
                good_offers.append(offer)
            elif floor_data == 'non_last' and int(offer['floor']) < max_floor:
                good_offers.append(offer)
            elif floor_data == '0' and int(offer['floor']) >= 1:
                good_offers.append(offer)
    return good_offers
