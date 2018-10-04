import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from accounts.models import Busker


class Provide(models.Model):
    provide_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provide_location_name = models.CharField(max_length=50, null=True)
    provide_type = models.CharField(max_length=10, null=True)
    provide_image = models.ImageField(upload_to='rentLocation/provide/', null=True, blank=True)
    provider_phone = models.CharField(null=False, max_length=20)
    provide_start_date = models.DateField()
    provide_end_date = models.DateField()
    available_dates = models.DateField(null=True)
    provide_start_time = models.TimeField()
    provide_end_time = models.TimeField()
    provide_location = models.CharField(max_length=200)
    provide_description = models.CharField(max_length=200, null=True)
    provide_rule = models.CharField(max_length=500, null=True)
    provide_refund_rule = models.CharField(max_length=500, null=True)

    def get_options(self):
        options = ProvideOption.objects.filter(provide=self.provide_id).order_by('provide_price')
        return options


class ProvideOption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provide = models.ForeignKey(Provide, unique=False, on_delete=models.CASCADE, blank=True)
    provide_option_id = models.AutoField(primary_key=True)
    provide_option_name = models.CharField(max_length=20, null=True)
    provide_price = models.IntegerField()


class ReservationPracticeRoom(models.Model):
    busker = models.ForeignKey(Busker, on_delete=models.CASCADE)
    provide = models.ForeignKey(Provide, on_delete=models.CASCADE)
    reservation_id = models.AutoField(primary_key=True)
    practice_date = models.DateField()
    practice_start_time = models.TimeField(null=True)
    practice_end_time = models.TimeField(null=True)
    practice_fee = models.IntegerField()


    # def reservation_date(self):
    #     start_date = datetime.date.today()

    #     provide_start_date_q = Provide.objects.filter(provide_id=self.provide).values('provide_start_date')
    #     provide_end_date_q = Provide.objects.filter(provide_id=self.provide).values('provide_end_date')
    #
    #     available_date = ReservationPracticeRoom.objects.filter(practice_date__range=(provide_start_date_q, provide_end_date_q)).values('practice_date')
    #
    #     return available_date;


        #ReservationPracticeRoom.objects.annotate(practice_date__range=[provide_start_date_q, provide_end_date_q])



