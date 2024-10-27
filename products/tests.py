from django.test import TestCase, Client
from django.utils import timezone
from .models import Product
import uuid

class mainTest(TestCase):
    def setUp(self):
        Product.objects.create(
            id=uuid.uuid4(),
            product_name="Test Product 1",
            price=10000,
            rating=4.5,
            reviews=10,
            created_at=timezone.now()
        )
        Product.objects.create(
            id=uuid.uuid4(),
            product_name="Test Product 2",
            price=20000,
            rating=3.5,
            reviews=5,
            created_at=timezone.now()
        )
        self.client = Client()

    def test_show_product(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        response = self.client.post('/add_product/', {
            'product_name': "New Product",
            'price': 15000,
            'rating': 4.0,
            'reviews': 7,
            'created_at': timezone.now()
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Product.objects.filter(product_name="New Product").exists())

    def test_delete_product(self):
        product = Product.objects.first()
        response = self.client.post('/delete_product/', {'id': str(product.id)}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.filter(id=product.id).exists())

    def test_edit_product(self):
        product = Product.objects.first()
        response = self.client.post('/edit_product', {
            'id': str(product.id),
            'product_name': "Updated Product",
            'price': 12000,
            'rating': 4.2,
            'reviews': 15
        })
        self.assertEqual(response.status_code, 200)
        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.product_name, "Updated Product")
        self.assertEqual(updated_product.price, 12000)
        self.assertEqual(updated_product.rating, 4.2)
        self.assertEqual(updated_product.reviews, 15)

    def test_product_details_json(self):
        product = Product.objects.first()
        response = self.client.get(f'/details/json/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('product_name', response.json())
