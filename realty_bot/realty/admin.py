from django.contrib import admin

from .models import UserBot, Developer, Profile, Address, Building, News, XmlLink, SpecialOffer, LocationPhoto, \
    ProcessingCorpusPhoto, InteriorPhoto, ShowRoomPhoto, Documentation, AboutProjectVideo, Term, Construction, \
    SalesDepartment, CallRequest, CallTrackingCampaign, CallTrackingCampaignCredentials, ProgressVideo, Corpus, \
    AnnouncementVideo, AboutProjectPhoto, BusinessLifePhoto, PersonalOfferPhoto, AboutProjectPresentation


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'developer', 'created_at', 'updated_at')
    list_filter = ('developer',)
    search_fields = ('developer',)
    readonly_fields = ('created_at', 'updated_at')


class BuildingDeveloperInline(admin.TabularInline):
    model = Building
    extra = 1


@admin.register(UserBot)
class UserBotAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'telegram_id', 'telegram_username', 'telegram_first_name', 'telegram_last_name')
    # list_filter = ('telegram_username',)
    search_fields = ('telegram_username',)


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    # inlines = (BuildingDeveloperInline,)
    list_display = ('__str__', 'developer_name', 'created_at', 'updated_at')
    list_filter = ('developer_name',)
    search_fields = ('developer_name',)


class NewsBuildingInline(admin.TabularInline):
    model = News
    extra = 1


class SpecialOfferBuildingInline(admin.TabularInline):
    model = SpecialOffer
    extra = 1


class XmlLinkBuildingInline(admin.TabularInline):
    model = XmlLink
    extra = 1


class DocumentationBuildingInline(admin.TabularInline):
    model = Documentation
    extra = 1


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    inlines = (NewsBuildingInline, SpecialOfferBuildingInline, XmlLinkBuildingInline, DocumentationBuildingInline)
    list_display = ('__str__', 'latin_name', 'developer', 'created_at', 'updated_at')
    list_filter = ('developer',)
    search_fields = ('developer',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'country', 'region', 'city', 'street', 'house', 'corpus', 'created_at', 'updated_at')
    list_filter = ('country', 'region', 'city')
    search_fields = ('country', 'region', 'city')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'building', 'title', 'display_image', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'building', 'display_image', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)


@admin.register(XmlLink)
class XmlLinkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'xml_link', 'type_of_xml', 'created_at', 'updated_at')
    list_filter = ('building', 'type_of_xml')
    search_fields = ('building', 'type_of_xml')


@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'building', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)


@admin.register(Documentation)
class Documentation(admin.ModelAdmin):
    list_display = ('__str__', 'building', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)


class PhotoBase(admin.ModelAdmin):
    list_display = ('__str__', 'display_image', 'order', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)
    readonly_fields = ('display_image', 'created_at', 'updated_at')


@admin.register(AnnouncementVideo)
class AnnouncementVideoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'display_video', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)
    readonly_fields = ('display_video', 'created_at', 'updated_at')


@admin.register(BusinessLifePhoto)
class BusinessLifePhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'display_image', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)
    readonly_fields = ('display_image', 'created_at', 'updated_at')


@admin.register(PersonalOfferPhoto)
class PersonalOfferPhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'display_image', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)
    readonly_fields = ('display_image', 'created_at', 'updated_at')


@admin.register(AboutProjectPhoto)
class AboutProjectPhotoAdmin(PhotoBase):
    pass


@admin.register(LocationPhoto)
class LocationPhotoAdmin(PhotoBase):
    pass


@admin.register(ProcessingCorpusPhoto)
class ProcessingCorpusPhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'corpus', 'display_image', 'order', 'created_at', 'updated_at')
    list_filter = ('building', 'corpus')
    search_fields = ('building', 'corpus')
    readonly_fields = ('display_image', 'created_at', 'updated_at')


@admin.register(InteriorPhoto)
class InteriorPhotoAdmin(PhotoBase):
    pass


@admin.register(ShowRoomPhoto)
class ShowRoomPhotoAdmin(PhotoBase):
    pass


@admin.register(ProgressVideo)
class ProgressVideoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'video_url', 'source_url', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)
    readonly_fields = ('display_video', 'created_at', 'updated_at')


@admin.register(AboutProjectVideo)
class AboutProjectVideoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'display_video', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)
    readonly_fields = ('display_video', 'created_at', 'updated_at')


@admin.register(AboutProjectPresentation)
class AboutProjectPresentationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'building', 'title', 'order', 'created_at', 'updated_at')
    list_filter = ('building', 'title')
    search_fields = ('building', 'title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'developer', 'building', 'type_of_term', 'bank', 'payment', 'created_at', 'updated_at')
    list_filter = ('developer', 'type_of_term', 'bank',)
    search_fields = ('developer', 'type_of_term', 'bank',)


@admin.register(Construction)
class ConstructionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'display_image', 'is_active', 'is_published', 'photo_date', 'created_at', 'updated_at')
    list_filter = ('building', 'is_active', 'is_published')
    search_fields = ('building', 'is_active', 'is_published')


@admin.register(SalesDepartment)
class SalesDepartmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'developer')
    list_filter = ('building', 'developer')
    search_fields = ('building', 'developer')


@admin.register(CallRequest)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'developer', 'telegram_user', 'telegram_user_phone', 'created_at', 'updated_at')
    list_filter = ('developer', 'building')
    search_fields = ('developer', 'building')


@admin.register(CallTrackingCampaign)
class CallTrackingCampaignAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'campaign_name', 'start_button', 'call_tracking_name', 'phone_number', 'developer', 'url_base64_encode', 'campaign_id', 'site_id', 'created_at', 'updated_at')
    list_filter = ('developer', 'call_tracking_name')
    search_fields = ('developer', 'call_tracking_name')
    fieldsets = (
        ('Some name', {
            'fields': ('campaign_name',
                       'developer',
                       'building',
                       'call_tracking_name',
                       'url_base64_encode',
                       'api_token',
                       'campaign_id',
                       'site_id',
                       'route_key',
                       'start_button',
                       'phone_number',
                       'created_at',
                       'updated_at'
)
        }),
    )
    readonly_fields = ['__str__', 'created_at', 'updated_at', 'url_base64_encode']


@admin.register(CallTrackingCampaignCredentials)
class CallTrackingCampaignCredentialsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'developer', 'access_token')
    list_filter = ('developer', 'building')
    search_fields = ('developer', 'building')
