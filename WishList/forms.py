from django import forms
from .models import Produk, WishlistItem

class WishlistItemForm(forms.ModelForm):
    produk = forms.ModelChoiceField(queryset=Produk.objects.all(), label="Select A Product")

    class Meta:
        model = WishlistItem
        fields = ['produk', 'jumlah']