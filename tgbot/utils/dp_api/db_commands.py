from typing import List

from asgiref.sync import sync_to_async
from django.db.models import Q

from realty_bot.realty.models import Developer, Address, Building, XmlLink, SpecialOffer


@sync_to_async
def get_building(building_name: str) -> Building:
    """Получаем объект Building по аргументу из ссылки."""
    building = Building.objects.get(latin_name=building_name)
    return building


@sync_to_async
def get_find_building(building_name: str) -> Building:
    """Получаем объект Building по переданному запросу."""
    building = Building.objects.get(Q(name__icontains=building_name) | Q(building_description__icontains=building_name))
    return building


@sync_to_async
def get_xml_link_by_name(building_name: str) -> str:
    """Получаем ссылку на xml по имени."""
    xml_link = XmlLink.objects.filter(building__latin_name=building_name).first().xml_link
    return xml_link


@sync_to_async
def get_developer_description(building_name: str) -> str:
    """Получаем описание о застройщике по названию ЖК."""
    description = Developer.objects.filter(building__latin_name=building_name).first().developer_description
    return description


@sync_to_async
def get_special_offers(building_name: str) -> List[SpecialOffer]:
    """Получаем список спецпредложений по названию ЖК."""
    offers = SpecialOffer.objects.filter(building__latin_name=building_name)
    return offers


@sync_to_async
def get_special_offer_description(offer_id: int) -> str:
    """Получаем описание спецпредложения по его id."""
    description = SpecialOffer.objects.get(id=offer_id).description
    return description
