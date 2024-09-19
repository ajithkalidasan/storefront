from django.views.decorators.cache import cache_page
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from .tasks import notify_customer
import requests
import logging

logger = logging.getLogger(__name__)



class HelloView(APIView):
    
    def get(self, request):
        try:
            logger.info("Callinf httpbib")
            response = requests.get("https://httpbin.org/delay/2") 
            logger.info("Getting htttp.bin")  
            data = response.json()
        except requests.ConnectionError:
            logger.critical("Connection error")
    
        # Pass the API data to the template
        return render(request, "hello.html", {'name': "data"})
        
# Cache the entire view for 60 seconds
