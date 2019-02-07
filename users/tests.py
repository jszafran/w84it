from django.test import TestCase
from users.models import CustomUser

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.u1 = CustomUser.objects.create_user('test_user_1', 'user_1@test.com', 'lubieplacki')
        self.u2 = CustomUser.objects.create_user('test_user_2', 'user_2@test.com', 'lubieplacki')
        self.u3 = CustomUser.objects.create_user('test_user_3', 'user_3@test.com', 'lubieplacki')
        
    def test_follow_user(self):
        self.u1.follow_user(self.u2)
        self.assertEqual(self.u2.get_my_followers()[0], self.u1)

    def test_unfollow_user(self):
        self.u1.follow_user(self.u2)
        if self.u1 in self.u2.get_my_followers():
            self.u1.unfollow_user(self.u2)
            self.assertEqual(self.u2.get_my_followers(), [])
            return
        self.assertTrue(False)

    def test_if_follow_user_method_is_idempotent(self):
        for _ in range(5):
            self.u1.follow_user(self.u2)
        self.assertEqual(len(self.u1.following.all()), 1)
        self.assertEqual(self.u1.following.all()[0], self.u2)

    def test_get_my_followers(self):
        self.u1.follow_user(self.u3)
        self.u2.follow_user(self.u3)
        self.assertEqual(len(self.u3.get_my_followers()), 2)
        self.assertTrue(self.u1 in self.u3.get_my_followers())
        self.assertTrue(self.u2 in self.u3.get_my_followers())

    def test_assymetry_of_followers_relationship(self):
        self.u1.follow_user(self.u2)
        self.assertTrue(self.u2 not in self.u1.followed_by.all())