from django.contrib import admin

from .models import UserBot, Developer, Address, Building, Flat, News, XmlLink, SpecialOffer, LocationPhoto, \
    ProcessingCorpusPhoto, InteriorPhoto, ShowRoomPhoto, Documentation, AboutProjectPhoto, Bank, Benefit, Term


class BuildingDeveloperInline(admin.TabularInline):
    model = Building
    extra = 1


@admin.register(UserBot)
class UserBotAdmin(admin.ModelAdmin):
    list_display = ('__str__', "user", "telegram_id", "telegram_username")
    list_filter = ("user", "telegram_username")
    search_fields = ("user", "telegram_username")


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
    list_display = ('__str__', 'building', 'title', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'building', 'display_image', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)


@admin.register(XmlLink)
class XmlLinkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'xml_link', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)


@admin.register(Documentation)
class Documentation(admin.ModelAdmin):
    list_display = ('__str__', 'building', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)


class PhotoBase(admin.ModelAdmin):
    list_display = ('__str__', 'display_image', 'created_at', 'updated_at')
    list_filter = ('building',)
    search_fields = ('building',)
    readonly_fields = ('display_image', 'created_at', 'updated_at')


@admin.register(LocationPhoto)
class LocationPhotoAdmin(PhotoBase):
    pass


@admin.register(ProcessingCorpusPhoto)
class ProcessingCorpusPhotoAdmin(PhotoBase):
    pass


@admin.register(InteriorPhoto)
class InteriorPhotoAdmin(PhotoBase):
    pass


@admin.register(ShowRoomPhoto)
class ShowRoomPhotoAdmin(PhotoBase):
    pass


@admin.register(AboutProjectPhoto)
class AboutProjectPhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'display_image', 'created_at', 'updated_at')
    list_filter = ('developer',)
    search_fields = ('developer',)
    readonly_fields = ('display_image', 'created_at', 'updated_at')


class TermBankInline(admin.TabularInline):
    model = Term
    extra = 1


class TermBenefitInline(admin.TabularInline):
    model = Term
    extra = 1


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    inlines = (TermBankInline,)
    list_display = ('__str__', 'developer', 'created_at', 'updated_at')
    list_filter = ('title', 'developer',)
    search_fields = ('title', 'developer',)


@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    inlines = (TermBenefitInline,)
    list_display = ('__str__', 'developer', 'created_at', 'updated_at')
    list_filter = ('developer',)
    search_fields = ('developer',)


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'bank', 'benefit', 'developer', 'title', 'it_term', 'installment_term', 'created_at', 'updated_at')
    list_filter = ('bank', 'benefit', 'developer', 'title', 'it_term', 'installment_term')
    search_fields = ('bank', 'benefit', 'developer', 'title', 'it_term', 'installment_term')
