from accounts.models import *
from rest_framework import serializers, filters
from django.contrib.auth.models import User
from accounts.models import Profile
from django.db.models import Sum,F


#사용자 프로필 객체 직렬화
from busking.models import LikePost


class ProfileSerializer(serializers.ModelSerializer):
    # ModelSerializer 를 이용해서 아래와 같이 짧은 코드로 직렬화 필드를 정의할 수 있다
    class Meta:
        model = Profile
        fields = ('user', 'user_phone', 'user_image', 'purchase_coin')

    # 신규 프로필 instance를 생성해서 리턴해준다
    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    # 생성되어 있는 프로필 instance 를 저장한 후 리턴해준다
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.user_phone = validated_data.get('user_phone', instance.user_phone)
        instance.user_image = validated_data.get('user_image', instance.user_image)
        instance.purchase_coin = validated_data.get('purchase_coin',instance.purchase_coin)
        instance.save()
        return instance


class ConnectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connections
        fields = ('connection_id', 'user', 'following')

class ScoreSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()
    posts_like = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    def get_follower_count(self, obj):
        following = obj.busker_id
        connected = Connections.objects.filter(following=following)
        return len(connected)

    def get_posts_like(self, obj):
        from busking.models import Post
        busker_id = obj.busker_id
        posts = LikePost.objects.filter(busker=busker_id)
        return len(posts)

    def get_score(self, obj):
        coin_amount = obj.received_coin
        follower_cnt = obj.get_followers()
        likes_cnt = obj.get_like()
        score = coin_amount + len(follower_cnt) + len(likes_cnt)
        return score

    class Meta:
        model = Busker
        fields = ('user', 'busker_id', 'busker_name', 'busker_type', 'team_name', 'busker_phone', 'busker_tag', 'busker_image', 'certification', 'received_coin', 'follower_count', 'posts_like', 'score')


#버스커 객체 직렬화
class BuskerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Busker
        fields = ('user', 'busker_id', 'busker_name', 'busker_type', 'team_name', 'busker_phone', 'busker_tag', 'busker_image', 'certification', 'received_coin')


#프로필과 버스커 정보를 담는 user객체 직렬화
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    busker = BuskerSerializer(required=True)
    class Meta:
        model = User
        fields = ('id', 'url', 'email', 'username', 'profile', 'busker')

    def create(self, validated_data):
        # create user
        user = User.objects.create(
            id=validated_data['id'],
            url=validated_data['url'],
            email=validated_data['email'],
            username=validated_data['username']
        )

        profile_data = validated_data.pop('profile')
        # create profile
        profile = Profile.objects.create(
            user=user,
            user_phone=profile_data['user_phone'],
            user_image=profile_data['user_image'],
            purchase_coin=validated_data['purchase_coin']
        )

        busker_data = validated_data.pop('busker')
        # create busker
        busker = Busker.objects.create(
            user=user,
            busker_id=busker_data['busker_id'],
            busker_type=busker_data['busker_type'],
            busker_name=busker_data['busker_name'],
            team_name=busker_data['team_name'],
            busker_phone=busker_data['busker_phone'],
            busker_tag=busker_data['busker_tag'],
            busker_image=busker_data['busker_image'],
            certification=busker_data['certification'],
            received_coin=busker_data['received_coin'],
            score=busker_data['score']
        )

        return user

#회원가입 객체 직렬화
class SignUpSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'profile')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # create user
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )

        profile_data = validated_data.pop('profile')
        # create profile
        profile = Profile.objects.create(
            user=user,
            user_phone=profile_data['user_phone']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

