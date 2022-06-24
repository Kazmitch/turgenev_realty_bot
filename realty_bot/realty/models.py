from django.utils.functional import cached_property
from django.utils.html import format_html

from django.db import models
from django.contrib.auth.models import User

from realty_bot.realty_bot.utils import user_directory_path, about_project_path


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    class Meta:
        abstract = True


class UserBot(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.BigIntegerField(verbose_name="ID Пользователя Телеграм", unique=True, blank=True, null=True)
    telegram_username = models.CharField(verbose_name="Username Телеграм", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"

    def __str__(self):
        return f"{self.user.get_full_name()}"


class Developer(BaseModel):
    developer_name = models.CharField(verbose_name="Название застройщика", max_length=255, blank=False)
    latin_name = models.CharField(verbose_name="Название на английском", max_length=255, unique=True, null=True,
                                  help_text='В формате <b>some_developer_name</b>')
    developer_description = models.TextField(verbose_name="Описание застройщика", blank=True,
                                             help_text='Не больше 1024 символов')

    class Meta:
        verbose_name = "Застройщик"
        verbose_name_plural = "Застройщики"

    def __str__(self):
        return f"{self.developer_name}"


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
    name = models.CharField(verbose_name="Название ЖК", max_length=255, unique=True, blank=False)
    latin_name = models.CharField(verbose_name="Название на английском", max_length=255, unique=True, null=True,
                                  help_text='В формате <b>some_building_name</b>')
    address = models.OneToOneField(Address, verbose_name="Адрес", on_delete=models.CASCADE, null=True)
    developer = models.ForeignKey(Developer, verbose_name="Застройщик", related_name="buildings",
                                  on_delete=models.CASCADE, null=True)
    building_description = models.TextField(verbose_name="Описание ЖК", blank=True)
    floors_total = models.CharField(verbose_name="Количество этажей", max_length=32, blank=False)
    built_year = models.DateField(verbose_name="Год сдачи (год постройки)", blank=False)
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
    floor = models.CharField(verbose_name="Этаж", max_length=32, blank=False, null=True)
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


class News(BaseModel):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс", related_name="news",
                                 null=True)
    title = models.CharField(verbose_name="Заголовок", max_length=255, null=True)
    text = models.TextField(verbose_name="Текст новости", blank=False, null=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title}"


class XmlLink(BaseModel):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name="xml_links", null=True)
    xml_link = models.TextField(verbose_name="Ссылка на xml", blank=True, null=True)

    class Meta:
        verbose_name = "XML Ссылка"
        verbose_name_plural = "XML Ссылки"

    def __str__(self):
        return f"{self.building.name} XML"


class SpecialOffer(BaseModel):
    directory = 'photo/special_offer'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name="special_offers", null=True)
    title = models.CharField(verbose_name="Заголовок спецпредложения", max_length=255, blank=False, null=True)
    description = models.TextField(verbose_name="Описание спецпредложения", null=True)
    photo = models.ImageField(upload_to=user_directory_path, verbose_name="Фотография")

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


class AboutProjectPhoto(BaseModel):
    directory = 'photo/about_project'
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, verbose_name="Застройщик",
                                  related_name="about_projects")
    photo = models.ImageField(upload_to=about_project_path, verbose_name="Фотография")

    class Meta:
        verbose_name = "О проекте Фото"
        verbose_name_plural = "О проекте Фото"

    def __str__(self):
        return f"{self.developer.developer_name}"

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
                                 related_name='corps')
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='Фотография')

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


class Documentation(BaseModel):
    directory = 'documents/declaration'
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Жилой комплекс",
                                 related_name='documentations')
    title = models.CharField(verbose_name="Название документа", max_length=255, blank=False, null=True)
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
    directory = 'documents/term'
    bank = models.CharField(verbose_name="Банк", max_length=64, choices=Bank.choices, null=True, blank=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, verbose_name="Застройщик", related_name="terms")
    type_of_term = models.CharField(verbose_name="Тип условия", max_length=64, choices=TypeOfTerm.choices)
    payment = models.IntegerField(verbose_name="Ежемесячный платёж", blank=True)
    title = models.CharField(verbose_name="Условие", max_length=255)
    description = models.TextField(verbose_name="Описание условия")
    document = models.FileField(upload_to=user_directory_path, verbose_name='Документ', blank=True)

    class Meta:
        verbose_name = "Условие"
        verbose_name_plural = "Условия"

    def __str__(self):
        return f"{self.title}"
