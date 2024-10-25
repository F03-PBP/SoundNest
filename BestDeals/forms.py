from django import forms
from .models import Product

class AddToDealsForm(forms.Form):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(sales__isnull=True),  # Only show products not in any deals
        widget=forms.CheckboxSelectMultiple,  # Allows selecting multiple products using checkboxes
        label="Select products to add to deals"
    )
