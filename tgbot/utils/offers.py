# import requests
import xmltodict
import asyncio
import aiohttp
from datetime import datetime

from tgbot.utils.dp_api.db_commands import get_xml_link_by_name


async def get_xml(url: str):
    """Получаем данные в формате xml."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            return data


async def get_max_floor_yan(xml: dict) -> int:
    """Получаем максимальный этаж ЖК из фида."""
    max_floor = int(xml['realty-feed']['offer'][0]['floors-total'])
    return max_floor


async def get_offers_yan(url: str, area_data: str, price_data: str, year_data: str, rooms_data: str):
    """Отбираем лоты по критериям."""
    xml = await get_xml(url)
    data = xmltodict.parse(xml)

    area = int(area_data)
    price = int(price_data)
    year_now = datetime.now().year

    good_offers = []

    for offer in data['realty-feed']['offer']:
        if float(offer['area']['value']) >= float(area) and float(offer['price']['value']) <= float(price):
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
    return good_offers


async def get_offers(data: dict, sort=None) -> list:
    """Получаем список предложений на основе данных."""
    building_name = data.get('building_name')
    area = data.get('area')
    price = data.get('price')
    year = data.get('year')
    rooms = data.get('rooms')
    xml_link = await get_xml_link_by_name(building_name)
    offers = await get_offers_yan(xml_link, area, price, year, rooms)
    if sort == 'price_low_to_high':
        offers = sorted(offers, key=lambda d: float(d['price']['value']))
    if sort == 'price_high_to_low':
        offers = sorted(offers, key=lambda d: float(d['price']['value']), reverse=True)
    if sort == 'area_low_to_high':
        offers = sorted(offers, key=lambda d: float(d['area']['value']))
    if sort == 'area_high_to_low':
        offers = sorted(offers, key=lambda d: float(d['area']['value']), reverse=True)
    return offers


async def get_max_and_low_values(data: dict) -> dict:
    offers = await get_offers(data)
    max_price_offer = max(offers, key=lambda d: float(d['price']['value']))
    low_price_offer = min(offers, key=lambda d: float(d['price']['value']))
    max_area_offer = max(offers, key=lambda d: float(d['area']['value']))
    low_area_offer = min(offers, key=lambda d: float(d['area']['value']))
    values = {
        'max_price': max_price_offer['price']['value'],
        'low_price': low_price_offer['price']['value'],
        'max_area': max_area_offer['area']['value'],
        'low_area': low_area_offer['area']['value'],
    }
    return values
