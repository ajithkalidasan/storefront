from django.shortcuts import render
from django.http import HttpResponse
from store.models import Customer, Product


# Create your views here.
def hello(request):
    customer = Customer.objects.all()
    product = Product.objects.filter(pk=1).first()
    membership = Customer.objects.filter(membership="G")
    context = {"customer": customer, "product": product, "membership": membership}
    return render(request, "hello.html", context)
