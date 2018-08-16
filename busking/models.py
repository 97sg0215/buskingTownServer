from django.contrib.auth.models import User
from django.db import models

# Create your models here.

#버스커 랭킹 모델
from accounts.models import Busker

class TopBusker(models.Model):
    data = models.DateField()
    busker = models.ForeignKey(Busker, on_delete=models.CASCADE)



