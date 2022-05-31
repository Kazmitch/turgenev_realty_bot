import requests
import xmltodict
import asyncio
import aiohttp


async def get_xml(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            return data


async def check_offers(url: str, area: str, price: str):

    task = asyncio.create_task(get_xml(url))

    xml = await task
    data = xmltodict.parse(xml)

    good_offers = []

    for offer in data['realty-feed']['offer']:
        print(offer)
        if float(offer['area']['value']) >= float(area) and int(offer['price']['value']) >= int(price):
            good_offers.append(offer)

    return good_offers

asyncio.run(check_offers('https://beta.xml-108.ru/xml/f7c15110-b851-4aca-bd5a-1e6f15bce5ef.xml', '50', '135000000'))
