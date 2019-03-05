from django.test import TestCase, Client
from users.models import User
import datetime
from django.urls import reverse

class UserTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('testuser1', 'user_1@test.com', 'lubieplacki')
        self.u2 = User.objects.create_user('testuser2', 'user_2@test.com', 'lubieplacki')
        self.u3 = User.objects.create_user('testuser3', 'user_3@test.com', 'lubieplacki')
        self.client = Client()
        self.grace_period_days = 7 # number of days for which user can revert his decision about account deletion

    def test_follow_user(self):
        self.u1.follow_user(self.u2)
        self.assertEqual(self.u2.get_followers().first(), self.u1)

    def test_unfollow_user(self):
        self.u1.follow_user(self.u2)
        self.assertEqual(len(self.u2.get_followers()), 1)
        self.u1.unfollow_user(self.u2)
        self.assertEqual(len(self.u2.get_followers()), 0)

    def test_if_follow_user_method_is_idempotent(self):
        for _ in range(5):
            self.u1.follow_user(self.u2)
        self.assertEqual(len(self.u1.following.all()), 1)
        self.assertEqual(self.u1.following.all().first(), self.u2)

    def test_get_followed(self):
        self.u1.follow_user(self.u3)
        self.u2.follow_user(self.u3)
        self.assertEqual(len(self.u3.get_followers()), 2)
        self.assertTrue(self.u1 in self.u3.get_followers())
        self.assertTrue(self.u2 in self.u3.get_followers())

    def test_asymmetry_of_followers_relationship(self):
        self.u1.follow_user(self.u2)
        self.assertTrue(self.u2 not in self.u1.followed_by.all())

    def test_changing_deletion_flag_after_confirming(self):
        self.client.login(email='user_1@test.com', password='lubieplacki')
        user = User.objects.get(email='user_1@test.com')
        self.assertFalse(user.to_be_deleted)
        self.client.post(reverse('delete_user'))
        user.refresh_from_db()
        self.assertTrue(user.to_be_deleted)

    def test_cancellation_of_user_deletion(self):
        self.client.login(email='user_1@test.com', password='lubieplacki')
        user = User.objects.get(email='user_1@test.com')
        self.assertFalse(user.to_be_deleted)
        self.assertIsNone(user.deletion_date)
        self.client.post(reverse('delete_user'))
        user.refresh_from_db()
        self.assertTrue(user.to_be_deleted)
        self.assertTrue(user.deletion_date == (datetime.date.today() + datetime.timedelta(days=self.grace_period_days)))
        self.client.post(reverse('revert_user_deletion'))
        user.refresh_from_db()
        self.assertFalse(user.to_be_deleted)
        self.assertIsNone(user.deletion_date)
