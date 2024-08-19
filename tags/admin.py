from django.contrib import admin

from .models import Tag, TaggedItem

# Register your models here.

admin.site.register(TaggedItem)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Tag model.
    """

    # Define which fields to display in the admin interface.
    list_display = [
        "label",
    ]

    # Define which fields to use for searching in the admin interface.
    search_fields = [
        "label",
    ]

    # The __str__ method is used to represent the model object as a string
    # in various admin interfaces.
