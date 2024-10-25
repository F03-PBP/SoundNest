from django import forms
from WishList.models import WishlistItem
from products.models import Product as Produk

class WishlistItemForm(forms.ModelForm):
    produk = forms.ModelChoiceField(queryset=Produk.objects.all(), label="Select A Product")

    class Meta:
        model = WishlistItem
        fields = ['produk', 'jumlah']