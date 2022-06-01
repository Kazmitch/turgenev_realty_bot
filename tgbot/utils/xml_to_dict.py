import requests
import xmltodict
import asyncio
import aiohttp


async def get_xml(url: str):
    """Получаем данные в формате xml."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            return data


async def get_offers_yan(url: str, area: str, price: str):
    """Отбираем лоты по критериям."""
    xml = await get_xml(url)
    data = xmltodict.parse(xml)

    good_offers = []

    for offer in data['realty-feed']['offer']:
        print(offer)
        if float(offer['area']['value']) >= float(area) and int(offer['price']['value']) >= int(price):
            good_offers.append(offer)

    return good_offers
