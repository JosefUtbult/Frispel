from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Userprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    ltu_id = models.CharField(max_length=30)
    favorite_food = models.CharField(max_length=100)

    trubadur_member = models.BooleanField(default=False)

    bookings_allowed = models.IntegerField(default=1)
    extended_membership_status = models.BooleanField(default=False)

    expiry_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.username + ' profile'
