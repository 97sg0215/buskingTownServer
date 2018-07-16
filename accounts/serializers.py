from accounts.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # ModelSerializer 를 이용해서 아래와 같이 짧은 코드로 직렬화 필드를 정의할 수 있다
    class Meta:
        model = Profile
        fields = ('user', 'user_birth', 'user_phone')

    # 신규 프로필 instance를 생성해서 리턴해준다
    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    # 생성되어 있는 프로필 instance 를 저장한 후 리턴해준다
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.user_birth = validated_data.get('user_birth', instance.user_birth)
        instance.user_phone = validated_data.get('user_phone', instance.user_phone)
        instance.save()
        return instance

class BuskerSerializer(serializers.ModelSerializer):
    # ModelSerializer 를 이용해서 아래와 같이 짧은 코드로 직렬화 필드를 정의할 수 있다
    class Meta:
        model = Busker
        fields = ('user', 'busker_name', 'team_name', 'busker_phone', 'busker_tag', 'busker_image', 'certification')

    # 신규 버스커 instance를 생성해서 리턴해준다
    def create(self, validated_data):
        return Busker.objects.create(**validated_data)

    # 생성되어 있는 버스커 instance 를 저장한 후 리턴해준다
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.busker_name = validated_data.get('busker_name', instance.busker_name)
        instance.team_name = validated_data.get('team_name', instance.team_name)
        instance.busker_phone = validated_data.get('busker_phone', instance.busker_phone)
        instance.busker_tag = validated_data.get('busker_tag', instance.busker_tag)
        instance.busker_image = validated_data.get('busker_image', instance.busker_image)
        instance.certification = validated_data.get('certification', instance.certification)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    busker = BuskerSerializer(required=True)
    class Meta:
        model = User
        fields = ('url', 'email', 'username', 'profile', 'busker')

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
            user_birth=profile_data['user_birth'],
            user_phone=profile_data['user_phone']
        )

        busker_data = validated_data.pop('busker')
        # create profile
        busker = Busker.objects.create(
            user=user,
            busker_name=busker_data['busker_name'],
            team_name=busker_data['team_name'],
            busker_phone=busker_data['busker_phone'],
            busker_tag=busker_data['busker_tag'],
            busker_image=busker_data['busker_image'],
            certification=busker_data['certification']
        )
        return user

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
            user_birth=profile_data['user_birth'],
            user_phone=profile_data['user_phone']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class BuskerPhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BuskerPhoto
        fields = ('url', 'id', 'image', 'owner')
        owner = serializers.Field(source='owner.username')