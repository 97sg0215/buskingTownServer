from django.contrib import admin

# Register your models here.
from busking.models import TopBusker

#admin user에서 확인하기 위함
class BuskerRankInline(admin.StackedInline):
    model = TopBusker
    can_delete = False
    verbose_name_plural = 'busker_rank'