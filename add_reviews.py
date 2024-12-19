import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SoundNest.settings")

django.setup()

import random
from django.contrib.auth.models import User
from products.models import Product
from reviews.models import Review
from datetime import datetime

usernames = ["Ketua", "Mike", "Elphaba", "Glinda", "Aul", "Sandy", "Nino", "Dino", "Pino", "Sulley"]
descriptions = [
    "Kualitas produk oke, audio jernih banget.",
    "Suara enak, kualitas terbaik di kelasnya.",
    "Audio bagus, puas banget sama produk ini.",
    "Bagus banget, cocok buat nonton film atau denger musik.",
    "Kualitas suara keren, cocok buat semua genre musik.",
    "Produk yang sangat memuaskan, audionya jernih.",
    "Gak nyesel beli produk ini, audio mantap!",
    "Suaranya oke, bassnya juga enak.",
    "Produk ini bagus banget, audio jernih tanpa distorsi.",
    "Sangat puas, suara jelas dan kuat.",
    "Audio bersih banget, cocok buat gaming atau musik.",
    "Produk berkualitas, suara jernih dan gak pecah.",
    "Suara sangat jelas dan detil, recomended deh.",
    "Suara bassnya juga mantap, gak mengecewakan.",
    "Kualitasnya pas banget, suara jernih dan bassnya terasa.",
    "Audio keren, gak ada suara yang mengganggu.",
    "Suara jelas banget, terutama untuk vokal.",
    "Sangat nyaman dipakai, audio luar biasa.",
    "Suara stereo-nya enak, produk ini worth it.",
    "Dengarnya enak, gak ada noise atau gangguan.",
    "Suara mantap banget, bassnya juga terasa.",
    "Produk ini bagus, gak nyesel beli.",
    "Kualitas suara jernih banget, bass mantap.",
    "Audio mantap, jernih, detail banget!",
    "Puas banget, suara sangat clean dan bassnya oke.",
    "Produk bagus, suara jernih dan bassnya kencang.",
    "Kualitas audio oke banget, bassnya dalam.",
    "Puas banget dengan kualitas suara yang jernih.",
    "Audio enak banget, recommended buat denger musik.",
    "Suara detail banget, gak ada distorsi.",
    "Suara jernih, bassnya terasa banget, top deh!",
]

def create_users():
    users = []
    for username in usernames:
        user = User.objects.create_user(username=username, password="racuntikus")
        users.append(user)
    return users

def add_reviews_to_products():
    products = Product.objects.all()
    users = create_users()
    
    for product in products:
        num_reviews = random.randint(2, 3)

        for _ in range(num_reviews):
            user = random.choice(users)
            rating = random.randint(7, 10)
            description = random.choice(descriptions)

            if not Review.objects.filter(user=user, product=product).exists():
                review = Review(
                    user=user,
                    product=product,
                    rating=rating,
                    description=description,
                    created_at=datetime.now(),
                    last_update=datetime.now()
                )
                review.save()

add_reviews_to_products()
print("Review data has been added successfully!")