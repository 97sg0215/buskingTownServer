from django.contrib import admin

# Register your models here.
from busking.models import TopBusker

class RankAdmin(admin.ModelAdmin):
    list_display = ('data', 'busker')

admin.site.register(TopBusker,RankAdmin)