import aiohttp
import xmltodict

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


async def get_offers_yan(url: str, area: str, price: str, year: str, rooms: str):
    """Отбираем лоты по критериям."""
    xml = await get_xml(url)
    data = xmltodict.parse(xml)

    price = f'{price}000000'

    good_offers = []

    for offer in data['realty-feed']['offer']:
        if float(offer['area']['value']) >= float(area) and (
                float(offer['price']['value']) <= float(price) if price != '0000000' else float(
                    offer['price']['value']) >= float(price)):
            if year == '0' and int(offer['built-year']) > 0:
                good_offers.append(offer)
            elif year != '0' and int(offer['built-year']) <= int(year):
                good_offers.append(offer)
            elif rooms == '0' and int(offer['rooms']) >= 1:
                good_offers.append(offer)
            elif rooms != '0' and int(offer['rooms']) >= int(rooms):
                good_offers.append(offer)
    return good_offers


async def get_offers(building_name, data: dict = None, sort=None) -> list:
    """Получаем список предложений на основе данных."""
    # building_name = data.get('building_name')
    area = str(data.get('flat_area'))
    price = str(data.get('flat_price'))
    year = str(data.get('flat_year'))
    rooms = str(data.get('flat_rooms'))
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


async def get_max_and_low_values(offers: list = None, params: dict = None, building_name: str = None) -> dict:
    if params:
        offers = await get_offers(building_name, params)
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


async def get_all_offers(building_name: str):
    """Получаем значения всех возможных вариантов."""
    xml_link = await get_xml_link_by_name(building_name)
    xml = await get_xml(xml_link)
    data = xmltodict.parse(xml)
    offers = data['realty-feed']['offer']
    values = await get_max_and_low_values(offers)
    return values
