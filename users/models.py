from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    followed_by = models.ManyToManyField('self', symmetrical=False)
    email = models.EmailField(blank=False, unique=True)

    def __str__(self):
        return self.email

    def get_my_followers(self):
        return [user for user in self.followed_by.all()]

    def follow_user(self, user_email):
        user_to_follow = None
        try:
            user_to_follow = CustomUser.objects.filter(email=user_email)[0]
        except IndexError:
            print(f"Action failed!\nThere's no user with '{user_email}' email address.")
        if user_to_follow:
            user_to_follow.followed_by.add(self)
            user_to_follow.save()
            print(f"User '{self.email}' followed user '{user_email}' successfully.")

    def get_users_i_am_following(self):
        pass

    def unfollow_user(self, user_email):
        pass
