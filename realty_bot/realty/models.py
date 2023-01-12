from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.html import format_html

from environs import Env

from realty_bot.realty_bot.utils import user_directory_path, about_project_path, encode_decode_values

env = Env()
env.read_env()


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    class Meta:
        abstract = True


class BasePublication(BaseModel):
    is_published = models.BooleanField(verbose_name="Опубликовано")
    is_active = models.BooleanField(verbose_name="Активно")
    publicate_at = models.DateField(verbose_name="Опубликовать", blank=True, null=True)
    published_at = models.DateField(verbose_name="Опубликовано", blank=True, null=True)

    class Meta:
        abstract = True


class UserBot(BaseModel):
    telegram_id = models.BigIntegerField(verbose_name="ID Пользователя Телеграм", blank=True, null=True)
    telegram_username = models.CharField(verbose_name="Username Телеграм", max_length=32, blank=True, null=True)
    telegram_first_name = models.CharField(verbose_name="Имя пользователя", max_length=64, blank=True, null=True)
    telegram_last_name = models.CharField(verbose_name="Фамилия пользователя", max_length=64, blank=True, null=True)
    is_admin = models.BooleanField(verbose_name="Администратор", default=False)
    building_name = models.CharField(verbose_name="Название ЖК", max_length=64, blank=True, null=True)
    calltracking = models.CharField(verbose_name="Название коллтрекинга", max_length=32, blank=True, null=True)
    campaign_id = models.CharField(verbose_name="ID рекламной кампании", max_length=16, blank=True, null=True)
    site_id = models.CharField(verbose_name="ID сайта", max_length=16, blank=True, null=True)

    @property
    def get_calltracking(self):
        return self.calltracking

    @property
    def get_source_id(self):
        if self.site_id and self.campaign_id:
            return {'campaign_id': self.campaign_id, 'site_id': self.site_id}
        else:
            if self.campaign_id:
                return {'campaign_id': self.campaign_id}
            else:
                return {'site_id': self.site_id}

    @property
    def get_source(self):
        return "campaign_id" if self.campaign_id else "site_id"

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"

    def __str__(self):
        return f"{self.telegram_id}"


class Developer(BaseModel):
    developer_name = models.CharField(verbose_name="Название застройщика", max_length=255)
    latin_name = models.CharField(verbose_name="Название на английском", max_length=255, unique=True, null=True,
                                  help_text='В формате <b>some_developer_name</b>')
    developer_description = models.TextField(verbose_name="Описание застройщика", blank=True,
                                             help_text='Не больше 1024 символов')

    class Meta:
        verbose_name = "Застройщик"
        verbose_name_plural = "Застройщики"

    def __str__(self):
        return f"{self.developer_name}"


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    developer = models.ForeignKey(
        Developer,
        related_name='profiles',
        verbose_name='Застройщик',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Address(BaseModel):
    country = models.CharField(verbose_name="Страна", max_length=32, blank=True)
    region = models.CharField(verbose_name="Название субъекта РФ", max_length=64, blank=True)
    city = models.CharField(verbose_name="Название района субъекта РФ (город)", max_length=64, blank=True)
    street = models.CharField(verbose_name="Улица", max_length=64, blank=True)
    house = models.CharField(verbose_name="Номер дома", max_length=32, blank=True)
    corpus = models.CharField(verbose_name="Корпус дома", max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return f"{self.city} {self.street} {self.house}"


class Building(BaseModel):
    name = models.CharField(verbose_name="Название ЖК", max_length=255, unique=True)
    latin_name = models.CharField(verbose_name="Название на английском", max_length=40, unique=True, null=True,
                                  help_text='В формате <b>some_building_name</b>\n<b>Не больше 40 символов</b>')
    address = models.OneToOneField(Address, verbose_name="Адрес", on_delete=models.CASCADE, null=True)
    developer = models.ForeignKey(Developer, verbose_name="Застройщик", related_name="buildings",
                                  on_delete=models.CASCADE, null=True)
    greeting = models.TextField(verbose_name="Фраза приветствия")
    building_description = models.TextField(verbose_name="Описание ЖК", blank=True)
    floors_total = models.CharField(verbose_name="Количество этажей", max_length=32)
    built_year = models.DateField(verbose_name="Год сдачи (год постройки)")
    ready_quarter = models.CharField(verbose_name="Квартал сдачи дома", max_length=32, blank=True)
    building_type = models.CharField(verbose_name="Тип дома", max_length=32, blank=True)
    building_section = models.CharField(verbose_name="Корпус дома", max_length=32, blank=True, null=True)
    ceiling_height = models.CharField(verbose_name="Высота потолков в метрах", max_length=32, blank=True)
    lift = models.BooleanField(verbose_name="Наличие лифта", blank=True)
    guarded_building = models.BooleanField(verbose_name="Закрытая территория", blank=True)
    parking = models.BooleanField(verbose_name="Наличие парковки", blank=True)

    class Meta:
        verbose_name = "Жилой комплекс"
        verbose_name_plural = "Жилые комплексы"

    def __str__(self):
        return f"{self.name}"


class Flat(BaseModel):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name="flats", null=True)
    flat_description = models.TextField(verbose_name="Описание квартиры", blank=True)
    floor = models.CharField(verbose_name="Этаж", max_length=32, null=True)
    rooms = models.CharField(verbose_name="Количество комнат", max_length=32, blank=True)
    studio = models.BooleanField(verbose_name="Студия", blank=True, null=True)
    total_area = models.CharField(verbose_name="Общая площадь", max_length=32, null=True)
    living_area = models.CharField(verbose_name="Жилая площадь", max_length=32, blank=True)
    kitchen_area = models.CharField(verbose_name="Площадь кухни", max_length=32, blank=True)
    bath_area = models.CharField(verbose_name="Площадь санузла", max_length=32, blank=True)
    price = models.CharField(verbose_name="Стоимость квартиры", max_length=32, null=True)

    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"

    def __str__(self):
        return f"{self.building.name} {self.total_area} {self.rooms} {self.price}"


class News(BasePublication):
    directory = 'photo/news'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс", related_name="news",
                                 null=True)
    title = models.CharField(verbose_name="Заголовок", max_length=255)
    text = models.TextField(verbose_name="Текст новости")
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='Фотография', blank=True, null=True)
    telegraph_url = models.CharField(verbose_name='Ссылка на Telegraph', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title}"

    @cached_property
    def display_image(self):
        html = '<a href="{img}"><img src="{img}" width="100" height="100"></a>'
        if self.photo:
            return format_html(html, img=self.photo.url)
        return format_html('<strong>There is no image for this entry.<strong>')

    display_image.short_description = 'Изображение'


class TypeOfXml(models.TextChoices):
    YANDEX = 'yandex', 'Яндекс'
    CIAN = 'cian', 'Cian'


class XmlLink(BaseModel):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name="xml_links", null=True)
    xml_link = models.CharField(verbose_name="Ссылка на xml", max_length=255)
    type_of_xml = models.CharField(verbose_name="Тип ссылка", max_length=16, choices=TypeOfXml.choices)

    class Meta:
        verbose_name = "XML Ссылка"
        verbose_name_plural = "XML Ссылки"

    def __str__(self):
        return f"{self.building.name} XML"


class Corpus(BaseModel):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name="corpuses", null=True)
    title = models.CharField(verbose_name="Название корпуса", max_length=32, null=True)

    class Meta:
        verbose_name = "Корпус"
        verbose_name_plural = "Корпуса"

    def __str__(self):
        return f"{self.title}"


class SpecialOffer(BaseModel):
    directory = 'photo/special_offer'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name="special_offers", null=True)
    title = models.CharField(verbose_name="Заголовок спецпредложения", max_length=255, null=True)
    description = models.TextField(verbose_name="Описание спецпредложения", null=True)
    photo = models.ImageField(upload_to=user_directory_path, verbose_name="Фотография")
    order = models.FloatField(verbose_name="Порядок", default=10)

    class Meta:
        verbose_name = "Спецпредложения"
        verbose_name_plural = "Спецпредложения"

    def __str__(self):
        return f"{self.title}"

    @cached_property
    def display_image(self):
        html = '<a href="{img}"><img src="{img}" width="100" height="100"></a>'
        if self.photo:
            return format_html(html, img=self.photo.url)
        return format_html('<strong>There is no image for this entry.<strong>')

    display_image.short_description = 'Изображение'


class AnnouncementVideo(BaseModel):
    directory = 'video/announcement'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='announcements')
    video = models.FileField(upload_to=user_directory_path, verbose_name='Видео')
    description = models.TextField(verbose_name="Описание видео", help_text="Не больше 1024 символов",
                                   max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = "Анонс"
        verbose_name_plural = "Анонсы"

    def __str__(self):
        return f"{self.building.name}"

    @cached_property
    def display_video(self):
        html = '<a href="{video}"><video src="{video}" width="320" height="240"></a>'
        if self.video:
            return format_html(html, video=self.video.url)
        return format_html('<strong>There is no video for this entry.<strong>')

    display_video.short_description = 'Видео'


class AboutProjectVideo(BaseModel):
    directory = 'video/about_project'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='about_project_videos')
    video = models.FileField(upload_to=user_directory_path, verbose_name='Видео')
    description = models.TextField(verbose_name="Описание видео", help_text="Не больше 1024 символов",
                                   max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = "О проекте Видео"
        verbose_name_plural = "О проекте Видео"

    def __str__(self):
        return f"{self.building.name}"

    @cached_property
    def display_video(self):
        html = '<a href="{video}"><video src="{video}" width="320" height="240"></a>'
        if self.video:
            return format_html(html, video=self.video.url)
        return format_html('<strong>There is no video for this entry.<strong>')

    display_video.short_description = 'Видео'


class BusinessLifePhoto(BaseModel):
    directory = 'photo/business_life'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='business_life_photos')
    photo = models.ImageField(upload_to=user_directory_path, verbose_name="Фотография")
    description = models.TextField(verbose_name="Описание фотографии", help_text="Не больше 1024 символов",
                                   max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = "Для бизнеса и жизни Фото"
        verbose_name_plural = "Для бизнеса и жизни Фото"

    def __str__(self):
        return f"{self.building.name}"

    @cached_property
    def display_image(self):
        html = '<a href="{img}"><img src="{img}" width="100" height="100"></a>'
        if self.photo:
            return format_html(html, img=self.photo.url)
        return format_html('<strong>There is no image for this entry.<strong>')

    display_image.short_description = 'Изображение'


class AboutProjectPhoto(BaseModel):
    directory = 'photo/about_project'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='about_project_photos')
    photo = models.ImageField(upload_to=user_directory_path, verbose_name="Фотография")
    order = models.FloatField(verbose_name="Порядок", default=10)
    description = models.TextField(verbose_name="Описание фотографии", help_text="Не больше 1024 символов",
                                   max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = "О проекте Фото"
        verbose_name_plural = "О проекте Фото"

    def __str__(self):
        return f"{self.building.name}"

    @cached_property
    def display_image(self):
        html = '<a href="{img}"><img src="{img}" width="100" height="100"></a>'
        if self.photo:
            return format_html(html, img=self.photo.url)
        return format_html('<strong>There is no image for this entry.<strong>')

    display_image.short_description = 'Изображение'


class LocationPhoto(BaseModel):
    directory = 'photo/location'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='locations')
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='Фотография')
    order = models.FloatField(verbose_name="Порядок", default=10)
    description = models.TextField(verbose_name="Описание фотографии", help_text="Не больше 1024 символов",
                                   max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = "Локация ЖК Фото"
        verbose_name_plural = "Локация ЖК Фото"

    def __str__(self):
        return f"{self.building.name}"

    @cached_property
    def display_image(self):
        html = '<a href="{img}"><img src="{img}" width="100" height="100"></a>'
        if self.photo:
            return format_html(html, img=self.photo.url)
        return format_html('<strong>There is no image for this entry.<strong>')

    display_image.short_description = 'Изображение'


class ProcessingCorpusPhoto(BaseModel):
    directory = 'photo/processing'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name="corps")
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, verbose_name="Корпус", related_name="corps", null=True)
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='Фотография')
    order = models.FloatField(verbose_name="Порядок", default=10)
    description = models.TextField(verbose_name="Описание фотографии", help_text="Не больше 1024 символов",
                                   max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = "Строящийся корпус Фото"
        verbose_name_plural = "Строящиеся корпуса Фото"

    def __str__(self):
        return f"{self.building.name}"

    @cached_property
    def display_image(self):
        html = '<a href="{img}"><img src="{img}" width="100" height="100"></a>'
        if self.photo:
            return format_html(html, img=self.photo.url)
        return format_html('<strong>There is no image for this entry.<strong>')

    display_image.short_description = 'Изображение'


class InteriorPhoto(BaseModel):
    directory = 'photo/interior'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='interiors')
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='Фотография')
    order = models.FloatField(verbose_name="Порядок", default=10)
    description = models.TextField(verbose_name="Описание фотографии", help_text="Не больше 1024 символов",
                                   max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = "Интерьер Фото"
        verbose_name_plural = "Интерьеры Фото"

    def __str__(self):
        return f"{self.building.name}"

    @cached_property
    def display_image(self):
        html = '<a href="{img}"><img src="{img}" width="100" height="100"></a>'
        if self.photo:
            return format_html(html, img=self.photo.url)
        return format_html('<strong>There is no image for this entry.<strong>')

    display_image.short_description = 'Изображение'


class ShowRoomPhoto(BaseModel):
    directory = 'photo/show_room'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='show_rooms')
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='Фотография')
    order = models.FloatField(verbose_name="Порядок", default=10)
    description = models.TextField(verbose_name="Описание фотографии", help_text="Не больше 1024 символов",
                                   max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = "Шоурум Фото"
        verbose_name_plural = "Шоурумы Фото"

    def __str__(self):
        return f"{self.building.name}"

    @cached_property
    def display_image(self):
        html = '<a href="{img}"><img src="{img}" width="100" height="100"></a>'
        if self.photo:
            return format_html(html, img=self.photo.url)
        return format_html('<strong>There is no image for this entry.<strong>')

    display_image.short_description = 'Изображение'


class ProgressVideo(BaseModel):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='progress_videos')
    video_url = models.CharField(verbose_name="Прямая ссылка на видео (youtube, vimeo)", max_length=255, blank=True,
                                 null=True)
    source_url = models.CharField(verbose_name="Ссылка на другой источник (telegra.ph)", max_length=255, blank=True,
                                  null=True)
    description = models.TextField(verbose_name="Описание видео", help_text="Не больше 1024 символов",
                                   max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = "Ход строительства"
        verbose_name_plural = "Ход строительства"

    def __str__(self):
        return f"{self.building.name}"

    @cached_property
    def display_video(self):
        html = '<iframe width="420" height="315" src="{video}"></iframe>'
        if self.video_url:
            return format_html(html, video=self.video_url)
        return format_html('<strong>There is no video for this entry.<strong>')

    display_video.short_description = 'Видео'


class Documentation(BaseModel):
    directory = 'documents/declaration'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='documentations')
    title = models.CharField(verbose_name="Название документа", max_length=255, null=True)
    document = models.FileField(upload_to=user_directory_path, verbose_name='Документ')

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документация"

    def __str__(self):
        return f"{self.title}"


class TypeOfTerm(models.TextChoices):
    BANK_OFFER = 'bank', 'Предложение от банка'
    INSTALLMENT = 'installment', 'Рассрочка'
    SPECIAL_MORTGAGE = 'conditions', 'Ипотека на специальных условиях'
    IT_MORTGAGE = 'it_mortgage', 'IT-ипотека'


class Bank(models.TextChoices):
    SBER = 'sber', 'Сбер'
    ALFA = 'alfa', 'Альфа Банк'
    RSHB = 'rshb', 'Россельхозбанк'
    GAZPROM = 'gazprom', 'Газпромбанк'
    VTB = 'vtb', 'Банк ВТБ'
    RAIFFEISEN = 'raiffeisen', 'Райффайзенбанк'
    ROSBANK = 'rosbank', 'Росбанк'


class Term(BaseModel):
    directory = 'photo/term'
    bank = models.CharField(verbose_name="Банк", max_length=64, choices=Bank.choices, null=True, blank=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, verbose_name="Застройщик", related_name="terms")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='terms')
    type_of_term = models.CharField(
        verbose_name="Тип условия",
        max_length=64,
        choices=TypeOfTerm.choices,
        default=TypeOfTerm.BANK_OFFER
    )
    payment = models.IntegerField(verbose_name="Ежемесячный платёж", blank=True, default=30000)
    title = models.CharField(verbose_name="Условие", max_length=255)
    description = models.TextField(verbose_name="Описание условия")
    document = models.FileField(upload_to=user_directory_path, verbose_name='Документ', blank=True)
    photo = models.ImageField(upload_to=user_directory_path, verbose_name="Фотография", blank=True, null=True)
    header_photo = models.BooleanField(verbose_name="Использовать для заголовка раздела", default=False)

    class Meta:
        verbose_name = "Условие"
        verbose_name_plural = "Условия"

    def __str__(self):
        return f"{self.title}"

    @cached_property
    def display_image(self):
        html = '<a href="{img}"><img src="{img}" width="100" height="100"></a>'
        if self.photo:
            return format_html(html, img=self.photo.url)
        return format_html('<strong>There is no image for this entry.<strong>')

    display_image.short_description = 'Изображение'


class Construction(BasePublication):
    directory = 'photo/construction'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='constructions')
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='Фотография')
    photo_date = models.DateField(verbose_name="Дата фотографии", help_text="К какой дате относится фотография")

    class Meta:
        verbose_name = "Динамика строительства Фото"
        verbose_name_plural = "Динамика строительства Фото"

    def __str__(self):
        return f"{self.building.name}"

    @cached_property
    def display_image(self):
        html = '<a href="{img}"><img src="{img}" width="100" height="100"></a>'
        if self.photo:
            return format_html(html, img=self.photo.url)
        return format_html('<strong>There is no image for this entry.<strong>')

    display_image.short_description = 'Изображение'


class SalesDepartment(BaseModel):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, verbose_name="Застройщик",
                                  related_name="sales_departments")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='sales_departments')
    description = models.TextField(verbose_name="Дни и время работы офиса продаж")

    class Meta:
        verbose_name = "Офис продаж"
        verbose_name_plural = "Офисы продаж"

    def __str__(self):
        return f"{self.building}"


class CallRequest(BaseModel):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, verbose_name="Застройщик",
                                  related_name="call_requests")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name="call_requests")
    telegram_user = models.ForeignKey(UserBot, on_delete=models.CASCADE, verbose_name="Пользователь",
                                      related_name="call_requests")
    telegram_user_phone = models.CharField(verbose_name="Телефон заявки", max_length=32)
    request_data = models.JSONField(verbose_name='Данные в JSON формате', blank=True, null=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.building.name}"


class CallTrackingCampaignCredentials(BaseModel):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, verbose_name="Застройщик",
                                  related_name="call_tracking_campaign_credentials")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name="call_tracking_campaign_credentials")
    access_token = models.CharField(verbose_name="API ключ", max_length=128, null=True)

    class Meta:
        verbose_name = "Креды"
        verbose_name_plural = "Креды"

    def __str__(self):
        return f"{self.building.name}, {self.access_token}"


class TypeOfCallTracking(models.TextChoices):
    COMAGIC = 'comagic', 'Comagic'
    CALLTOUCH = 'calltouch', 'Calltouch'
    SCB = 'smart_call_back', 'SmartCallBack'


class CallTrackingCampaign(BaseModel):
    campaign_name = models.CharField(verbose_name="Название рекламной кампании", max_length=255)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, verbose_name="Застройщик",
                                  related_name="call_tracking_campaigns")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name="call_tracking_campaigns")
    call_tracking_name = models.CharField(verbose_name="Название коллтрекинга", max_length=32,
                                          choices=TypeOfCallTracking.choices, default=TypeOfCallTracking.COMAGIC)
    api_token = models.ForeignKey(CallTrackingCampaignCredentials, verbose_name="API ключ", on_delete=models.CASCADE,
                                  related_name="call_tracking_campaigns", null=True)
    campaign_id = models.CharField(verbose_name="ID рекламной кампании", max_length=32, blank=True, null=True)
    site_id = models.CharField(verbose_name="ID сайта", max_length=32, blank=True, null=True)
    route_key = models.CharField(verbose_name="Ключ виджета 'Форма на сайте'", max_length=32, blank=True, null=True,
                                 help_text="Используется для обратного перезвона в Calltouch")
    phone_number = models.CharField(verbose_name="Подменный номер", max_length=32, blank=True,
                                    null=True, help_text="Пример: +79095432100")
    start_button = models.BooleanField(verbose_name="Прямой заход в бота", default=False)

    class Meta:
        verbose_name = "Рекламная кампания"
        verbose_name_plural = "Рекламные кампании"

    def __str__(self):
        return f"{self.building.name}"

    def save(self, *args, **kwargs):
        if self.start_button:
            CallTrackingCampaign.objects.update(start_button=False)
        super().save(*args, **kwargs)

    @property
    def get_source_id(self):
        if self.site_id and self.campaign_id:
            return {'c_id': self.campaign_id, 's_id': self.site_id}
        else:
            if self.campaign_id:
                return {'c_id': self.campaign_id}
            else:
                return {'s_id': self.site_id}

    @property
    def url_base64_encode(self, **kwargs):
        if self.building.latin_name and (self.campaign_id and self.site_id):
            encoded_url = encode_decode_values(f'{self.building.latin_name}&ct={self.call_tracking_name}&s_id={self.site_id}&c_id={self.campaign_id}')
            return f'https://t.me/{env.str("BOT_NAME")}?start={encoded_url}'
        elif self.building.latin_name and (self.campaign_id or self.site_id):
            if self.campaign_id:
                encoded_url = encode_decode_values(f'{self.building.latin_name}&ct={self.call_tracking_name}&c_id={self.campaign_id}')
                return f'https://t.me/{env.str("BOT_NAME")}?start={encoded_url}'
            elif self.site_id:
                encoded_url = encode_decode_values(f'{self.building.latin_name}&ct={self.call_tracking_name}&s_id={self.site_id}')
                return f'https://t.me/{env.str("BOT_NAME")}?start={encoded_url}'
        else:
            return f'Не заполнено поле: {self.building.latin_name} или {self.campaign_id} или {self.site_id}'
