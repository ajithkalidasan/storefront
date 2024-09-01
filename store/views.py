from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product,Collection
from .serializers import ProductSerializer, CollectionSerializer


# Create your views here.
class ProductView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_serializer_context(self):
        return {'request': self.request}

    
    
        
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
   
    def get_serializer_context(self):
        return {'request': self.request}
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.inventory == 0:
            return Response("can't delete a product with 0 inventory")
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionsView(ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
class CollectionsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    
    

    
    
