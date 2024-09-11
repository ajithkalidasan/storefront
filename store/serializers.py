from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from . signals import order_created
from . import models
from .models import Product, Collection, Review, CartItem, Cart, Customer


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]

class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return models.ProductImage.objects.create(product_id=product_id, **validated_data)
    class Meta:
        model = models.ProductImage
        fields = ["id", "image", ]
class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name="calculated_tax")
    collection = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product

        fields = ["id", "title", "price", "price_with_tax", "collection", "images"]

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
    product = SimpleProductSerializer()  # SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]
        read_only_fields = ["id"]  # These fields will be read-only


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = models.OrderItem
        fields = ["id", "product", "unit_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = models.Order
        fields = ["id", "customer", "placed_at", "payment_status", "items"]

class UpdateOderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ["payment_status"]
    
class CreateOrderSerializer(serializers.Serializer):
    card_id = serializers.UUIDField()
    def validate_cart_id(self, card_id):
        if not Cart.objects.filter(pk=card_id).exists():
            raise serializers.ValidationError("No such cart")
        if CartItem.objects.filter(cart_id=card_id).count() == 0:
            raise serializers.ValidationError("Cart is empty")
        return card_id

    def save(self, **kwargs):
        card_id = self.validated_data["card_id"]
        with transaction.atomic():
            
            (customer, created) = Customer.objects.get_or_create(
                user_id=self.context["user_id"]
            )

            order = models.Order.objects.create(customer=customer)

            cart_items = CartItem.objects.select_related("product").filter(
                cart_id= card_id
            )

            order_items = [
                models.OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.price,
                    quantity=item.quantity,
                )
                for item in cart_items
            ]
            models.OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.filter(pk= card_id).delete()
            order_created.send_robust(self.__class__, order=order)
            return order
        

        
