import operator
from typing import List

from aiogram.types import Message
from asgiref.sync import sync_to_async
from django.db.models import Q, QuerySet

from realty_bot.realty.models import Developer, Building, XmlLink, SpecialOffer, Documentation, \
    AboutProjectPhoto, LocationPhoto, ProcessingCorpusPhoto, InteriorPhoto, ShowRoomPhoto, Term, News, Construction, \
    UserBot, SalesDepartment, CallRequest, CallTrackingCampaign, CallTrackingCampaignCredentials, ProgressVideo, Corpus, \
    AnnouncementVideo, AboutProjectVideo, BusinessLifePhoto, PersonalOfferPhoto, AboutProjectPresentation, Mailing


@sync_to_async
def create_userbot(message: Message, building_name: str, calltracking, **kwargs):
    """Создаем пользователя в базе."""
    telegram_id = message.from_user.id
    telegram_username = message.from_user.username
    telegram_first_name = message.from_user.first_name
    telegram_last_name = message.from_user.last_name
    UserBot.objects.create(
        telegram_id=telegram_id,
        telegram_username=telegram_username,
        telegram_first_name=telegram_first_name,
        telegram_last_name=telegram_last_name,
        building_name=building_name,
        calltracking=calltracking,
        campaign_id=kwargs.get('c_id', None),
        site_id=kwargs.get('s_id', None)
    )


@sync_to_async
def get_userbot(telegram_id: str) -> UserBot:
    """Получаем объект UserBot по telegram_id."""
    user_bot = UserBot.objects.filter(telegram_id=telegram_id).order_by('-id').first()
    return user_bot


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
    xml_link = XmlLink.objects.filter(building__latin_name=building_name).first()
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
def get_corpuses(building_name: str) -> QuerySet[Corpus]:
    """Получаем query set объектов Corpus по названию ЖК."""
    corpuses = Corpus.objects.filter(building__latin_name=building_name)
    return corpuses


@sync_to_async
def get_document_file(document_id: int) -> str:
    """Получаем путь документа по его id."""
    document_path = Documentation.objects.get(id=document_id).document
    return document_path


@sync_to_async
def get_announcement(building_name: str) -> QuerySet[AnnouncementVideo]:
    """Получаем query set объекта AnnouncementVideo."""
    announcement = AnnouncementVideo.objects.filter(building__latin_name=building_name).first()
    return announcement


@sync_to_async
def get_business_life_photo(building_name: str):
    """Получаем объект BusinessLifePhoto."""
    photo = BusinessLifePhoto.objects.filter(building__latin_name=building_name).first()
    return photo


@sync_to_async
def get_personal_offer_photo(building_name: str):
    """Получить объект PersonalOfferPhoto."""
    photo = PersonalOfferPhoto.objects.filter(building__latin_name=building_name).first()
    return photo


@sync_to_async
def get_about_project_photos(building_name: str) -> QuerySet[AboutProjectPhoto]:
    """Получаем query set объекта AboutProjectPhoto."""
    photo = AboutProjectPhoto.objects.filter(building__latin_name=building_name).order_by('order')
    return photo


@sync_to_async
def get_about_project_presentations(building_name: str) -> QuerySet[AboutProjectPresentation]:
    presentations = AboutProjectPresentation.objects.filter(building__latin_name=building_name).order_by('order')
    return presentations


@sync_to_async
def get_presentation_file(presentation_id: int) -> str:
    """Получаем путь документа по его id."""
    presentation = AboutProjectPresentation.objects.filter(id=presentation_id).first()
    return presentation


@sync_to_async
def get_about_project_video(building_name: str) -> str:
    """Получаем объект AboutProjectVideo."""
    video = AboutProjectVideo.objects.filter(building__latin_name=building_name).first()
    return video


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
    photo_set = model.objects.filter(building__latin_name=building_name).order_by('order')
    return photo_set


@sync_to_async
def get_corpus_photos(building_name: str, corpus_id: int) -> QuerySet[ProcessingCorpusPhoto]:
    """Получаем query set объектов ProcessingCorpusPhoto по названию ЖК и id корпуса."""
    photo_set = ProcessingCorpusPhoto.objects.filter(building__latin_name=building_name, corpus=corpus_id).order_by(
        'order')
    return photo_set


@sync_to_async
def get_progress_video(building_name: str) -> ProgressVideo:
    """Получаем объект ProgressVideo по названию ЖК."""
    video_progress = ProgressVideo.objects.filter(building__latin_name=building_name).first()
    return video_progress


@sync_to_async
def get_term_photo(building_name: str) -> Corpus:
    """Получаем объект Corpus, в котором присутствует фотография."""
    term_photo = Term.objects.filter(building__latin_name=building_name, header_photo=True).first()
    return term_photo


@sync_to_async
def get_terms(building_name: str, term: str) -> List[Term]:
    """Получаем query set объектов Term по названию ЖК и условию."""
    order_date = Term.objects.filter(building__latin_name=building_name, type_of_term=term).order_by('-created_at')[:5]
    terms = sorted(order_date, key=operator.attrgetter('payment'))
    return terms


@sync_to_async
def get_news(building_name: str) -> QuerySet[News]:
    """Получаем query set объектов News по названию ЖК."""
    news = News.objects.filter(building__latin_name=building_name, is_active=True, is_published=True)
    return news


@sync_to_async
def get_construction_photos(building_name: str) -> QuerySet[Construction]:
    """Получаем query set объектов Construction по названию ЖК."""
    construct_photos = Construction.objects.filter(building__latin_name=building_name).order_by('-photo_date')
    return construct_photos


@sync_to_async
def get_sales_department(building_name: str) -> SalesDepartment:
    """Получаем объект SalesDepartment по названию ЖК."""
    sales_department = SalesDepartment.objects.filter(building__latin_name=building_name).first()
    return sales_department


@sync_to_async
def create_requests(building_name: str, telegram_user_id: int, phone_number: str, data: dict):
    """Записываем запрос на перезвон."""
    CallRequest.objects.create(
        developer=Developer.objects.get(buildings__latin_name=building_name),
        building=Building.objects.get(latin_name=building_name),
        telegram_user=UserBot.objects.filter(telegram_id=telegram_user_id).order_by('-id').first(),
        telegram_user_phone=phone_number,
        request_data=data
    )


@sync_to_async
def get_call_request(building_name: str, **kwargs) -> CallTrackingCampaign:
    """Получаем объект рекламной кампании."""
    call = CallTrackingCampaign.objects.filter(building__latin_name=building_name, site_id=kwargs.get('site_id'),
                                               campaign_id=kwargs.get('campaign_id')).first()
    return call


@sync_to_async
def get_start_campaign() -> CallTrackingCampaign:
    """Получаем объект рекламной кампании с органикой."""
    campaign = CallTrackingCampaign.objects.filter(start_button=True).first()
    return campaign


async def create_mailing(send_id: str, user_id: str, msg_id: str):
    """Сохраняем рассылку."""
    user = await UserBot.objects.filter(telegram_id=user_id).afirst()
    await Mailing.objects.acreate(
        mailing_id=send_id,
        user_bot=user,
        msg_id=msg_id
    )


@sync_to_async
def get_mailing(mailing_id: str):
    """Получаем объект рассылки."""
    mailing = list(Mailing.objects.prefetch_related('user_bot').filter(mailing_id=mailing_id))
    return mailing
