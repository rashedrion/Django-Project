from importlib.resources import path
from django.urls.resolvers import URLPattern
from onlineorder.api.serializer import CategorySerializer
from . import views
from rest_framework import generics
from onlineorder.models import*

urlPatterns = [
    path('categories/', views.categorylistapi),
    path('productapi/', views.productlistapi),

]
