# Create your views here.
from django.shortcuts import render, redirect
from .models import Sale, Product
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
from .forms import AddToDealsForm


def best_deals(request):
    sales = Sale.objects.filter(sale_end_time__gt=timezone.now()) # produk yang sekarang sedang promo
    top_picks = sales.order_by('-product__rating')  # sales sorted berdasarkan rating
    top_picks_guest = top_picks[:5] # 5 produk pertama di top picks
    least_countdown = sales.order_by('-sale_start_time')  # sales sorted berdasarkan countdown
    available_products = Product.objects.exclude(sales__isnull=False)  # produk yang tidak sedang promo
    #is_admin = request.user.is_staff  # Check if user is admin

    context = {
        'sales': sales,
        'top_picks': top_picks,
        'least_countdown': least_countdown,
        'available_products': available_products,
        'top_picks_guest': top_picks_guest,
        #'is_admin': is_admin
    }
    return render(request, 'bestdeals.html', context)

@require_http_methods(["DELETE"])
def delete_product(request, product_id):
    try:
        # Assuming you have a Product model
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
def add_to_deals_ajax(request):
    if request.method == 'POST' and request.user.is_staff:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        discount = data.get('discount')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Validate and create sale
        try:
            product = Product.objects.get(id=product_id)
            if not Sale.objects.filter(product=product).exists():  # Ensure product is not already in deals
                Sale.objects.create(
                    product=product,
                    discount_percentage=discount,
                    sale_start_time=start_date or timezone.now(),
                    sale_end_time=end_date
                )
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Product already in deals'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)