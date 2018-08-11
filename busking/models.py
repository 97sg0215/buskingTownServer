from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from accounts.models import Busker

#버스커 랭킹 모델
class TopBusker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    busker = models.OneToOneField(Busker, primary_key=True, unique=False, on_delete=models.CASCADE)
    busker_rank = models.IntegerField(null=True)
