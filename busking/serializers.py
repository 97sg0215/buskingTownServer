from rest_framework import serializers

from busking.models import BuskerRank


class BuskerRankSerializer(serializers.ModelSerializer):
    # ModelSerializer 를 이용해서 아래와 같이 짧은 코드로 직렬화 필드를 정의할 수 있다
    class Meta:
        model = BuskerRank
        fields = ('user', 'follower', 'coin')

    # 신규 프로필 instance를 생성해서 리턴해준다
    def create(self, validated_data):
        return BuskerRank.objects.create(**validated_data)

    # 생성되어 있는 프로필 instance 를 저장한 후 리턴해준다
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.follower = validated_data.get('follower', instance.follower)
        instance.coin = validated_data.get('coin', instance.coin)
        instance.save()
        return instance