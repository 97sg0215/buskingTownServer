from django.contrib import admin

# Register your models here.
from busking.models import Post, supportCoin, RoadConcert


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'busker', 'post_image', 'content', 'created_at')

class CoinAdmin(admin.ModelAdmin):
    list_display = ('supportCoin_id','busker','user','coin_amount', 'date_created', 'coin_balance')

class RoadConcertAdmin(admin.ModelAdmin):
    list_display = ('road_concert_id', 'busker', 'road_address','road_lon','road_lat', 'road_name', 'road_concert_date', 'road_concert_start_time', 'road_concert_end_time')

# class FollowerStatics(admin.ModelAdmin):
#     list_display = ('busker', 'follower_count_statistics_date')

admin.site.register(Post, PostAdmin)
admin.site.register(supportCoin, CoinAdmin)
admin.site.register(RoadConcert, RoadConcertAdmin)
# admin.site.register(BuskerFollowerStatistics, FollowerStatics)