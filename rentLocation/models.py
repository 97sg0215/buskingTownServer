import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from accounts.models import Busker


class Provide(models.Model):
    provide_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provide_location_name = models.CharField(max_length=50, null=False)
    provide_type = models.IntegerField(null=False)
    provide_image = models.ImageField(upload_to='rentLocation/provide/', null=False)
    provider_phone = models.CharField(null=False, max_length=20)
    provider_email = models.EmailField(null=True)
    provide_start_date = models.DateField(null=False)
    provide_end_date = models.DateField(null=False)
    provide_start_time = models.TimeField(null=False)
    provide_end_time = models.TimeField(null=False)
    provide_location = models.CharField(null=False,max_length=200)
    provide_description = models.CharField(null=False,max_length=200)
    provide_rule = models.CharField(null=False, max_length=500)
    provide_refund_rule = models.CharField(null=False, max_length=500)

    def get_options(self):
        options = ProvideOption.objects.filter(provide=self.provide_id).order_by('provide_price')
        return options


    def reservation_check(self):
        #다른 예약 시간
        l = ReservationPracticeRoom.objects.filter(provide=self.provide_id)

        return l


class ProvideOption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provide = models.ForeignKey(Provide, unique=False, on_delete=models.CASCADE, blank=True)
    provide_option_id = models.AutoField(primary_key=True)
    provide_option_name = models.CharField(max_length=20, null=False)
    provide_price = models.IntegerField(null=False)


class ReservationPracticeRoom(models.Model):
    busker = models.ForeignKey(Busker, on_delete=models.CASCADE)
    provide = models.ForeignKey(Provide, on_delete=models.CASCADE, related_name='reservation_concert_provide')
    provide_option = models.ForeignKey(ProvideOption, on_delete=models.CASCADE, related_name='reservation_concert_provide_option')
    reservation_id = models.AutoField(primary_key=True)
    practice_date = models.DateField(null=False)
    practice_start_time = models.TimeField(null=False)
    practice_end_time = models.TimeField(null=False)
    practice_fee = models.IntegerField(null=False)

class ReservationConcertRoom(models.Model):
    busker = models.ForeignKey(Busker, on_delete=models.CASCADE)
    provide = models.ForeignKey(Provide, on_delete=models.CASCADE, related_name='reservation_provide')
    provide_option = models.ForeignKey(ProvideOption, on_delete=models.CASCADE, related_name='reservation_provide_option')
    concert_reservation_id = models.AutoField(primary_key=True)
    concert_date = models.DateField(null=False)
    concert_start_time = models.TimeField(null=False)
    concert_end_time = models.TimeField(null=False)
    concert_fee = models.IntegerField(null=False)


