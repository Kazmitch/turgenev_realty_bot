from typing import List

from asgiref.sync import sync_to_async
from django.db.models import Q

from realty_bot.realty.models import Developer, Address, Building, XmlLink, SpecialOffer, Documentation, \
    AboutProjectPhoto, LocationPhoto, ProcessingCorpusPhoto, InteriorPhoto, ShowRoomPhoto


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
    description = Developer.objects.filter(buildings__latin_name=building_name).first().developer_description
    return description


@sync_to_async
def get_special_offers(building_name: str) -> List[SpecialOffer]:
    """Получаем список объектов SpecialOffer по названию ЖК."""
    offers = SpecialOffer.objects.filter(building__latin_name=building_name)
    return offers


@sync_to_async
def get_special_offer_description(offer_id: int) -> SpecialOffer:
    """Получаем объект SpecialOffer по его id."""
    special_offer = SpecialOffer.objects.get(id=offer_id)
    return special_offer


@sync_to_async
def get_documents(building_name: str) -> List[Documentation]:
    """Получаем список объектов Documentation по названию ЖК."""
    documents = Documentation.objects.filter(building__latin_name=building_name)
    return documents


@sync_to_async
def get_document_file(document_id: int) -> str:
    """Получаем путь документа по его id."""
    document_path = Documentation.objects.get(id=document_id).document
    return document_path


@sync_to_async
def get_about_project_photo(building_name: str) -> str:
    """Получаем путь фотографии О Проекте."""
    name = Developer.objects.filter(buildings__latin_name=building_name).first().latin_name
    path = AboutProjectPhoto.objects.filter(developer__latin_name=name).first().photo.name
    return path


@sync_to_async
def get_gallery_photos(section: str, building_name: str):
    """Получаем список фотографий нужной модели."""
    models_dict = {
        'location': LocationPhoto,
        'construction': ProcessingCorpusPhoto,
        'interior': InteriorPhoto,
        'showroom': ShowRoomPhoto
    }
    model = models_dict.get(section)
    photo_set = model.objects.filter(building__latin_name=building_name)
    return photo_set
