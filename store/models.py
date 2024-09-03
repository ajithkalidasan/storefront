"""
This module defines the data models for an e-commerce application using Django's ORM.

Models:
    Product: Represents a product with details such as title, content, price, inventory, and associations with collections and promotions.
    Customer: Represents a customer with personal details and membership status.
    Order: Represents an order placed by a customer, including payment status and associations with order items.
    OrderItem: Represents an item within an order, including the product, quantity, and unit price.
    Address: Represents a customer's address.
    Collection: Represents a collection of products.
    Cart: Represents a shopping cart.
    CartItem: Represents an item within a shopping cart, including the product and quantity.
    Promotion: Represents a promotion applied to products, including a description and discount.

Usage:
    Use these models to create, retrieve, update, and delete instances in the e-commerce database.
"""

from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(default="")
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=99.99)
    inventory = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        "Collection", on_delete=models.PROTECT, related_name="products"
    )
    promotions = models.ManyToManyField("Promotion")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_CHOICES = (
        ("MEMBERSHIP_BRONZE", "Basic"),
        ("MEMBERSHIP_SILVER", "Silver"),
        ("MEMBERSHIP_GOLD", "Gold"),
    )
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=120)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=18, choices=MEMBERSHIP_CHOICES, default="MEMBERSHIP_BRONZE"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "store_customers"
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
        ]
        ordering = ["first_name", "last_name"]


class Order(models.Model):
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETED = "C"
    PAYMENT_STATUS_FAILED = "F"
    PAYMENT_STATUS_CHOICES = (
        ("PAYMENT_STATUS_PENDING", "Pending"),
        ("PAYMENT_STATUS_COMPLETED", "Completed"),
        ("PAYMENT_STATUS_FAILED", "Failed"),
    )
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=30, choices=PAYMENT_STATUS_CHOICES, default="PAYMENT_STATUS_PENDING"
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="addresses"
    )
    zip = models.CharField(max_length=120)


class Collection(models.Model):
    title = models.CharField(max_length=120, null=True, blank=True)
    featured_product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    def __str__(self):
        return self.title


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Promotion(models.Model):
    description = models.CharField(max_length=255, null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)

    def __self__(self):
        return self.description
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name