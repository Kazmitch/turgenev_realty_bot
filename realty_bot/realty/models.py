from django.db import models
from django.contrib.auth.models import User


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
    developer_description = models.TextField(verbose_name="Описание застройщика", blank=True)

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


class Building(BaseModel):
    name = models.CharField(verbose_name="Название ЖК", max_length=255, unique=True, blank=False)
    latin_name = models.CharField(verbose_name="Название на английском", max_length=255, unique=True, null=True)
    address = models.ForeignKey(Address, verbose_name="Адрес", on_delete=models.CASCADE, null=True)
    developer = models.ForeignKey(Developer, verbose_name="Застройщик", on_delete=models.CASCADE, null=True)
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
    building_name = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    flat_description = models.TextField(verbose_name="Описание квартиры", blank=True)
    floor = models.CharField(verbose_name="Этаж", max_length=32, blank=False, null=True)
    rooms = models.CharField(verbose_name="Количество комнат", max_length=32, blank=True)
    studio = models.BooleanField(verbose_name="Студия", blank=True, null=True)
    total_area = models.CharField(verbose_name="Общая площадь", max_length=32, blank=False, null=True)
    living_area = models.CharField(verbose_name="Жилая площадь", max_length=32, blank=True)
    kitchen_area = models.CharField(verbose_name="Площадь кухни", max_length=32, blank=True)
    bath_area = models.CharField(verbose_name="Площадь санузла", max_length=32, blank=True)
    price = models.CharField(verbose_name="Стоимость квартиры", max_length=32, blank=False, null=True)

    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"

    def __str__(self):
        return f"{self.building_name} {self.total_area} {self.rooms} {self.price}"


class News(BaseModel):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    title = models.CharField(verbose_name="Заголовок", max_length=255, blank=False, null=True)
    text = models.TextField(verbose_name="Текст новости", blank=False, null=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return f"{self.title}"


class XmlLinks(BaseModel):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    xml_link = models.TextField(verbose_name="Ссылка на xml", blank=True, null=True)

    class Meta:
        verbose_name = "XML Ссылка"
        verbose_name_plural = "XML Ссылки"

    def __str__(self):
        return f"{self.building.name} XML"
