from django.contrib import admin
# Register your models here.
from .models import *
from django.utils.translation import gettext_lazy as _


class DeleteUndeleteMixin:
    def mark_deleted(self, request, queryset):
        queryset.update(deleted=True)

    def un_delete(self, request, queryset):
        queryset.update(deleted=False)

    mark_deleted.short_description = _("Отметить на удалени")
    un_delete.short_description = _("Убрать отметку удаления")

class DiseaseAdmin(admin.ModelAdmin, DeleteUndeleteMixin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug", "created_at", "deleted")
    list_display_links = ("id", "title", "slug")
    search_fields = ("title","tags")
    fields = ("title", "slug", "description", "codemkb", "search", "tags", "communities", "created_at", "updated_at", "deleted")
    readonly_fields = ("created_at", "updated_at")

class CommunityAdmin(admin.ModelAdmin, DeleteUndeleteMixin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug", "created_at", "deleted")
    list_display_links = ("id", "title", "slug")
    search_fields = ("title",)
    fields = ("title", "slug", "description", "created_at", "updated_at", "deleted")
    readonly_fields = ("created_at", "updated_at")

class ContactAdmin(admin.ModelAdmin, DeleteUndeleteMixin):
    save_as = True
    save_on_top = True
    list_display = ("id", "type","community","created_at", "deleted")
    list_display_links = ("id","type", "community")
    search_fields = ("title",)
    fields = ("community","type", "content","created_at","updated_at", "deleted")
    readonly_fields = ("created_at", "updated_at")

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    fields = ("title", "slug", "deleted")

admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Tag, TagAdmin)

admin.site.site_title = 'Управление сайтом Редкиеболезни - сообщества пациентов'
admin.site.site_header = 'Управление сайтом Редкиеболезни - сообщества пациентов'