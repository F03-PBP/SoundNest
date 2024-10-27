from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render, get_object_or_404
from reviews.models import Review
from reviews.forms import ReviewForm
from django.core import serializers
import json

def show_reviews(request):
    reviews = Review.objects.all()
    reviews_data = []
    for review in reviews:
        stars = range(review.rating)  # Bintang penuh
        empty_stars = range(10 - review.rating)  # Bintang kosong
        reviews_data.append({ # Ambil dari user
            'user_name': review.user.username,
            'user_initials': review.user.username[:2].upper(),
            'date': review.created_at,
            'product_price': review.product.price,
            'rating': review.rating,
            'stars': stars,
            'empty_stars': empty_stars,
            'text': review.description,
            'id': review.id,
            'user_id': review.user.id,
        })

    return render(request, 'reviews.html', {'reviews': reviews_data, 'user': request.user})

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            user = request.user
            
            # Cek apakah user sudah mereview produk ini
            existing_review = Review.objects.filter(product=product, user=user).exists()
            if existing_review:
                return JsonResponse({
                    'success': False,
                    'message': 'You have already reviewed this product.'
                }, status=400)
            
            # Jika belum ada review, simpan review baru
            review = form.save(commit=False)
            review.user = user
            review.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Review successfully added'
            }, status=201)
        
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)

def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Cek apakah user adalah pemilik review
    if review.user != request.user:
        return JsonResponse({
            'success': False,
            'message': 'You do not have permission to edit this review.'
        }, status=403)

    if request.method == 'GET':
        # Mengirimkan data review untuk diedit (menampilkan modal edit)
        return JsonResponse({
            'success': True,
            'review': {
                'description': review.description,  # Menggunakan 'description' sesuai model
                'rating': review.rating,
                'product': review.product.id,
            }
        })

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)  # Ambil data dari request body sebagai JSON
            new_description = data.get('description')
            new_rating = data.get('rating')

            if not new_description or not new_rating:
                return JsonResponse({'success': False, 'message': 'Please provide both description and rating.'}, status=400)

            # Update review
            review.description = new_description  # Gunakan 'description' untuk teks review
            review.rating = int(new_rating)
            review.save()

            return JsonResponse({'success': True, 'message': 'Review updated successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user and not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'message': 'You do not have permission to delete this review.'
        }, status=403)

    review.delete()
    return JsonResponse({
        'success': True,
        'message': 'Review successfully deleted'
    }, status=200)

def review_list(request):
    reviews = Review.objects.all()
    data = serializers.serialize('json', reviews)
    return JsonResponse(data, safe=False)

