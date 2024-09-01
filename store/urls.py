from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductView.as_view()),
    path('products/<int:pk>/', views.ProductDetailView.as_view()),
    path('collections/', views.CollectionsView.as_view()),
    path('collections/<int:pk>/', views.CollectionsDetailView.as_view(), name='collections_details'),
    
]
