from django.shortcuts import render
from django.http import JsonResponse
from WishList.models import WishlistItem, Produk
from .forms import WishlistItemForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from WishList.models import Produk, WishlistItem
from django.http import HttpResponse
from django.urls import reverse
from django.core import serializers
from django.http import HttpResponseRedirect
def view_wishlist(request):
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E'
    }
    return render(request, "main.html", context)
# Create your views here.

def get_produk_list(request):
    produk_list = WishlistItem.objects.all()
    return render(request, 'main.html', {'produk': produk_list})

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

# @login_required
# def wishlist_view(request):
#     wishlist_items = request.user.wishlist.all()
#     return render(request, 'main.html', {'wishlist_items': wishlist_items})
def delete_wish(request, id):
    product = Produk.objects.get(pk = id)
    product.delete()
    return HttpResponseRedirect(reverse('main:view_wishlist'))


# @csrf_exempt
# @require_POST
#def add_product_entry_ajax(request):
    # name = strip_tags(request.POST.get("name"))
    # description = strip_tags(request.POST.get("description"))
    # price = request.POST.get("price")
    # user = request.user

    # new_product = Product(
    #     name=name, description = description,
    #     price = price,
    #     user=user
    # )
    # new_product.save()

    # return HttpResponse(b"CREATED", status=201)