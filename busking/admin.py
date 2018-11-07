from django.contrib import admin

# Register your models here.
from busking.models import Post, supportCoin


class RankAdmin(admin.ModelAdmin):
    list_display = ('busker',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'busker', 'post_image', 'content', 'created_at')

class CoinAdmin(admin.ModelAdmin):
    list_display = ('supportCoin_id','busker','user','coin_amount', 'date_created', 'coin_balance')

admin.site.register(Post, PostAdmin)
admin.site.register(supportCoin, CoinAdmin)