from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from products.models import Product

# Create your views here.
def get_products(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type = "application/json")