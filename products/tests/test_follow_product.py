from django.test import TestCase
from products.tests.factory import ProductsFactory
from users.models import User


class ProductTestCases(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user('testuser1', 'user_1@test.com', 'lubieplacki')
        self.user_2 = User.objects.create_user('testuser2', 'user_2@test.com', 'lubieplacki')
        self.user_3 = User.objects.create_user('testuser3', 'user_3@test.com', 'lubieplacki')
        self.prod_1 = ProductsFactory(owner=self.user_1, name='product_1', price=50.00)
        self.prod_2 = ProductsFactory(owner=self.user_1, name='product_2', price=50.00)

    def test_adding_new_product_follower(self):
        self.assertEqual(self.prod_1.followed_by.all().count(), 0)
        self.assertEqual(self.prod_1.followers_num, 0)
        self.prod_1.add_follower(self.user_2)
        self.prod_1.add_follower(self.user_3)
        self.assertEqual(self.prod_1.followed_by.all().count(), 2)
        self.assertIn(self.user_2, self.prod_1.followed_by.all())
        self.assertIn(self.user_3, self.prod_1.followed_by.all())
        self.assertEqual(self.prod_1.followers_num, 2)

    def test_removing_product_follower(self):
        self.assertEqual(self.prod_1.followed_by.all().count(), 0)
        self.assertEqual(self.prod_1.followers_num, 0)
        self.prod_1.add_follower(self.user_2)
        self.prod_1.add_follower(self.user_3)
        self.assertEqual(self.prod_1.followed_by.all().count(), 2)
        self.assertEqual(self.prod_1.followers_num, 2)
        self.prod_1.remove_follower(self.user_2)
        self.assertEqual(self.prod_1.followed_by.all().count(), 1)
        self.assertEqual(self.prod_1.followers_num, 1)
        self.assertIn(self.user_3, self.prod_1.followed_by.all())
