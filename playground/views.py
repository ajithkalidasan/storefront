from django.shortcuts import render
from .tasks import notify_customer




# Create your views here.
def hello(request):
    notify_customer.delay("hello")
    
    
    return render(request, "hello.html")
