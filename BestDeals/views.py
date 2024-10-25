# Create your views here.
from django.shortcuts import render, redirect
from .models import Sale, Product
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
from .forms import AddToDealsForm


def best_deals(request):
    sales = Sale.objects.filter(sale_end_time__gt=timezone.now()).order_by('-sale_start_time')
    return render(request, 'bestdeals.html', {'sales': sales})

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