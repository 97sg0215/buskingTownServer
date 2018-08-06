from django.contrib import admin

# Register your models here.
from busking.models import BuskerRank


class BuskerRankInline(admin.StackedInline):
    model = BuskerRank
    can_delete = False
    verbose_name_plural = 'busker_rank'