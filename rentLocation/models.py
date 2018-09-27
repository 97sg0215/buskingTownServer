from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Provide(models.Model):
    provide_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provide_type = models.CharField(max_length=10, null=True)
    provide_image = models.ImageField(upload_to='rentLocation/provide/', null=True, blank=True)
    provider_phone = models.CharField(null=False, max_length=20)
    provide_start_date = models.DateField()
    provide_end_date = models.DateField()
    provide_start_time = models.TimeField()
    provide_end_time = models.TimeField()
    provide_location = models.CharField(max_length=200)
    provide_description = models.CharField(max_length=200, null=True)
    provide_rule = models.CharField(max_length=500,null=True)
    provide_refund_rule = models.CharField(max_length=500, null=True)

    def get_options(self):
        options = ProvideOption.objects.filter(provide=self.provide_id)
        return options


class ProvideOption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provide = models.ForeignKey(Provide, unique=False, on_delete=models.CASCADE, blank=True)
    provide_option_id = models.AutoField(primary_key=True)
    provide_option_name = models.CharField(max_length=20, null=True)
    provide_price = models.IntegerField()


