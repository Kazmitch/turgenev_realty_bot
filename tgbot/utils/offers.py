import aiohttp
import xmltodict

from tgbot.utils.dp_api.db_commands import get_xml_link_by_name


async def get_xml(url: str):
    """Получаем данные в формате xml."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            return data


async def get_photo_url(offer: dict, type_xml: str) -> str:
    """Получаем url фотографии."""
    if type_xml == 'yandex':
        photos = offer.get('image')
        if isinstance(photos, list):
            photo_url = photos[0].get('#text')
            return photo_url
        elif isinstance(photos, dict):
            photo_url = photos.get('#text')
            return photo_url
        elif isinstance(photos, str):
            return photos
    else:
        photo_url = offer.get('LayoutPhoto').get('FullUrl')
        return photo_url


async def get_values(offer: dict, type_xml: str) -> dict:
    """Получаем словарь со значениями."""
    if type_xml == 'yandex':
        values = {
            'offer_area': offer.get('area').get('value'),
            'offer_price': offer.get('price').get('value'),
            'offer_rooms': offer.get('rooms'),
            'offer_floor': offer.get('floor'),
        }
    else:
        values = {
            'offer_area': offer.get('TotalArea'),
            'offer_price': offer.get('BargainTerms').get('Price'),
            'offer_rooms': offer.get('FlatRoomsCount'),
            'offer_floor': offer.get('FloorNumber')
        }
    return values


async def get_max_floor_yan(xml: dict) -> int:
    """Получаем максимальный этаж ЖК из фида."""
    max_floor = int(xml['realty-feed']['offer'][0]['floors-total'])
    return max_floor


async def get_offers_yan(url: str, area: str, price: str, year: str, rooms: str):
    """Отбираем лоты по критериям из фида Яндекс."""
    xml = await get_xml(url)
    data = xmltodict.parse(xml)

    price = f'{price}000000'

    good_offers = []

    for offer in data['realty-feed']['offer']:
        if float(offer['area']['value'].replace(',', '.')) >= float(area) and (
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


async def get_offers_cian(url: str, area: str, price: str, year: str, rooms: str):
    """Отбираем лоты по критериям из фида Cian."""
    xml = await get_xml(url)
    data = xmltodict.parse(xml)

    price = f'{price}000000'

    good_offers = []

    for offer in data['feed']['object']:
        if float(offer['TotalArea']) >= float(area) and (
                float(offer['BargainTerms']['Price']) <= float(price) if price != '0000000' else float(
                offer['BargainTerms']['Price']) >= float(price)):
            if year == '0' and int(offer['Building']['Deadline']['Year']) > 0:
                good_offers.append(offer)
            elif year != '0' and int(offer['Building']['Deadline']['Year']) <= int(year):
                good_offers.append(offer)
            elif rooms == '0' and int(offer['FlatRoomsCount']) >= 1:
                good_offers.append(offer)
            elif rooms != '0' and int(offer['FlatRoomsCount']) >= int(rooms):
                good_offers.append(offer)
    return good_offers


async def sort_yan_offers(offers: list, type_sort: str):
    if type_sort == 'price_low_to_high':
        offers = sorted(offers, key=lambda d: float(d['price']['value']))
    if type_sort == 'price_high_to_low':
        offers = sorted(offers, key=lambda d: float(d['price']['value']), reverse=True)
    if type_sort == 'area_low_to_high':
        offers = sorted(offers, key=lambda d: float(d['area']['value']))
    if type_sort == 'area_high_to_low':
        offers = sorted(offers, key=lambda d: float(d['area']['value']), reverse=True)
    return offers


async def sort_cian_offers(offers: list, type_sort):
    if type_sort == 'price_low_to_high':
        offers = sorted(offers, key=lambda d: float(d['BargainTerms']['Price']))
    if type_sort == 'price_high_to_low':
        offers = sorted(offers, key=lambda d: float(d['BargainTerms']['Price']), reverse=True)
    if type_sort == 'area_low_to_high':
        offers = sorted(offers, key=lambda d: float(d['TotalArea']))
    if type_sort == 'area_high_to_low':
        offers = sorted(offers, key=lambda d: float(d['TotalArea']), reverse=True)
    return offers


async def get_offers(building_name, data: dict = None, sort=None) -> list:
    """Получаем список предложений на основе данных."""
    area = str(data.get('flat_area'))
    price = str(data.get('flat_price'))
    year = str(data.get('flat_year'))
    rooms = str(data.get('flat_rooms'))
    xml_link = await get_xml_link_by_name(building_name)
    if xml_link.type_of_xml == 'yandex':
        offers = await get_offers_yan(xml_link.xml_link, area, price, year, rooms)
        if sort is not None:
            offers = await sort_yan_offers(offers, sort)
        return offers
    elif xml_link.type_of_xml == 'cian':
        offers = await get_offers_cian(xml_link.xml_link, area, price, year, rooms)
        if sort is not None:
            offers = await sort_cian_offers(offers, sort)
        return offers


async def get_max_and_low_values_yan(offers: list = None, params: dict = None, building_name: str = None) -> dict:
    if params:
        offers = await get_offers(building_name, params)
    max_price_offer = max(offers, key=lambda d: float(d['price']['value']))
    low_price_offer = min(offers, key=lambda d: float(d['price']['value']))
    max_area_offer = max(offers, key=lambda d: float(d['area']['value'].replace(',', '.')))
    low_area_offer = min(offers, key=lambda d: float(d['area']['value'].replace(',', '.')))
    values = {
        'max_price': max_price_offer['price']['value'],
        'low_price': low_price_offer['price']['value'],
        'max_area': max_area_offer['area']['value'].replace(',', '.'),
        'low_area': low_area_offer['area']['value'].replace(',', '.'),
    }
    return values


async def get_max_and_low_values_cian(offers: list = None, params: dict = None, building_name: str = None) -> dict:
    if params:
        offers = await get_offers(building_name, params)
    max_price_offer = max(offers, key=lambda d: float(d['BargainTerms']['Price']))
    low_price_offer = min(offers, key=lambda d: float(d['BargainTerms']['Price']))
    max_area_offer = max(offers, key=lambda d: float(d['TotalArea']))
    low_area_offer = min(offers, key=lambda d: float(d['TotalArea']))
    values = {
        'max_price': max_price_offer['BargainTerms']['Price'],
        'low_price': low_price_offer['BargainTerms']['Price'],
        'max_area': max_area_offer['TotalArea'],
        'low_area': low_area_offer['TotalArea'],
    }
    return values


async def get_all_offers(building_name: str, params: dict = None):
    """Получаем значения всех возможных вариантов."""
    xml_link = await get_xml_link_by_name(building_name)
    xml = await get_xml(xml_link.xml_link)
    data = xmltodict.parse(xml)
    if xml_link.type_of_xml == 'yandex':
        offers = data['realty-feed']['offer']
        values = await get_max_and_low_values_yan(offers, params, building_name)
        return values
    elif xml_link.type_of_xml == 'cian':
        offers = data['feed']['object']
        values = await get_max_and_low_values_cian(offers, params, building_name)
        return values
