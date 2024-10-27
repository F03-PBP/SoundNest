from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from products.models import Product
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def get_products(request):
    data = Product.objects.all()

    return HttpResponse(serializers.serialize("json", data), content_type = "application/json")

@login_required()
def show_product(request):
    # Get all the products from the data base
    products = Product.objects.all().order_by('-created_at')

    paginator= Paginator(products, 20)

    page_number = request.GET.get('page', 1)

    try:
        page_number = int(page_number)  # Biar enggak AttributeError
    except ValueError:
        page_number = 1

    page_products = paginator.get_page(page_number)

    last_login = request.user.last_login

    return render(request, "main.html", {"page_products": page_products, "last_login": last_login})

@login_required()
def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'details.html', {'product': product})

@csrf_exempt
@require_POST
def add_product(request):
    try:
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        rating = request.POST.get('rating')
        reviews = request.POST.get('reviews')

        rating = float(rating)

        # Create a new Product instance
        product = Product.objects.create(
            product_name=product_name,
            price=price,
            rating=rating,
            reviews=reviews
        )

        return JsonResponse({
            'success': True,
            'product': {
                'product_name': product.product_name,
                'price': product.price,
                'rating': product.rating,
                'reviews': product.reviews,
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})