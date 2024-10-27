from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from products.models import Product
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def get_products(request):
    data = Product.objects.all()

    return HttpResponse(serializers.serialize("json", data), content_type = "application/json")

# @login_required()
def show_product(request):
    # Get all the products from the data base
    products = Product.objects.all()

    paginator= Paginator(products, 20)

    page_number = request.GET.get('page', 1)

    try:
        page_number = int(page_number)  # Biar enggak AttributeError
    except ValueError:
        page_number = 1

    page_products = paginator.get_page(page_number)

    return render(request, "main.html", {"page_products": page_products})