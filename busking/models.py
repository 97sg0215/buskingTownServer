from django.contrib.auth.models import User
from django.db import models

# Create your models here.

#버스커 랭킹 모델
from accounts.models import Busker

class TopBusker(models.Model):
    busker = models.ForeignKey(Busker, on_delete=models.CASCADE)

#게시물 작성
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    busker = models.ForeignKey(Busker, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    content = models.CharField(max_length=4096, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

#코인
class supportCoin(models.Model):
    supportCoin_id = models.AutoField(primary_key=True)
    busker = models.ForeignKey(Busker, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin_amount = models.IntegerField(null=True)
    supportDate = models.DateTimeField(auto_now_add=True, auto_created=True, null=True)




