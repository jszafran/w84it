from django.test import TestCase
from django.urls import reverse
from users.models import User
from ..models import Product
from .test_resources import datasets
from products.tests.factory import ProductsFactory
from commons.validation_messages import (FORM_URL_INVALID, FORM_PRICE_INVALID_DECIMALS,
                                         FORM_CURRENCY_INVALID, FORM_UNIQUE_USER_AND_PRODUCT_NAME_CONSTRAINT_VIOLATION,
                                         FORM_DATE_INVALID)
from django.http import Http404
from commons.useful_funcs import replace_dict_none_values_to_empty_string
from products.views import user_owns_product
import copy


class ProductTestCases(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user('testuser1', 'user_1@test.com', 'lubieplacki')
        self.user_2 = User.objects.create_user('testuser2', 'user_2@test.com', 'lubieplacki')
        self.client.login(email='user_1@test.com', password='lubieplacki')
        self.products_count = Product.objects.all().count
        self.datasets = datasets

    def test_if_valid_product_edits_are_saved_correctly(self):
        product = ProductsFactory(owner=self.user_1, name='before_update', price=50.00)
        self.assertEqual(product.name, 'before_update')
        self.assertEqual(product.price, 50.00)
        kwargs = copy.deepcopy(product.__dict__)
        kwargs.update({'name': 'after_update',
                       'price': 130.00,
                       'save_product': 'save_product'})  # save_product is required to simulate clicking 'Edit' button
        kwargs = replace_dict_none_values_to_empty_string(kwargs)  # to replace None with '' in requests
        self.client.post(reverse('edit_product', args=(product.pk,)), kwargs)
        product = Product.objects.get(pk=product.pk)
        self.assertEqual(product.name, 'after_update')
        self.assertEqual(product.price, 130.00)

    def test_that_product_cannot_be_updated_with_incorrect_values(self):
        product = ProductsFactory(owner=self.user_1, name='before_update', price=50.00, url='http://www.valid-url.com')
        self.assertEqual(product.name, 'before_update')
        self.assertEqual(product.price, 50.00)
        kwargs = copy.deepcopy(product.__dict__)
        kwargs.update({'price': 130.00130434,
                       'save_product': 'save_product',
                       'url': 'http://www invalid url',
                       'currency': '-',
                       'launch_date': '2018-99-99'})
        kwargs = replace_dict_none_values_to_empty_string(kwargs)
        response = self.client.post(reverse('edit_product', args=(product.pk,)), kwargs)
        self.assertContains(response, FORM_DATE_INVALID)
        self.assertContains(response, FORM_URL_INVALID)
        self.assertContains(response, FORM_PRICE_INVALID_DECIMALS)
        self.assertContains(response, FORM_CURRENCY_INVALID)

    def test_that_product_wont_be_saved_with_non_unique_name_same_user_products(self):
        product_1 = ProductsFactory(owner=self.user_1, name='product_1_name')
        product_2 = ProductsFactory(owner=self.user_1, name='product_2_name')
        kwargs = copy.deepcopy(product_2.__dict__)
        kwargs.update({'name': 'product_1_name', 'save_product': 'save_product'})
        kwargs = replace_dict_none_values_to_empty_string(kwargs)
        response = self.client.post(reverse('edit_product', args=(product_2.pk,)), kwargs)
        self.assertEqual(product_2.name, 'product_2_name')
        self.assertContains(response, FORM_UNIQUE_USER_AND_PRODUCT_NAME_CONSTRAINT_VIOLATION)

    def test_users_owns_product_func(self):
        product = ProductsFactory(owner=self.user_1)
        self.assertTrue(user_owns_product(self.user_1, product.pk))
        self.assertFalse(user_owns_product(self.user_2, product.pk))
        self.assertRaises(Http404, user_owns_product, self.user_1, 0)  # test with non-existing product pk

    def test_that_user_cannot_edit_product_that_doesnt_belong_to_him(self):
        product = ProductsFactory(owner=self.user_1, name='orig_name')
        self.client.logout()
        self.client.login(email='user_2@test.com', password='lubieplacki')
        kwargs = copy.deepcopy(product.__dict__)
        kwargs.update({'name': 'edited_name', 'save_product': 'save_product'})
        kwargs = replace_dict_none_values_to_empty_string(kwargs)
        response = self.client.post(reverse('edit_product', args=(product.pk,)), kwargs)
        self.assertEqual(product.name, 'orig_name')
        self.assertEqual(response.status_code, 404)
