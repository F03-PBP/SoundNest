from django.db import models
from django.contrib.auth.models import User
import uuid

class Reviews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    rating = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        # Rating ada di antara 1-5
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating harus antara 1 dan 5")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
