from django.contrib import admin
from .models import (UserBot, Building, Developer, SpecialOffer, LocationPhoto, ProcessingCorpus,
                     Interior, ShowRoomPhoto)

# Register your models here.


@admin.register(UserBot)
class UserBotAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_id', 'telegram_username', 'created_at', 'updated_at')
    list_filter = ('user', 'telegram_id', 'telegram_username')
    search_fields = ('user', 'telegram_id', 'telegram_username')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основные поля', {
            'fields': ('user', 'telegram_id', 'telegram_username')
        }),
        ('Дополнительные поля', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('developer_name', 'developer_description', 'created_at', 'updated_at')
    list_filter = ('developer_name', 'developer_description')
    search_fields = ('developer_name', 'developer_description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основные поля', {
            'fields': ('developer_name', 'developer_description')
        }),
        ('Дополнительные поля', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'latin_name',
        'address',
        'developer',
        'built_year',
        'ready_quarter',
        'building_type',
    )
    list_filter = ('developer', 'latin_name')
    search_fields = (
        'name',
        'latin_name',
        'address',
        'developer',
        'building_description'
    )
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основные поля', {
            'fields': (
                'name',
                'latin_name',
                'address',
                'developer',
                'building_description',
                'floors_total',
                'built_year',
                'ready_quarter',
                'building_type',
                'building_section',
                'ceiling_height',
                'lift',
                'guarded_building',
                'parking',
            )
        }),
        ('Дополнительные поля', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('building', 'title', 'description', 'created_at', 'updated_at')
    list_filter = ('building', 'title', 'description')
    search_fields = ('building', 'title', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основные поля', {
            'fields': ('building', 'title', 'description')
        }),
        ('Дополнительные поля', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


class BasePhotoAdmin(admin.ModelAdmin):
    list_display = ('building', 'photo', 'created_at', 'updated_at')
    list_filter = ('building', 'photo')
    search_fields = ('building', 'photo')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основные поля', {
            'fields': ('building', 'photo')
        }),
        ('Дополнительные поля', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(LocationPhoto)
class LocationPhotoAdmin(BasePhotoAdmin):
    pass


@admin.register(ProcessingCorpus)
class ProcessingCorpusAdmin(BasePhotoAdmin):
    pass


@admin.register(Interior)
class InteriorAdmin(BasePhotoAdmin):
    pass


@admin.register(ShowRoomPhoto)
class ShowRoomPhotoAdmin(BasePhotoAdmin):
    pass

