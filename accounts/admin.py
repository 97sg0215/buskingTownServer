from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


#생성한 버스커모델과 프로필 모델을 Django admin에서 확인 가능하게끔 inline 시켜줌
class BuskerInline(admin.StackedInline):
    model = Busker
    can_delete = False
    verbose_name_plural = 'busker'

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, BuskerInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
