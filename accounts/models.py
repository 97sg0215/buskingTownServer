from django.db import models
from django.contrib.auth.models import User
from django.db.models import ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver

from buskingTownServer import settings
from rest_framework.authtoken.models import Token
from django.db.models import F, Sum, Count, Case, When, Value

#장고 기본 제공 되는 user 모델과 1대1매핑 하여 확장
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, unique=False, on_delete=models.CASCADE, blank=True)
    user_phone = models.CharField(max_length=20, null=False)
    user_image = models.ImageField(upload_to='user_profile/', null=True, blank=True)

    def get_followings(self):
        followings = Connections.objects.filter(user=self.user)
        return followings

    def get_provides(self):
        from rentLocation.models import Provide
        provides = Provide.objects.filter(user=self.user)
        return provides

    def get_liked(self):
        from busking.models import LikePost
        like_posts = LikePost.objects.filter(likes=self.user)
        return like_posts

# post_save 시그널을 받아 user 토큰을 생성한다.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

#버스커 모델도 user모델의 확장 user에서 제공하는 기본키를 사용하지 않고 busker_id로 기본키 관리
class Busker(models.Model):
    user = models.OneToOneField(User, unique=False, on_delete=models.CASCADE)
    busker_id = models.AutoField(primary_key=True)
    busker_name = models.CharField(null=False, max_length=50, blank=True, unique=True)
    busker_type = models.IntegerField(null=False, blank=True)
    team_name = models.CharField(null=False, max_length=50, blank=True)
    busker_tag = models.CharField(null=False, max_length=200, blank=True)
    busker_phone = models.CharField(null=False, max_length=20, blank=True)
    busker_image = models.ImageField(upload_to='accounts/certification/', null=False, blank=True)
    certification = models.NullBooleanField(default=None, blank=True)
    received_coin = models.IntegerField(blank=True, default=0)

    def get_followers(self):
        followers = Connections.objects.filter(following=self.busker_id)
        return followers

    def get_score(self):
        coin_amount = self.received_coin
        follower_cnt = self.get_followers()
        score = coin_amount + len(follower_cnt)
        return score

    def get_posts(self):
        from busking.models import Post
        posts = Post.objects.filter(busker=self.busker_id)
        return posts

    def get_like(self):
        from busking.models import LikePost
        like_posts = LikePost.objects.filter(busker=self.busker_id)
        return like_posts

    def get_coin(self):
        from busking.models import supportCoin
        supportCoin = supportCoin.objects.filter(busker=self.busker_id)
        return supportCoin

    def get_practice_reservation(self):
        from rentLocation.models import ReservationPracticeRoom
        practiceRoom = ReservationPracticeRoom.objects.filter(busker=self.busker_id)
        return practiceRoom

class Connections(models.Model):
    connection_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=False, related_name="friendship_creator_set", on_delete=models.CASCADE)
    following = models.ForeignKey(Busker, unique=False, related_name="friend_set", on_delete=models.CASCADE)


