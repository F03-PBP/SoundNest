from django import forms
from reviews.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'description', 'rating']

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        user = self.initial.get('user')

        if Review.objects.filter(user=user, product=product).exists():
            raise forms.ValidationError('You have already reviewed this product.')
        
        return cleaned_data