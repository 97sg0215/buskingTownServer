from rest_framework import serializers

from busking.models import TopBusker

#버스커 랭킹 객체 직렬화
class BuskerRankSerializer(serializers.ModelSerializer):
    # ModelSerializer 를 이용해서 아래와 같이 짧은 코드로 직렬화 필드를 정의할 수 있다
    class Meta:
        model = TopBusker
        fields = ('data', 'busker')

    # 신규 프로필 instance를 생성해서 리턴해준다
    def create(self, validated_data):
        return TopBusker.objects.create(**validated_data)

    # 생성되어 있는 프로필 instance 를 저장한 후 리턴해준다
    def update(self, instance, validated_data):
        instance.follower = validated_data.get('busker', instance.busker)
        instance.coin = validated_data.get('data', instance.data)
        instance.save()
        return instance