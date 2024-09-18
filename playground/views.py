from django.views.decorators.cache import cache_page
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from .tasks import notify_customer
import requests


class HelloView(APIView):
    @method_decorator(cache_page(5*60))
    def get(self, request):
        response = requests.get("https://httpbin.org/delay/2")   
        data = response.json()
    
        # Pass the API data to the template
        return render(request, "hello.html", {'name': "data"})
        
# Cache the entire view for 60 seconds
