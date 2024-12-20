import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SoundNest.settings")

django.setup()

import random
from django.contrib.auth.models import User
from products.models import Product
from reviews.models import Review
from datetime import datetime

usernames = ["Ketua", "mike", "Elphaba", "Glinda", "aul", "sandy", "nino", "Dino", "Pino", "sulley", "dydy"]
descriptions = [
    "kualitas produk oke, audio jernih banget",
    "Suara enak, kualitas terbaik di kelasnya",
    "audio bagus, puas banget sama produk ini",
    "Bagus banget, cocok buat nonton film atau denger musik",
    "kualitas suara keren, cocok buat semua genre musik",
    "Produk yang sangat memuaskan, audionya jernih",
    "gak nyesel beli produk ini, audio mantap!",
    "suaranya oke, bassnya juga enak",
    "Produk ini bagus banget, audio jernih tanpa distorsi",
    "sangat puas, suara jelas dan kuat",
    "Audio bersih banget, cocok buat gaming atau musik",
    "produk berkualitas, suara jernih dan gak pecah",
    "Suara sangat jelas dan detil, recomended deh",
    "suara bassnya juga mantap, gak mengecewakan",
    "Kualitasnya pas banget, suara jernih dan bassnya terasa",
    "audio keren, gak ada suara yang mengganggu",
    "Suara jelas banget, terutama untuk vokal",
    "sangat nyaman dipakai, audio luar biasa",
    "Suara stereo-nya enak, produk ini worth it",
    "dengarnya enak, gak ada noise atau gangguan",
    "Suara mantap banget, bassnya juga terasa",
    "produk ini bagus, gak nyesel beli",
    "Kualitas suara jernih banget, bass mantap",
    "audio mantap, jernih, detail banget!",
    "Puas banget, suara sangat clean dan bassnya oke",
    "produk bagus, suara jernih dan bassnya kencang",
    "Kualitas audio oke banget, bassnya dalam",
    "puas banget dengan kualitas suara yang jernih",
    "audio enak banget, recommended buat denger musik",
    "suara detail banget, gak ada distorsi",
    "suara jernih, bassnya terasa banget, top deh!",
    "Audio-nya clear banget bass-nya deep cocok buat chill vibes",
    "Suaranya crispy abis bener-bener satisfying buat daily use",
    "Bassnya boomy treble-nya smooth pokoknya top banget",
    "Denger musik pake ini feel-nya kayak di studio clear banget",
    "Sound-nya rich banget all genre masuk best buy banget deh",
    "Vokalnya lifelike detail banget bener-bener next level",
    "Kualitasnya superb clarity-nya bikin setiap beat kerasa banget",
    "Bener-bener balance nggak over bass tapi tetep powerful"
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
        num_reviews = random.randint(3, 7)

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