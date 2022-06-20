from typing import List

from asgiref.sync import sync_to_async
from django.db.models import Q, QuerySet

from realty_bot.realty.models import Developer, Address, Building, XmlLink, SpecialOffer, Documentation, \
    AboutProjectPhoto, LocationPhoto, ProcessingCorpusPhoto, InteriorPhoto, ShowRoomPhoto, Bank, Term, Benefit


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
def get_special_offers(building_name: str) -> QuerySet[SpecialOffer]:
    """Получаем query set объектов SpecialOffer по названию ЖК."""
    offers = SpecialOffer.objects.filter(building__latin_name=building_name)
    return offers


@sync_to_async
def get_special_offer_description(offer_id: int) -> SpecialOffer:
    """Получаем объект SpecialOffer по его id."""
    special_offer = SpecialOffer.objects.get(id=offer_id)
    return special_offer


@sync_to_async
def get_documents(building_name: str) -> QuerySet[Documentation]:
    """Получаем query set объектов Documentation по названию ЖК."""
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


@sync_to_async
def get_banks(building_name: str) -> QuerySet[Bank]:
    """Получаем query set объектов Bank по названию ЖК."""
    banks = Bank.objects.filter(developer__buildings__latin_name=building_name)
    return banks


@sync_to_async
def get_bank_terms(building_name: str, bank_id: int) -> QuerySet[Term]:
    """Получаем query set объектов Term по названию ЖК и id банка."""
    terms = Term.objects.filter(developer__buildings__latin_name=building_name, bank_id=bank_id)
    return terms


@sync_to_async
def get_current_term(building_name: str, bank_id: int, term_id: int) -> Term:
    """Получаем конкретное условие банка."""
    term = Term.objects.filter(developer__buildings__latin_name=building_name, bank_id=bank_id, id=term_id).first()
    return term


@sync_to_async
def get_installments(building_name: str) -> QuerySet[Term]:
    """Получаем query set условий ЖК только с рассрочкой."""
    installment = Term.objects.filter(developer__buildings__latin_name=building_name, installment_term=True)
    return installment


@sync_to_async
def get_installment_term(building_name: str, installment_id: int) -> Term:
    """Получаем объект Term по названию ЖК и id."""
    terms = Term.objects.filter(developer__buildings__latin_name=building_name, installment_term=True, id=installment_id).first()
    return terms


@sync_to_async
def get_it_mortgage(building_name: str) -> Term:
    """Получаем query set условия ЖК только с it-ипотекой."""
    it_term = Term.objects.filter(developer__buildings__latin_name=building_name, it_term=True).first()
    return it_term


@sync_to_async
def get_benefits(building_name: str) -> QuerySet[Term]:
    """Получаем query set льгот ЖК."""
    conditions = Benefit.objects.filter(developer__buildings__latin_name=building_name)
    return conditions


@sync_to_async
def get_benefit_terms(building_name: str, benefit_id: int) -> QuerySet[Term]:
    """Получаем query set условий льгот по ЖК id и id условия."""
    condition_terms = Term.objects.filter(developer__buildings__latin_name=building_name, benefit_id=benefit_id)
    return condition_terms


@sync_to_async
def get_current_benefit_term(building_name: str, benefit_id: int, term_id: int) -> Term:
    """Получаем конкретное условие льготы."""
    condition_term = Term.objects.filter(developer__buildings__latin_name=building_name, benefit_id=benefit_id, id=term_id).first()
    return condition_term
