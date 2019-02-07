from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followed_by = models.ManyToManyField("self", symmetrical=False, related_name="following")
    email = models.EmailField(blank=False, unique=True)

    def __str__(self):
        return self.email
    
    @classmethod
    def get_user_by_email(cls, email):
        try:
            return User.objects.filter(email=email)[0]
        except:
            return None

    def get_my_followers(self):
        return [user for user in self.followed_by.all()]

    def follow_user(self, user_email):
        user_to_follow = User.get_user_by_email(user_email)
        if user_to_follow:
            user_to_follow.followed_by.add(self)
            user_to_follow.save()
            print(f"User '{self.email}' followed user '{user_email}' successfully.")

    def unfollow_user(self, email):
        user_to_unfollow = User.get_user_by_email(email=email)
        if user_to_unfollow:
            user_to_unfollow.followed_by.remove(self)

    def get_users_i_am_following(self):
        return self.following.all()


