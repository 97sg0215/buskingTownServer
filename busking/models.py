from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from accounts.models import Busker


class BuskerRank(models.Model):
    user = models.OneToOneField(User, null=True, unique=False, on_delete=models.CASCADE)
    follower = models.IntegerField(null=True,  blank=True)
    coin = models.IntegerField(null=True, blank=True)