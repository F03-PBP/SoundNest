# Create your views here.

from django.shortcuts import render, redirect
from .models import Sale, Product
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from django.contrib.admin.views.decorators import staff_member_required


def best_deals(request):
    # Add context data to make products visible in template
    context = {
        'is_staff': request.user.is_staff,
        # Add initial data for non-AJAX loadin
        'initial_data': get_deals_data()
    }
    return render(request, "bestdeals.html", context)

def get_deals_data():
    """Helper function to get all deals data"""
    sales = Sale.objects.all()
    top_picks = sales.order_by('-product__rating')
    top_picks_guest = top_picks[:5]
    least_countdown = sales.order_by('sale_end_time')
    available_products = Product.objects.exclude(sales__isnull=False)
    
    return {
        'sales': format_sales_data(sales),
        'top_picks': format_sales_data(top_picks),
        'top_picks_guest': format_sales_data(top_picks_guest),
        'least_countdown': format_sales_data(least_countdown),
        'available_products': format_product_data(available_products)
    }

def format_sales_data(sales):
    """Helper function to format sales data"""
    return [{
        'id': sale.product.id,
        'product_name': sale.product.product_name,
        'original_price': float(sale.product.price),  # Convert Decimal to float for JSON
        'discount': float(sale.discount_percentage),
        'price': float(sale.discounted_price),
        'rating': float(sale.product.rating),
        'sale_end_time': sale.sale_end_time.isoformat(),
        'time_remaining': sale.get_time_remaining,
        'reviews': sale.product.reviews,
    } for sale in sales]

def format_product_data(products):
    """Helper function to format product data"""
    return [{
        'id': product.id,
        'product_name': product.product_name,
        'price': float(product.price),
        'rating': float(product.rating),
        'reviews': product.reviews
    } for product in products]

def show_json(request):
    data = get_deals_data()
    return JsonResponse(data)

    
@csrf_exempt
@require_http_methods(["POST"])
def add_to_deals(request):
    # if request.method == 'POST' and request.user.is_staff:
    data = json.loads(request.body)
    product_id = data.get('product_id')
    discount = data.get('discount')
    
    end_date = data.get('end_date')
   
   
    # Validate and create sale
    try:
        product = Product.objects.get(id=product_id)
        if not Sale.objects.filter(product=product).exists():  # Ensure product is not already in deals
            Sale.objects.create(
                product=product,
                discount_percentage=discount,
                sale_end_time=end_date
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Product already in deals'}, status=400)
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)

@csrf_exempt
@require_http_methods(["PUT"])
def edit_deals(request, product_id):
    try:
        data = json.loads(request.body)
        discount = data.get('discount')
        end_date = data.get('end_date')

        # Find the sale by product_id instead of sale id
        sale = Sale.objects.get(product_id=product_id)
        
        # Update the sale
        sale.discount_percentage = discount
        sale.sale_end_time = end_date
        sale.save()

        return JsonResponse({
            'success': True,
            'message': 'Deal updated successfully'
        })
    except Sale.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Sale not found'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
    
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_deals(request, product_id):
    try:
        # Find and delete the sale by product_id
        sale = Sale.objects.get(product_id=product_id)
        sale.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Deal deleted successfully'
        })
    except Sale.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Sale not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
