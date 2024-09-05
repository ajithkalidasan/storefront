from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection, Review, CartItem, Cart


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name="calculated_tax")
    collection = serializers.StringRelatedField()

    class Meta:
        model = Product

        fields = ["id", "title", "price", "price_with_tax", "collection"]

    def create(self, validated_data):
        collection_id = self.context["collection_id"]
        return Product.objects.create(**validated_data, collection_id=collection_id)

    def calculated_tax(self, product: Product):
        return product.price + product.price * Decimal(0.18)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "description", "date"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price"]
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer() #SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()
    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price
        
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
        
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']