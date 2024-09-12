from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import (
    Product,
    Collection,
    Promotion,
    Customer,
    Order,
    OrderItem,
    Address,
    Cart,
    CartItem,
    Review,
    ProductImage
)


# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
    """
    A custom list filter for the admin interface that filters products by inventory.
    """

    # The title of the filter that will be displayed in the admin interface.
    title = "inventory"

    # The name of the parameter that will be used in the URL query string.
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples that represent the available options for the filter.
        The first element of each tuple is the actual value of the filter, and the second
        element is the display name of the filter option.
        """
        return [
            # The "<10" value is used to filter products with inventory less than 10.
            # The "Low" label is what will be displayed in the admin interface for this filter option.
            ("<10", "Low"),
        ]

    def queryset(self, request, queryset):
        """
        Filters the queryset based on the selected filter value.
        If the filter value is "<10", the queryset will be filtered to only include products
        with inventory less than 10.
        """
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [
            ("<10", "Low"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)





@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "featured_product", "products_count"]
    list_editable = ["featured_product"]
    list_per_page = 10
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection_id": str(collection.id)})
        )
        return format_html('<a href="{}">{}', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("products"))


class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    readonly_fields = ["thumbnail"]
    
    def thumbnail(self, instance):
        if instance.image.name !='':
            return format_html(
                f'<img src="{instance.image.url}" style="max-width: 100px; max-height: 100px; object-fit: cover;/">'
            )
        return "No image"
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    autocomplete_fields = ["collection"]
    actions = ["clear_inventory", "update_inventory"]
    inlines = [ProductImageInLine]
    list_display = ["title", "price", "inventory_status", "collection_list"]
    list_editable = ["price"]
    list_filter = [
        "collection",
        "last_updated",
        InventoryFilter,
    ]
    list_per_page = 10
    search_fields = ["title"]
    list_select_related = ["collection"]

    def collection_list(self, product):
        return product.collection.title

    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were cleared from inventory.",
            messages.ERROR,
        )

    def update_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=100)
        self.message_user(
            request,
            f"{updated_count} products were updated.",
            messages.SUCCESS,
        )

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory == 0:
            return "Low"
        elif product.inventory < 10:
            return "Out of stock"
        else:
            return "OK"
    class Media:
        css = {"all": ["store/style.css"]}


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ["description", "discount"]
    list_editable = ["discount"]
    list_per_page = 10
    search_fields = ["description"]


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ["product"]
    min_num = 1
    max_num = 10
    model = OrderItem
    extra = 0




   


admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Customer)
