from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # additinal fields to be added here
    followed_by = models.ManyToManyField('self',
                                    symmetrical=False)

    def __str__(self):
        return self.email

    def get_followers(self):
        self.followed_by

    def follow_user(self, obj):
        pass