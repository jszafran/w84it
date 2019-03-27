from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import CustomASCIIUsernameValidator


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(help_text='Required. 40 characters or fewer. Letters, digits and ./_ only.', max_length=40, unique=True, validators=[CustomASCIIUsernameValidator()], verbose_name='username')
    followed_by = models.ManyToManyField("self", symmetrical=False, related_name="following")
    to_be_deleted = models.BooleanField(default=False)
    deletion_date = models.DateField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @classmethod
    def get_user_by_email(cls, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_followers(self):
        return self.followed_by.all()

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

    def get_followed(self):
        return self.following.all()

    def get_followed_products(self):
        return self.followed_products.all()
