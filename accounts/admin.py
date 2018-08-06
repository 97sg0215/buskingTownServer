from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from busking.admin import BuskerRankInline
from .models import *

class BuskerInline(admin.StackedInline):
    model = Busker
    can_delete = False
    verbose_name_plural = 'busker'

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, BuskerInline, BuskerRankInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
