from accounts.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Profile
from busking.models import TopBusker
from busking.serializers import BuskerRankSerializer

#사용자 프로필 객체 직렬화
class ProfileSerializer(serializers.ModelSerializer):
    # ModelSerializer 를 이용해서 아래와 같이 짧은 코드로 직렬화 필드를 정의할 수 있다
    class Meta:
        model = Profile
        fields = ('user', 'user_phone', 'following', 'follows_requesting_user')

    following = serializers.SerializerMethodField()
    follows_requesting_user = serializers.SerializerMethodField()

    # 신규 프로필 instance를 생성해서 리턴해준다
    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    # 생성되어 있는 프로필 instance 를 저장한 후 리턴해준다
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.user_phone = validated_data.get('user_phone', instance.user_phone)
        instance.save()
        return instance

    def get_following(self, obj):
        creator = self.context['request'].user
        following = obj.user
        connected = Connection.objects.filter(creator=creator, following=following)
        return connected
        #팔로워 숫자로 보려면 return len(connected)

    def get_follows_requesting_user(self, obj):
        creator = self.context['request'].user
        following = obj.user
        connected = Connection.objects.filter(creator=following, following=creator)
        return connected

#버스커 객체 직렬화
class BuskerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busker
        fields = ('user', 'busker_id', 'busker_name', 'team_name',
                  'busker_phone', 'busker_tag', 'busker_image', 'certification')

#프로필과 버스커 정보를 담는 user객체 직렬화
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    busker = BuskerSerializer(required=True)
    busker_rank = BuskerRankSerializer(required=True, write_only=True)
    class Meta:
        model = User
        fields = ('url', 'email', 'username', 'profile', 'busker', 'busker_rank')

    def create(self, validated_data):
        # create user
        user = User.objects.create(
            url=validated_data['url'],
            email=validated_data['email'],
            username=validated_data['username']
        )

        profile_data = validated_data.pop('profile')
        # create profile
        profile = Profile.objects.create(
            user=user,
            user_phone=profile_data['user_phone'],
            following=profile_data['following'],
            follows_requesting_user=profile_data['follows_requesting_user'],
            follow_link=profile_data['follow_link']
        )

        busker_data = validated_data.pop('busker')
        # create busker
        busker = Busker.objects.create(
            user=user,
            busker_id=busker_data['busker_id'],
            busker_name=busker_data['busker_name'],
            team_name=busker_data['team_name'],
            busker_phone=busker_data['busker_phone'],
            busker_tag=busker_data['busker_tag'],
            busker_image=busker_data['busker_image'],
            certification=busker_data['certification']
        )

        busker_rank_data = validated_data.pop('busker_rank')
        busker_rank = TopBusker.objects.create(
            busker=busker_rank_data['busker'],
            date=busker_rank_data['date']
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
