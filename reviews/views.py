from django.shortcuts import render
from .models import Review

def show_reviews(request):
    return render(request, 'main.html')

def review_list(request):
    reviews_data = [
        {"user_name": "Alex K.", "user_initials": "AK", "user_role": "Senior Analyst", "rating": 5, "date": "2024-01-20", "text": "Working at Sam.AI..."},
        {"user_name": "Emily R.", "user_initials": "ER", "user_role": "Front-End Engineer", "rating": 4, "date": "2023-11-13", "text": "Sam.AI is not just..."},
        # Tambahkan lebih banyak data review di sini
    ]
    
    # Tambahkan logika untuk menghitung bintang di backend
    for review in reviews_data:
        review['stars'] = list(range(review['rating']))  # Bintang penuh
        review['empty_stars'] = list(range(5 - review['rating']))  # Bintang kosong
    
    context = {
        'reviews': reviews_data
    }
    return render(request, 'main.html', context)
    # reviews = Reviews.objects.all()
    # return render(request, 'review_list.html', {'reviews': reviews})