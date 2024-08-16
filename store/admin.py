from django.contrib import admin
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
)


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    list_per_page = 10
    search_fields = ["first_name", "last_name", "email"]

    @admin.display(ordering="orders_count")
    def orders_count(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer_id": str(customer.id)})
        )
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "featured_product", "products_count"]
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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "inventory_status", "collection_list"]
    list_editable = ["price"]
    list_per_page = 10
    search_fields = ["title"]
    list_select_related = ["collection"]

    def collection_list(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory == 0:
            return "Low"
        elif product.inventory < 10:
            return "Out of stock"
        else:
            return "OK"


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ["description", "discount"]
    list_editable = ["discount"]
    list_per_page = 10
    search_fields = ["description"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "placed_at", "payment_status"]
    list_editable = ["payment_status"]
    list_per_page = 10
    search_fields = ["customer__first_name", "customer__last_name"]


admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
