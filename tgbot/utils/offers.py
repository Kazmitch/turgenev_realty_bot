import aiohttp
import xmltodict

from tgbot.utils.dp_api.db_commands import get_xml_link_by_name


async def get_xml(url: str):
    """Получаем данные в формате xml."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            return data


async def get_photo_url(offer: dict, type_xml: str) -> list:
    """Получаем url фотографии."""
    if type_xml == 'yandex':
        photos = offer.get('image')
        if isinstance(photos, list):
            return photos
        elif isinstance(photos, dict):
            photo_url = photos.get('#text')
            return photo_url
        elif isinstance(photos, str):
            return [photos]
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
            'offer_section': offer.get('building-section'),
            'offer_type_of_flat': offer.get('custom-field').get('value')
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
    max_floor = int(xml.get('realty-feed').get('offer')[0].get('floors-total'))
    return max_floor


async def get_offers_yan(url: str, rooms: str):
    """Отбираем лоты по критериям из фида Яндекс."""
    xml = await get_xml(url)
    data = xmltodict.parse(xml)

    good_offers = []

    for offer in data.get('realty-feed').get('offer'):

        if rooms == 'studio':
            if offer.get('studio'):
                good_offers.append(offer)
                continue
            else:
                continue
        else:
            if offer.get('rooms'):
                if 3 <= int(offer.get('rooms')) <= 4 and int(rooms) == 3:
                    good_offers.append(offer)
                    continue
                elif int(offer.get('rooms')) == int(rooms):
                    good_offers.append(offer)
                    continue
                elif int(offer.get('rooms')) == 5 and int(rooms) == 5:
                    good_offers.append(offer)
                    continue
                else:
                    continue
            else:
                continue
    return good_offers


async def get_offers_cian(url: str, rooms: str):
    """Отбираем лоты по критериям из фида Cian."""
    xml = await get_xml(url)
    data = xmltodict.parse(xml)

    good_offers = []

    for offer in data.get('feed').get('object'):

        if rooms == 'studio':
            if int(offer.get('FlatRoomsCount')) == 9:
                good_offers.append(offer)
            else:
                continue
        else:
            if int(offer.get('FlatRoomsCount')) == int(rooms):
                good_offers.append(offer)
            else:
                continue
    return good_offers


async def sort_yan_offers(offers: list, type_sort: str):
    if type_sort == 'price_low_to_high':
        offers = sorted(offers, key=lambda d: float(d.get('price').get('value')))
    if type_sort == 'price_high_to_low':
        offers = sorted(offers, key=lambda d: float(d.get('price').get('value')), reverse=True)
    if type_sort == 'area_low_to_high':
        offers = sorted(offers, key=lambda d: float(d.get('area').get('value')))
    if type_sort == 'area_high_to_low':
        offers = sorted(offers, key=lambda d: float(d.get('area').get('value')), reverse=True)
    return offers


async def sort_cian_offers(offers: list, type_sort):
    if type_sort == 'price_low_to_high':
        offers = sorted(offers, key=lambda d: float(d.get('BargainTerms').get('Price')))
    if type_sort == 'price_high_to_low':
        offers = sorted(offers, key=lambda d: float(d.get('BargainTerms').get('Price')), reverse=True)
    if type_sort == 'area_low_to_high':
        offers = sorted(offers, key=lambda d: float(d.get('TotalArea')))
    if type_sort == 'area_high_to_low':
        offers = sorted(offers, key=lambda d: float(d.get('TotalArea')), reverse=True)
    return offers


async def get_offers(building_name, rooms: str, sort: str) -> list:
    """Получаем список предложений на основе данных."""
    xml_link = await get_xml_link_by_name(building_name)
    if xml_link.type_of_xml == 'yandex':
        offers = await get_offers_yan(xml_link.xml_link, rooms)
        if sort is not None:
            offers = await sort_yan_offers(offers, sort)
        return offers
    elif xml_link.type_of_xml == 'cian':
        offers = await get_offers_cian(xml_link.xml_link, rooms)
        if sort is not None:
            offers = await sort_cian_offers(offers, sort)
        return offers


async def get_max_and_low_values_yan(offers: list = None, params: dict = None, building_name: str = None) -> dict:
    if params:
        offers = await get_offers(building_name, params)
    # max_price_offer = max(offers, key=lambda d: float(d.get('price').get('value')))
    # low_price_offer = min(offers, key=lambda d: float(d.get('price').get('value')))
    max_area_offer = max(offers, key=lambda d: float(d.get('area').get('value').replace(',', '.')))
    low_area_offer = min(offers, key=lambda d: float(d.get('area').get('value').replace(',', '.')))
    values = {
        # 'max_price': max_price_offer.get('price').get('value'),
        # 'low_price': low_price_offer.get('price').get('value'),
        'max_area': max_area_offer.get('area').get('value').replace(',', '.'),
        'low_area': low_area_offer.get('area').get('value').replace(',', '.'),
    }
    return values


async def get_max_and_low_values_cian(offers: list = None, params: dict = None, building_name: str = None, xml_id: int = None) -> dict:
    if params:
        offers = await get_offers(building_name, params)
    max_price_offer = max(offers, key=lambda d: float(d.get('BargainTerms').get('Price')))
    low_price_offer = min(offers, key=lambda d: float(d.get('BargainTerms').get('Price')))
    max_area_offer = max(offers, key=lambda d: float(d.get('TotalArea').replace(',', '.')))
    low_area_offer = min(offers, key=lambda d: float(d.get('TotalArea').replace(',', '.')))
    values = {
        'max_price': max_price_offer.get('BargainTerms').get('Price'),
        'low_price': low_price_offer.get('BargainTerms').get('Price'),
        'max_area': max_area_offer.get('TotalArea').replace(',', '.'),
        'low_area': low_area_offer.get('TotalArea').replace(',', '.'),
    }
    return values


async def get_all_offers(building_name: str, params: dict = None):
    """Получаем значения всех возможных вариантов."""
    xml_link = await get_xml_link_by_name(building_name)
    xml = await get_xml(xml_link.xml_link)
    data = xmltodict.parse(xml)
    if xml_link.type_of_xml == 'yandex':
        offers = data.get('realty-feed').get('offer')
        values = await get_max_and_low_values_yan(offers, params, building_name)
        return values
    elif xml_link.type_of_xml == 'cian':
        offers = data.get('feed').get('object')
        values = await get_max_and_low_values_cian(offers, params, building_name)
        return values
