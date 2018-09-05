from django.contrib import admin

# Register your models here.
from busking.models import TopBusker, Post


class RankAdmin(admin.ModelAdmin):
    list_display = ('data', 'busker')

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'busker', 'image', 'content', 'created_at')

admin.site.register(TopBusker,RankAdmin)
admin.site.register(Post,PostAdmin)