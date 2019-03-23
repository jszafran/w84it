from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from ..models import Product
from .test_resources import datasets
from products.tests.factory import ProductsFactory


class ProductTestCases(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user('testuser1', 'user_1@test.com', 'lubieplacki')
        self.user_2 = User.objects.create_user('testuser2', 'user_2@test.com', 'lubieplacki')
        self.client.login(email='user_1@test.com', password='lubieplacki')
        self.products_count = Product.objects.all().count
        self.datasets = datasets

    def test_if_no_orphan_product_is_left_after_owner_deletion(self):
        self.assertEqual(self.products_count(), 0)
        product = ProductsFactory(owner=self.user_1)
        product_pk = product.pk
        self.assertEquals(self.products_count(), 1)
        owner = User.objects.get(username='testuser1')
        owner_pk = owner.pk
        self.assertEqual(owner.pk, Product.objects.get(pk=product.pk).owner_id)
        owner.delete()
        self.assertRaises(User.DoesNotExist, User.objects.get, pk=owner_pk)
        self.assertRaises(Product.DoesNotExist, Product.objects.get, pk=product_pk)

    def test_if_existing_product_is_deleted(self):
        self.assertEquals(self.products_count(), 0)
        product = ProductsFactory(owner=self.user_1)
        self.assertEquals(self.products_count(), 1)
        self.client.post(reverse('delete_product', args=(product.pk,)))
        self.assertEqual(self.products_count(), 0)

    def test_that_user_not_owning_the_product_cannot_delete_it(self):
        product = ProductsFactory(owner=self.user_1)
        self.client.logout()
        self.client.login(email='user_2@test.com', password='lubieplacki')
        response = self.client.post(reverse('delete_product', args=(product.pk,)))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Product.objects.filter(pk=product.pk).exists())

    def test_that_delete_request_made_after_successful_product_deletion_raises_404(self):
        product = ProductsFactory(owner=self.user_1)
        product_pk = product.pk
        self.client.post(reverse('delete_product', args=(product.pk,)))
        self.assertRaises(Product.DoesNotExist, Product.objects.get, pk=product_pk)
        response = self.client.post(reverse('delete_product', args=(product_pk,)))
        self.assertEqual(response.status_code, 404)
