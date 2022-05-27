from django.http import JsonResponse
from onlineorder.models import Category, Product
from .serializer import CategorySerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework import generics, serializers
from rest_framework.decorators import api_view


def apiOverview(request):
    return JsonResponse("Api Base view", safe=False)


@api_view(['GET'])
def categorylistapi(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def productlistapi(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)
