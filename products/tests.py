from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from .models import Product
from .test_resources import datasets
from commons.validation_messages import (FORM_URL_INVALID, FORM_PRICE_INVALID_DECIMALS,
                                         FORM_PRICE_INVALID_DIGITS_AMOUNT, FORM_CURRENCY_INVALID,
                                         FORM_UNIQUE_USER_AND_PRODUCT_NAME_CONSTRAINT_VIOLATION, FORM_DATE_INVALID)


class ProductTestCases(TestCase):
    def setUp(self):
        User.objects.create_user('testuser1', 'user_1@test.com', 'lubieplacki')
        self.client = Client()
        self.client.login(email='user_1@test.com', password='lubieplacki')
        self.products_count = Product.objects.all().count
        self.datasets = datasets

    def test_if_valid_product_is_correctly_added_to_database(self):
        self.assertEqual(self.products_count(), 0)
        self.client.post(reverse('add_product'), datasets.get('full_valid_data'))
        self.assertEqual(self.products_count(), 1)

    def test_if_same_product_will_not_be_added_multiple_times(self):
        self.assertEqual(self.products_count(), 0)
        self.client.post(reverse('add_product'), datasets.get('full_valid_data'))
        self.assertEqual(self.products_count(), 1)
        for _ in range(10):
            response = self.client.post(reverse('add_product'), datasets.get('full_valid_data'))
        self.assertContains(response, FORM_UNIQUE_USER_AND_PRODUCT_NAME_CONSTRAINT_VIOLATION)
        self.assertEqual(self.products_count(), 1)

    def test_if_product_with_invalid_url_wont_be_created(self):
        self.assertEqual(self.products_count(), 0)
        response = self.client.post(reverse('add_product'), datasets.get('invalid_data_url'))
        self.assertContains(response, FORM_URL_INVALID)
        self.assertEqual(self.products_count(), 0)

    def test_if_product_with_invalid_price_wont_be_created(self):
        self.assertEqual(self.products_count(), 0)
        response = self.client.post(reverse('add_product'), datasets.get('invalid_data_price_too_many_decimals'))
        self.assertContains(response, FORM_PRICE_INVALID_DECIMALS)
        response = self.client.post(reverse('add_product'), datasets.get('invalid_data_price_too_many_digits'))
        self.assertContains(response, FORM_PRICE_INVALID_DIGITS_AMOUNT)
        self.assertEqual(self.products_count(), 0)

    def test_if_product_containing_valid_price_but_no_currency_wont_be_created(self):
        self.assertEqual(self.products_count(), 0)
        response = self.client.post(reverse('add_product'), datasets.get('invalid_data_price_with_no_currency'))
        self.assertContains(response, FORM_CURRENCY_INVALID)
        self.assertEqual(self.products_count(), 0)

    def test_if_product_with_invalid_dates_wont_be_created(self):
        self.assertEqual(self.products_count(), 0)
        response = self.client.post(reverse('add_product'), datasets.get('invalid_data_wrong_dates'))
        self.assertContains(response, FORM_DATE_INVALID)
        self.assertEqual(self.products_count(), 0)

    def test_if_no_orphan_product_is_left_after_owner_deletion(self):
        self.assertEqual(self.products_count(), 0)
        self.client.post(reverse('add_product'), datasets.get('full_valid_data'))
        self.assertEquals(self.products_count(), 1)
        owner = User.objects.get(username='testuser1')
        self.assertEqual(owner.pk, Product.objects.get(pk=1).owner_id)
        owner.delete()
        self.assertFalse(User.objects.filter(pk=1).exists())
        self.assertFalse(Product.objects.filter(pk=1).exists())
