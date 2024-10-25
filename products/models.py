from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    price = models.IntegerField()
    rating = models.FloatField(default=0.0)
    reviews = models.IntegerField(default=0)

    def update_rating(self):
        reviews = self.review_set.all()
        total_reviews = reviews.count()
        if total_reviews > 0:
            average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.rating = average_rating
            self.reviews = total_reviews
            self.save()