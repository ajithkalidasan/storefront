from django.contrib import admin

from .models import Tag, TaggedItem

# Register your models here.

admin.site.register(TaggedItem)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]
