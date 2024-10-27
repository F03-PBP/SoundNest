from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from products.models import Product
from .models import Sale
from datetime import timedelta
import json


class SaleModelTest(TestCase):
    def setUp(self):
        # Create a Product instance
        self.product = Product.objects.create(
            product_name="Test Product",
            price=100.00,
            rating=4.5,
            reviews=10
        )
        
        # Create Sale instance
        self.sale = Sale.objects.create(
            product=self.product,
            discount_percentage=20.0,
            sale_end_time=timezone.now() + timedelta(days=1)
        )

    def test_discounted_price(self):
        """Test the discounted price calculation."""
        self.assertAlmostEqual(self.sale.discounted_price, 80.0)

    def test_get_time_remaining(self):
        """Test if the remaining time is calculated and formatted correctly."""
        self.assertIn("d", self.sale.get_time_remaining)

    def test_is_sale_active(self):
        """Test if sale is active based on end time."""
        self.assertTrue(self.sale.is_sale_active())
        self.sale.sale_end_time = timezone.now() - timedelta(days=1)
        self.sale.save()
        self.assertFalse(self.sale.is_sale_active())


class SaleViewTest(TestCase):
    def setUp(self):
        # Set up client, user, product, and sale data
        self.client = Client()
        self.user = User.objects.create_user(username="admin", password="password", is_staff=True)
        
        self.product = Product.objects.create(
            product_name="Test Product",
            price=100.00,
            rating=4.5,
            reviews=10
        )
        
        self.sale = Sale.objects.create(
            product=self.product,
            discount_percentage=20.0,
            sale_end_time=timezone.now() + timedelta(days=1)
        )

    def test_best_deals_view(self):
        """Test the best_deals view rendering with context."""
        response = self.client.get(reverse('best_deals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bestdeals.html")
        self.assertIn('initial_data', response.context)

    def test_show_json(self):
        """Test the JSON response from show_json view."""
        response = self.client.get(reverse('show_json'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('sales', data)

    def test_add_to_deals(self):
        """Test adding a product to deals with JSON POST request."""
        self.client.login(username="admin", password="password")
        data = {
            'product_id': self.product.id,
            'discount': 10,
            'end_date': (timezone.now() + timedelta(days=2)).isoformat()
        }
        response = self.client.post(
            reverse('add_to_deals'),
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Sale.objects.filter(product=self.product).exists())

    def test_edit_deals(self):
        """Test editing a deal with JSON PUT request."""
        self.client.login(username="admin", password="password")
        data = {
            'discount': 15,
            'end_date': (timezone.now() + timedelta(days=3)).isoformat()
        }
        response = self.client.put(
            reverse('edit_deals', args=[self.product.id]),
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.sale.refresh_from_db()
        self.assertEqual(self.sale.discount_percentage, 15)

    def test_delete_deals(self):
        """Test deleting a deal with JSON DELETE request."""
        self.client.login(username="admin", password="password")
        response = self.client.delete(
            reverse('delete_deals', args=[self.product.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Sale.objects.filter(product=self.product).exists())
