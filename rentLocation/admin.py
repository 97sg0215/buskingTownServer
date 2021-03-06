from django.contrib import admin

from rentLocation.models import *


class ProvideOptionInline(admin.StackedInline):
    model = ProvideOption
    list_display = ('provide_option_number','provide_option_name', 'provide_price')

class ProvideAdmin(admin.ModelAdmin):
    inlines = [
        ProvideOptionInline,
    ]

admin.site.register(Provide, ProvideAdmin)
admin.site.register(ProvideOption)
admin.site.register(ReservationPracticeRoom)
admin.site.register(ReservationConcertRoom)