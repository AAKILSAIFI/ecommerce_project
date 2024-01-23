# ecommerce_app/urls.py
from django.urls import path
from .views import product_list

urlpatterns = [
    path('products/', product_list, name='product_list'),
    # Add more paths for other views as needed
]
