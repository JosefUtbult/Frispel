from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_set_up = models.BooleanField(default=False)

    favorite_food = models.CharField(max_length=100)

    trubadur_member = models.BooleanField(default=False)

    bookings_allowed = models.IntegerField(default=1)
    extended_membership_status = models.BooleanField(default=False)

    application_expiry_date = models.DateField(default=timezone.now)
    registered_expiry_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.username + ' profile'
