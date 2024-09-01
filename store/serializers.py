from rest_framework import serializers
from decimal import Decimal
from .models import  Product, Collection

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', ]
    


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='calculated_tax')
    collection = serializers.StringRelatedField()

    class Meta:
        model = Product
        
        fields = ['id', 'title', 'price', "price_with_tax", "collection"]
        

  

    def calculated_tax(self, product: Product):
        return product.price + product.price * Decimal(0.18)
