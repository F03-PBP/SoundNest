from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import WishlistItem

User = get_user_model()

class WishlistItemModelTest(TestCase):

    def setUp(self):
        # Membuat pengguna untuk pengujian
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_wishlist_item_creation(self):
        # Membuat item wishlist
        wishlist_item = WishlistItem.objects.create(
            user=self.user,
            produk=None,  # Bisa diset ke None jika tidak ada product
            jumlah=2,
            price=100,
            nama_produk="Test Product"
        )
        
        # Memastikan item wishlist dibuat dengan benar
        self.assertEqual(wishlist_item.user, self.user)
        self.assertEqual(wishlist_item.jumlah, 2)
        self.assertEqual(wishlist_item.price, 100)
        self.assertEqual(wishlist_item.nama_produk, "Test Product")

    def test_wishlist_item_str(self):
        # Memastikan representasi string item wishlist
        wishlist_item = WishlistItem.objects.create(
            user=self.user,
            produk=None,  # Bisa diset ke None jika tidak ada product
            jumlah=1,
            price=50,
            nama_produk="Sample Product"
        )
        self.assertEqual(str(wishlist_item), "Sample Product")  # Pastikan ini sesuai dengan __str__() yang diharapkan

    def test_wishlist_item_default_jumlah(self):
        # Memastikan jumlah default
        wishlist_item = WishlistItem.objects.create(
            user=self.user,
            produk=None,
            price=150,
            nama_produk="Default Quantity Product"
        )
        self.assertEqual(wishlist_item.jumlah, 1)  # Pastikan default jumlah adalah 1
