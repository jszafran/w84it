# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .views import User
from django.db.models import Q
import datetime

# delete users that never activated their accounts and creation date is >= n_days
@shared_task(name='delete_not_activated_users')
def delete_not_activated_users(n_days):
    not_activated_users = User.objects.filter(
        Q(is_active = False) &         # currently inactive users
        Q(last_login__isnull = True) & # never logged in
        Q(date_joined__date__lte = datetime.date.today() - datetime.timedelta(days = n_days))
    )

    not_activated_users.delete()

# delete users that asked for deletion of their accounts and didn't change their mind during grace period
@shared_task(name='delete_leavers_accounts')
def delete_leavers_accounts():
    leavers = User.objects.filter(Q(deletion_date = datetime.date.today()) &
                                  Q(to_be_deleted = True))
    
    leavers.delete()
