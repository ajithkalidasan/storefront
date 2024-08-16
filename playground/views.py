from django.shortcuts import render
from django.http import HttpResponse
from store.models import Customer, Product


# Create your views here.
def hello(request):
    # customer = Customer.objects.all()[:10]
    customer = Customer.objects.values("first_name",  "email")[:10]
    product = Product.objects.filter(pk=1).first()
    membership = Customer.objects.filter(membership="G")[:10]
    context = {"customer": customer, "product": product, "membership": membership}
    return render(request, "hello.html", context)
