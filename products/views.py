from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from products.models import Product
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
import json
from django.utils.timezone import now
from reviews.models import Review
from reviews.views import show_reviews


def get_products(request):
    sort_option = request.GET.get('sort', 'latest')  # Default to 'latest'

    if sort_option == 'latest':
        products = Product.objects.all().order_by('-created_at')
    elif sort_option == 'price_asc':
        products = Product.objects.all().order_by('price')
    elif sort_option == 'price_desc':
        products = Product.objects.all().order_by('-price')
    else:
        products = Product.objects.all()  # Default case if sort option is invalid

    return HttpResponse(serializers.serialize("json", products), content_type="application/json")


def show_product(request):
    # Get all the products from the data base
    products = Product.objects.all().order_by('-created_at')

    filter_option = request.GET.get('filter', 'default')

    if filter_option == 'price_asc':
        products = products.order_by('price') 
    elif filter_option == 'price_desc':
        products = products.order_by('-price')

    paginator= Paginator(products, 20)

    page_number = request.GET.get('page', 1)

    try:
        page_number = int(page_number)  # Biar enggak AttributeError
    except ValueError:
        page_number = 1

    page_products = paginator.get_page(page_number)

    # last_login = request.user.last_login

    return render(request, "main.html", {"page_products": page_products})

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = show_reviews(request, product_id)

    context = {
        'product': product,
        'reviews': reviews,
        'product_id': product.id
    }
    return render(request, 'details.html', context)

@csrf_exempt
@require_POST
@login_required
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
    

@csrf_exempt
@require_POST
@login_required
def delete_product(request):
    try:
        data = json.loads(request.body)
        product_id = data.get("id")
        product = get_object_or_404(Product, id=product_id)
        
        # Delete the product
        product.delete()
        
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    
@csrf_exempt
@require_POST
@login_required
def edit_product(request):
    try:
        product_id = request.POST.get("id")
        product = get_object_or_404(Product, id=product_id)
        
        product.product_name = request.POST.get("product_name")
        product.price = int(request.POST.get("price"))
        product.rating = float(request.POST.get("rating"))
        product.reviews = int(request.POST.get("reviews"))
        
        product.save()

        return JsonResponse({
            "success": True,
            "product": {
                "id": product.id,
                "product_name": product.product_name,
                "price": product.price,
                "rating": product.rating,
                "reviews": product.reviews,
            }
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    
def product_details_json(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return JsonResponse({
        "id": product.id,
        "product_name": product.product_name,
        "price": product.price,
        "rating": product.rating,
        "reviews": product.reviews,
    })

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_product = Product.objects.create(
                product_name=data["name"],
                price=int(data["price"]),
                rating=float(data["rating"]),
                reviews=int(data["reviews"]),
                created_at=now()  # Set current timestamp
            )
            new_product.save()
            return JsonResponse({"status": "success", "product_id": new_product.id}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=401)

@csrf_exempt
def edit_product_flutter(request, product_id):
    print(f"Request method: {request.method}")  # Log the request method
    print(f"Request body: {request.body}")  # Log the request body

    if request.method == 'POST':
        try:
            print(f"Received request for product_id: {product_id}")  # Log the product ID
            data = json.loads(request.body)

            # Check if product exists
            product = get_object_or_404(Product, id=product_id)
            print(f"Product found: {product}")  # Log the product details

            # Update product details
            product.product_name = data.get("product_name", product.product_name)
            product.price = int(data.get("price", product.price))
            product.rating = float(data.get("rating", product.rating))
            product.reviews = int(data.get("reviews", product.reviews))
            product.save()

            return JsonResponse({"status": "success"}, status=200)
        except Product.DoesNotExist:
            print("Product not found")
            return JsonResponse({"status": "error", "message": "Product not found"}, status=404)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        print("Invalid method")
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@csrf_exempt
def delete_product_flutter(request, product_id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return JsonResponse({"status": "success"}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)


