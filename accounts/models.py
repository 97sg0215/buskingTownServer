from django.db import models
from django.contrib.auth.models import User
from django.db.models import ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from buskingTownServer import settings
from rest_framework.authtoken.models import Token


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, unique=False, on_delete=models.CASCADE)
    user_birth = models.DateField(null=True, blank=True)
    user_phone = models.CharField(max_length=20, blank=True)
 #   user_image = ThumbnailImageField(upload_to='profile_image/%Y/%m')

# post_save 시그널을 받아 토큰을 생성한다.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Busker(models.Model):
    user = models.OneToOneField(User, unique=False, on_delete=models.CASCADE)
    busker_id = models.AutoField(primary_key=True)
    busker_name = models.CharField(null=True, max_length=50, blank=True)
    team_name = models.CharField(null=True, max_length=50, blank=True)
    busker_tag = models.CharField(null=True, max_length=200, blank=True)
    busker_phone = models.CharField(null=True, max_length=20, blank=True)
    busker_image = ImageField(upload_to='busker_profile_image/', null=True, blank=True)
    certification = models.NullBooleanField(default=None,blank=True)
