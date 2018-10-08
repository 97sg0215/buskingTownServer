from rest_framework import serializers

from busking.models import Post


#게시물 작성 객체 직렬화
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_id', 'busker', 'post_image', 'content', 'likes', 'created_at', 'likes_count')