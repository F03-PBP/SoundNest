from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produk = models.ForeignKey(Product, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
    price = models.IntegerField()
    nama_produk = models.CharField(max_length=255)