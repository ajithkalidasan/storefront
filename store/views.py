from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import Product,Collection
from .serializers import ProductSerializer, CollectionSerializer


# Create your views here.
@api_view(["GET", "POST", "PUT", "DELETE"])
def product_list(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok')
    elif request.method == "PUT":
        product = get_object_or_404(Product, pk=request.data["id"])
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok')
    elif request.method == "DELETE":
        product = get_object_or_404(Product, pk=request.data["id"])
        product.delete()
        return Response('ok')
        

@api_view()
def product_detail(request,id):
    product = get_object_or_404(Product, pk=id) 
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(["GET", "POST", "PUT", "DELETE"])
def collections(request):
    if request.method == "GET":
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Created')
    elif request.method == "PUT":
        collections = get_object_or_404(Collection, pk=request.data["id"])
        serializer = CollectionSerializer(collections, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('updated')
    elif request.method == "DELETE":
        collections = get_object_or_404(Collection, pk=request.data["id"])
        collections.delete()
        return Response('deleted')
    
@api_view(["GET","PATCH", "DELETE"])
def collections_details(request,id):
    collections = get_object_or_404(Collection, pk=id) 
    if request.method == "PATCH":
        serializer = CollectionSerializer(collections,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok')
    elif request.method == "DELETE":
        collections.delete()
        return Response('ok')
    elif request.method == "GET":
        serializer = CollectionSerializer(collections)
        return Response(serializer.data)
    
    
