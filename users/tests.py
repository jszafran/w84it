from django.test import TestCase
from users.models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('testuser1', 'user_1@test.com', 'lubieplack3')
        self.u2 = User.objects.create_user('testuser2', 'user_2@test.com', 'lubieplacki')
        self.u3 = User.objects.create_user('testuser3', 'user_3@test.com', 'lubieplacki')

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
