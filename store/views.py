from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Product,Collection, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer


# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_serializer_context(self):
        return {"collection_id": self.kwargs.get("collection_pk")}
    
    def destroy(self, request, *args, **kwargs):
        if self.get_object().inventory == 0:
            return Response({'error':"can't delete a product with 0 inventory"})
        return super().destroy(request, *args, **kwargs)
    
   

   
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    def get_serializer_context(self):
        return {'request': self.request}
    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error':"can't delete a collection with products"})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
  
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs.get('product_pk'))
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}
        
    

    
    
