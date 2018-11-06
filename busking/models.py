from django.contrib.auth.models import User
from django.db import models

# Create your models here.

#버스커 랭킹 모델
from accounts.models import Busker

#게시물 작성
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    busker = models.ForeignKey(Busker, on_delete=models.CASCADE, related_name="busker_post")
    post_image = models.ImageField(upload_to='busking/post_image/', blank=True, null=True)
    content = models.CharField(max_length=4096, null=True)
    created_at = models.DateField(auto_now_add=True, auto_created=True)

#게시물 like
class LikePost(models.Model):
    like_post_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    busker = models.ForeignKey(Busker, on_delete=models.CASCADE, related_name='likes')
    likes = models.ForeignKey(User,  on_delete=models.CASCADE)

#코인
class supportCoin(models.Model):
    supportCoin_id = models.AutoField(primary_key=True)
    busker = models.ForeignKey(Busker, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    support_message = models.CharField(max_length=400, null=True)
    coin_amount = models.IntegerField(null=False)
    supportDate = models.DateField(auto_now_add=True, auto_created=True)
    coin_balance = models.IntegerField(null=True)




