from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal
import json
from datetime import timedelta
from .models import Sale, Product
import uuid
from django.utils import timezone

class SaleModelTests(TestCase):
    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            id=uuid.uuid4(),
            product_name="Test Product",
            price=Decimal('100.00'),
            rating=4.5,
            reviews=10,
            created_at = timezone.localtime()
        )
        
        # Create a test sale
        self.sale = Sale.objects.create(
            product=self.product,
            discount_percentage=Decimal('20.00'),
            sale_end_time=timezone.localtime() + timedelta(days=1)
        )

    def test_discounted_price(self):
        """Test the discounted_price property"""
        expected_price = Decimal('80.00')  # 100 - 20%
        self.assertEqual(self.sale.discounted_price, expected_price)

    def test_get_time_remaining_days(self):
        """Test time remaining when more than a day is left"""
        self.sale.sale_end_time = timezone.localtime() + timedelta(days=2, hours=3)
        self.assertTrue("2d" in self.sale.get_time_remaining)

    def test_get_time_remaining_hours(self):
        """Test time remaining when less than a day is left"""
        self.sale.sale_end_time = timezone.localtime() + timedelta(hours=5, minutes=30)
        self.assertTrue("5h" in self.sale.get_time_remaining)

    def test_get_time_remaining_minutes(self):
        """Test time remaining when less than an hour is left"""
        self.sale.sale_end_time = timezone.localtime() + timedelta(minutes=45)
        self.assertTrue("45m" in self.sale.get_time_remaining)

    def test_is_sale_active(self):
        """Test if sale is active"""
        self.assertTrue(self.sale.is_sale_active())
        
        # Test expired sale
        self.sale.sale_end_time = timezone.localtime() - timedelta(days=1)
        self.assertFalse(self.sale.is_sale_active())

class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            id=uuid.uuid4(),
            product_name="Test Product",
            price=Decimal('100.00'),
            rating=4.5,
            reviews=10,
            created_at = timezone.localtime()
        )
        self.sale = Sale.objects.create(
            product=self.product,
            discount_percentage=Decimal('20.00'),
            sale_end_time=timezone.localtime() + timedelta(days=1)
        )
        
        # Create staff user
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpass123',
            is_staff=True
        )

    def test_best_deals_view(self):
        """Test the best deals view"""
        response = self.client.get(reverse('best_deals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestdeals.html')

    def test_show_json_view(self):
        """Test the JSON data endpoint"""
        response = self.client.get(reverse('show_json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('sales', data)
        self.assertIn('top_picks', data)
        self.assertIn('top_picks_guest', data)

    def test_add_to_deals(self):
        """Test adding a new deal"""
        new_product = Product.objects.create(
            id=uuid.uuid4(),
            product_name="New Product",
            price=Decimal('150.00'),
            rating=4.0,
            reviews=5,
            created_at = timezone.localtime()
        )
        
        data = {
            'product_id': str(new_product.id),
            'discount': 25.00,
            'end_date': (timezone.localtime() + timedelta(days=7)).isoformat()
        }
        
        response = self.client.post(
            reverse('add_to_deals'),
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Sale.objects.filter(product=new_product).exists())

    def test_edit_deals(self):
        """Test editing an existing deal"""
        data = {
            'discount': 30.00,
            'end_date': (timezone.localtime() + timedelta(days=14)).isoformat()
        }
        
        response = self.client.put(
            reverse('edit_deals', args=[self.product.id]),
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        updated_sale = Sale.objects.get(product=self.product)
        self.assertEqual(float(updated_sale.discount_percentage), 30.00)

    def test_delete_deals(self):
        """Test deleting a deal"""
        response = self.client.delete(
            reverse('delete_deals', args=[self.product.id])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Sale.objects.filter(product=self.product).exists())

class URLTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product_id = uuid.uuid4()

    def test_url_best_deals(self):
        """Test best deals URL"""
        url = reverse('best_deals')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_add_to_deals(self):
        """Test add to deals URL"""
        url = reverse('add_to_deals')
        self.assertEqual(url, '/add-to-deals/')

    def test_url_edit_deals(self):
        """Test edit deals URL"""
        url = reverse('edit_deals', args=[self.product_id])
        self.assertEqual(url, f'/edit-deals/{self.product_id}/')

    def test_url_delete_deals(self):
        """Test delete deals URL"""
        url = reverse('delete_deals', args=[self.product_id])
        self.assertEqual(url, f'/delete-deals/{self.product_id}/')

    def test_url_show_json(self):
        """Test show JSON URL"""
        url = reverse('show_json')
        self.assertEqual(url, '/json/')