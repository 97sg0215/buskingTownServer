from django.contrib import admin

# Register your models here.
from busking.models import Post


class RankAdmin(admin.ModelAdmin):
    list_display = ('busker',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'busker', 'post_image', 'content', 'created_at')

admin.site.register(Post, PostAdmin)