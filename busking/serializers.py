from rest_framework import serializers

from busking.models import Post, LikePost, supportCoin


#게시물 작성 객체 직렬화
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_id', 'busker', 'post_image', 'content', 'created_at')

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ('like_post_id', 'post', 'busker', 'likes')

class SupportCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = supportCoin
        fields = ('__all__')