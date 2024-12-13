from django.shortcuts import render
import datetime
from django.http import JsonResponse
from WishList.models import WishlistItem
from .forms import WishlistItemForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.http import HttpResponse
from django.urls import reverse
from django.core import serializers
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
@login_required
def view_wishlist(request):
    context = {
        'npm' : '911',
        'name': 'easteregg',
        'class': 'skibidi'
    }
    return render(request, "wishlist.html", context)

def get_product_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_wishlist_json(request):
    data = WishlistItem.objects.filter(user= request.user) # for now .all karena belum ada login loginan segala
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_product_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@login_required
def tambah_wishlist_ajax(request):
    if request.method == 'POST':
        form = WishlistItemForm(request.POST)
        if form.is_valid():
            wishlist_item = form.save(commit=False)
            wishlist_item.user = request.user
            wishlist_item.save()
            return JsonResponse({'status': 'success', 'message': 'Produk berhasil ditambahkan ke wishlist!'})
        return JsonResponse({'status': 'error', 'message': 'Form tidak valid.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

@csrf_exempt
@login_required
def delete_wish(request, id):
    wishlist = WishlistItem.objects.get(pk = id)
    wishlist.delete()
    return HttpResponseRedirect(reverse('WishList:view_wishlist'))


@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    product_id = request.POST.get('produk')
    new_product = Product.objects.get(id=product_id)
    quantity = request.POST.get("quantity")
    user = request.user
    date = str(datetime.datetime.now())
    harga = new_product.price
    product_name = new_product.product_name
    new_wishlist = WishlistItem(
        user = user,
        produk = new_product,
        jumlah = quantity,
        date_added = date,
        price = harga,
        nama_produk = product_name
    )
    new_wishlist.save()

    if request.method == 'POST':
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'}, status=400)