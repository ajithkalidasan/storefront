from rest_framework import serializers
from decimal import Decimal
from .models import  Product, Collection, Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title' ]
    


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='calculated_tax')
    collection = serializers.StringRelatedField()

    class Meta:
        model = Product
        
        fields = ['id', 'title', 'price', "price_with_tax", "collection"]
        

    def create(self, validated_data):
        collection_id = self.context['collection_id']
        return Product.objects.create(**validated_data, collection_id=collection_id)
  

    def calculated_tax(self, product: Product):
        return product.price + product.price * Decimal(0.18)
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)
