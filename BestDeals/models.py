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
        seconds = remaining.seconds
        
        if days > 0:
            return f"{days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return f"{seconds}s" #kalo sisa <1 menit, bakal muncul detik

    def is_sale_active(self):
        """
        Checks if the sale is still active.
        """
        return timezone.localtime() < self.sale_end_time
