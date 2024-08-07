from django.contrib import admin
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
admin.site.register(Product)
admin.site.register(Collection)
admin.site.register(Promotion)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
