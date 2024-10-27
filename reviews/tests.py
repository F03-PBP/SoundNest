from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from .models import Review

class ReviewViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(product_name='Sample Product', price=100)

    def test_add_review(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('reviews:add_review'), {
            'product': self.product.id,
            'description': 'Great product!',
            'rating': 5,
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Review.objects.filter(user=self.user, product=self.product).exists())

    def test_add_duplicate_review(self):
        self.client.login(username='testuser', password='password123')
        # Tambahkan review pertama
        self.client.post(reverse('reviews:add_review'), {
            'product': self.product.id,
            'description': 'Great product!',
            'rating': 5,
        })
        # Tambahkan review yang sama
        response = self.client.post(reverse('reviews:add_review'), {
            'product': self.product.id,
            'description': 'Another review!',
            'rating': 4,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'You have already reviewed this product.')

    def test_edit_review(self):
        self.client.login(username='testuser', password='password123')
        review = Review.objects.create(user=self.user, product=self.product, description='Good product', rating=5)

        response = self.client.post(reverse('reviews:edit_review', args=[review.id]), {
            'description': 'Updated review',
            'rating': 8,
        })
        self.assertEqual(response.status_code, 200)
        review.refresh_from_db()
        self.assertEqual(review.description, 'Updated review')
        self.assertEqual(review.rating, 8)

    def test_delete_review(self):
        self.client.login(username='testuser', password='password123')
        review = Review.objects.create(user=self.user, product=self.product, description='Will be deleted', rating=5)

        response = self.client.post(reverse('reviews:delete_review', args=[review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Review.objects.filter(id=review.id).exists())
