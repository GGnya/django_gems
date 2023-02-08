from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Gem, GemType, Profile


# Register your models here.

@admin.register(Gem)
class GemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'size', 'type', 'clarity', 'gem_image', 'description',
                    'price', 'owner', 'date_created', 'date_updated')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description', 'type', 'owner')
    prepopulated_fields = {'slug': ("title",)}
    fields = ('id', 'title', 'slug', 'size', 'type', 'clarity', 'gem_image', 'description',
              'price', 'owner', 'is_available', 'date_created', 'date_updated')
    readonly_fields = ('id',)
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.gem_image.url}" width=50>')

    get_html_photo.short_description = 'Миниатюра'


@admin.register(GemType)
class GemTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    list_display_links = ('type',)
    search_fields = ('type',)
    fields = ('type',)
    readonly_fields = ('id',)
    save_on_top = True


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'user_alias', 'date_created')
