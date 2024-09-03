from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import FilterSet
from .models import Product, Collection


class DefaultPagination(PageNumberPagination):
    """
    DefaultPagination provides pagination settings for API views.

    This pagination class inherits from DRF's PageNumberPagination
    and sets a default page size of 10 items per page.

    """

    page_size = 10


class ProductFilter(FilterSet):
    """
    ProductFilter allows filtering of Product objects based on specific fields.

    The filter supports the following fields:
    - `title` (case-insensitive containment search)
    - `collection` (exact match)
    - `price` (less than `lt` and greater than `gt`)

    """

    class Meta:
        model = Product
        fields = {
            "title": ["icontains"],
            "collection": ["exact"],
            "price": ["lt", "gt"],
        }


class CollectionFilter(FilterSet):
    """
    CollectionFilter allows filtering of Collection objects based on specific fields.

    The filter supports the following fields:
    - `title` (case-insensitive containment search)
    - `featured_product` (exact match)

    """

    class Meta:
        model = Collection
        fields = {
            "title": ["icontains"],
            "featured_product": ["exact"],
        }
