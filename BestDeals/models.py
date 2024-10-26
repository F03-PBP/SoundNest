from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product
# Sale Model
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    sale_end_time = models.DateTimeField()
    

    @property
    def discounted_price(self):
        return self.product.price * (1 - (self.discount_percentage / 100))
    
    @property
    def get_time_remaining(self):
        """
        Returns the remaining time as a formatted string.
        """
        remaining = self.sale_end_time - timezone.localtime()
        
        if remaining.total_seconds() <= 0:
            return "Sale ended"
            
        days = remaining.days
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        
        if days > 0:
            return f"{days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    def is_sale_active(self):
        """
        Checks if the sale is still active.
        """
        return timezone.localtime() < self.sale_end_time

    def __str__(self):
        return f'{self.product.name} - {self.discount_percentage}% off'

# # User Interaction Model (optional)
# class UserInteraction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     reminder_time = models.DateTimeField(null=True, blank=True)
#     notified = models.BooleanField(default=False)

#     def __str__(self):
#         return f'{self.user.username} - {self.product.name} interaction'


