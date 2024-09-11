from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product
from store.admin import ProductImageInLine


# Register your models here.
class TagInline(GenericTabularInline):
    autocomplete_fields = ["tag"]
    model = TaggedItem
    extra = 1


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInLine]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
