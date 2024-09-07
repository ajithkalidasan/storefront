from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter, NestedDefaultRouter

from . import views

# Main router
router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")
router.register("collections", views.CollectionViewSet, basename="collection")
router.register("cart", views.CartViewSet, basename="cart")
router.register("customers", views.CustomerViewSet, basename="customer")

# Nested router for product reviews
products_router = NestedSimpleRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

carts_router = NestedDefaultRouter(router, "cart", lookup="cart_pk")
carts_router.register("items", views.CartItemViewSet, basename="cart-items")
urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
    path("", include(carts_router.urls)),
]
