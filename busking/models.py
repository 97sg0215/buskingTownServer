from django.contrib.auth.models import User
from django.db import models

# Create your models here.

#버스커 랭킹 모델
from accounts.models import Busker, Connections


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
    date_created = models.DateField(auto_now_add=True, auto_created=True)
    time_created = models.TimeField(auto_now_add=True, auto_created=True, null=True)
    coin_balance = models.IntegerField(null=True)
    view_check = models.BooleanField(default=False)

#길거리 공연
class RoadConcert(models.Model):
    road_concert_id = models.AutoField(primary_key=True)
    busker = models.ForeignKey(Busker, on_delete=models.CASCADE)
    road_address = models.CharField(max_length=100)
    road_lon = models.DecimalField(null=True, decimal_places=30, max_digits=100)
    road_lat = models.DecimalField(null=True, decimal_places=30, max_digits=100)
    road_name = models.CharField(max_length=50)
    road_concert_date = models.DateField()
    road_concert_start_time = models.TimeField()
    road_concert_end_time = models.TimeField()


