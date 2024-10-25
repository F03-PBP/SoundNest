from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
class Produk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2)

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
