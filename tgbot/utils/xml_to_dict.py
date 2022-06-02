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


async def get_offers_yan(url: str, area_data: str, price_data: str, year_data: str):
    """Отбираем лоты по критериям."""
    xml = await get_xml(url)
    data = xmltodict.parse(xml)

    area = [int(n) for n in area_data.split(',')]
    price = [int(n) for n in price_data.split(',')]
    max_floor = await get_max_floor_yan(data)
    year_now = datetime.now().year

    if year_data == 'hand_over':
        year_query = f'< {year_now}'
    if year_data == 'now_year':
        year_query = f'== {year_now}'
    if year_data == '0':
        year_query = f'> {year_now}'

    good_offers = []

    for offer in data['realty-feed']['offer']:
        if float(area[0]) <= float(offer['area']['value']) < float(area[1]) and float(price[0]) <= float(offer['price']['value']) < float(price[1]):
            good_offers.append(offer)

    return good_offers
