from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Product, Collection, Review, CartItem, Cart
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer

from .utils import DefaultPagination, ProductFilter, CollectionFilter


# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ["title", "collection__title"]
    ordering_fields = ["price", "last_updated"]

    def get_serializer_context(self):
        return {"collection_id": self.kwargs.get("collection_pk")}

    def destroy(self, request, *args, **kwargs):
        if self.get_object().inventory == 0:
            return Response({"error": "can't delete a product with 0 inventory"})
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CollectionFilter
    pagination_class = DefaultPagination

    def get_serializer_context(self):
        return {"request": self.request}

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({"error": "can't delete a collection with products"})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get("product_pk"))

    def get_serializer_context(self):
        return {"product_id": self.kwargs.get("product_pk")}



# Create your views here.

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    
class CardItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id=self.kwargs.get("cart_pk"))\
            .select_related("product")
    