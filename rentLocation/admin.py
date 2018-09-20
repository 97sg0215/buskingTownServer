from django.contrib import admin

from rentLocation.models import ProvideOption, Provide


class ProvideOptionInline(admin.StackedInline):
    model = ProvideOption
    list_display = ('provide_option_number','provide_option_name', 'provide_price')

class ProvideAdmin(admin.ModelAdmin):
    inlines = [
        ProvideOptionInline,
    ]

admin.site.register(Provide, ProvideAdmin)