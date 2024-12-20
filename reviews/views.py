from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from reviews.models import Review
from reviews.forms import ReviewForm
import json
from django.views.decorators.csrf import csrf_exempt

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.utils.timezone import localtime

def show_reviews(request, product_id):
    reviews_response = review_list(request)
    all_reviews = json.loads(reviews_response.content)  # Parsing JSON response menjadi list

    # Filter berdasarkan product_id
    filtered_reviews = []
    for review in all_reviews:
        if str(review['product_id']) == str(product_id):
            filtered_reviews.append(review)
 
    return filtered_reviews

@csrf_exempt
def add_review(request):
    try:
        user = authenticate_user(request)
    except AuthenticationFailed as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=401)
    
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            rating = data.get('rating')
            description = data.get('description')
            product_id = data.get('product')

            if not rating or not description or not product_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Please provide all required fields: rating, description, and product.'
                }, status=400) 

            # Cek apakah user sudah mereview produk
            if Review.objects.filter(product_id=product_id, user=user).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'You have already reviewed this product.'
                }, status=400)

            # Simpan review
            review = Review.objects.create(
                rating=rating,
                description=description,
                product_id=product_id,
                user=user,
            )
            return JsonResponse({
                'success': True,
                'message': 'Review added successfully.',
                'review_id': review.id,
            }, status=201)

        else:
            form = ReviewForm(request.POST)
            if form.is_valid():
                product = form.cleaned_data['product']
                
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

@csrf_exempt
def edit_review(request, review_id):
    try:
        user = authenticate_user(request)
    except AuthenticationFailed as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=401)
    
    review = get_object_or_404(Review, id=review_id)

    # Cek apakah user adalah pemilik review
    if review.user != user:
        return JsonResponse({
            'success': False,
            'message': 'You do not have permission to edit this review.'
        }, status=403)

    if request.method == 'GET':
        # Mengirimkan data review untuk diedit (menampilkan modal edit)
        return JsonResponse({
            'success': True,
            'review': {
                'description': review.description,
                'rating': review.rating,
                'product': review.product.id,
            }
        })

    elif request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        new_rating = data.get('rating')
        new_description = data.get('description')

        if not new_rating or not new_description:
            return JsonResponse({
                'success': False,
                'message': 'Please provide both rating and description.'
            }, status=400)

        review.rating = int(new_rating)
        review.description = new_description
        review.save()

        return JsonResponse({
            'success': True,
            'message': 'Review updated successfully.',
            'review_id': review.id,
            'last_update': review.last_update,
        }, status=200)
    
@csrf_exempt
def delete_review(request, review_id):
    try:
        user = authenticate_user(request)
    except AuthenticationFailed as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=401)
    
    review = get_object_or_404(Review, id=review_id)

    if review.user != user and not user.is_staff:
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
    reviews = Review.objects.all()  # Optimalkan query
    reviews_data = []

    for review in reviews:
        stars = list(range(review.rating))  # Bintang penuh
        empty_stars = list(range(10 - review.rating))  # Bintang kosong

        # Tentukan waktu update
        if review.created_at == review.last_update:
            update_time = localtime(review.created_at)
        else:
            update_time = localtime(review.last_update)

        reviews_data.append({
            'id': str(review.id),
            'user_id': review.user.id,
            'user_name': review.user.username,
            'user_initials': review.user.username[:2].upper(),
            'product_id': review.product.id,
            'product_name': review.product.product_name,
            'product_price': review.product.price,
            'rating': review.rating,
            'stars': stars,
            'empty_stars': empty_stars,
            'description': review.description,
            'updated_at': update_time.strftime('%Y-%m-%d %H:%M'),
        })

    return JsonResponse(reviews_data, safe=False)

@csrf_exempt
def show_reviews_flutter(request):
    # Ambil parameter query
    product_id = request.GET.get('product_id')
    by_user = request.GET.get('by_user', 'false').lower() == 'true'

    reviews_response = review_list(request)
    all_reviews = json.loads(reviews_response.content)

    if by_user:
        try:
            user = authenticate_user(request)
        except AuthenticationFailed as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=401)

        filtered_reviews = [review for review in all_reviews if review['user_name'] == user.username]

    elif product_id:
        filtered_reviews = [review for review in all_reviews if str(review['product_id']) == str(product_id)]

    else:  # Tidak ada parameter valid
        return JsonResponse({
            'success': False,
            'message': 'Please provide either product_id or by_user=true.'
        }, status=400)
    
    return JsonResponse(filtered_reviews, safe=False)

def authenticate_user(request):
    if 'Authorization' in request.headers:
        token_key = request.headers.get('Authorization').split(' ')[1] 
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
            request.user = user 
            return user
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

    elif request.user.is_authenticated:
        return request.user

    else:
        raise AuthenticationFailed('You must be logged in.')