from django.shortcuts import render
from products.models import Product

# Create your views here.
def show_product(request):
    # Get all the products from the data base
    products = Product.objects.all()

    return render(request, "main.html", {"products": products})