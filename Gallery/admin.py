from django.contrib import admin

# Register your models here.

from .models import Card, AboutAuthor, Tag, CardTag


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type']
    search_fields = ['title', 'description']


admin.site.register(AboutAuthor)
admin.site.register(Tag)
admin.site.register(CardTag)