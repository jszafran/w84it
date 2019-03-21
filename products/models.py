from django.db import models
from users.models import User


class Product(models.Model):
    owner = models.ForeignKey(User, models.CASCADE, null=False)
    name = models.CharField(max_length=200, help_text='Name of your product/event (up to 200 characters).',
                                blank=False, null=False)
    description = models.TextField(help_text='Description of your product.')
    url = models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=3)
    work_start_date = models.DateField(null=True, blank=True)
    launch_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(null=False, blank=False, auto_now=True)
    last_modified_date = models.DateTimeField(null=False, blank=False, auto_now=True)

    class Meta:
        unique_together = ('name', 'owner',)

    def __str__(self):
        return self.name

    def add_product(self):
        pass
