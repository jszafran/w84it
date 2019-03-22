from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from ..models import Product
from .test_resources import datasets
from products.tests.factory import ProductsFactory


class ProductTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser1', 'user_1@test.com', 'lubieplacki')
        self.client.login(email='user_1@test.com', password='lubieplacki')
        self.products_count = Product.objects.all().count
        self.datasets = datasets

    def test_if_no_orphan_product_is_left_after_owner_deletion(self):
        self.assertEqual(self.products_count(), 0)
        product = ProductsFactory(owner=self.user)
        self.assertEquals(self.products_count(), 1)
        owner = User.objects.get(username='testuser1')
        self.assertEqual(owner.pk, Product.objects.get(pk=product.pk).owner_id)
        owner.delete()
        self.assertFalse(User.objects.all())
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())

    def test_if_existing_product_is_deleted(self):
        self.assertEquals(self.products_count(), 0)
        product = ProductsFactory(owner=self.user)
        self.assertEquals(self.products_count(), 1)
        self.client.post(reverse('delete_product', args=(product.pk,)))
        self.assertEqual(self.products_count(), 0)
