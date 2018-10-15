from rest_framework import serializers


#버스커 객체 직렬화
from rentLocation.models import ProvideOption, Provide, ReservationPracticeRoom


class ProvideOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvideOption
        fields = ('user', 'provide', 'provide_option_id', 'provide_option_name', 'provide_price')

    def create(self, validated_data):
        return ProvideOption.objects.create(**validated_data)

    # 생성되어 있는 프로필 instance 를 저장한 후 리턴해준다
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.provide = validated_data.get('provide', instance.provide)
        instance.provide_option_id = validated_data.get('provide_option_id', instance.provide_option_id)
        instance.provide_option_name = validated_data.get('provide_option_name', instance.provide_option_name)
        instance.provide_price = validated_data.get('provide_price', instance.provide_price)
        instance.save()
        return instance


class ProvideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provide
        fields = ('provide_id', 'user', 'provide_location_name', 'provide_type', 'provide_image', 'provider_phone', 'provider_email', 'provide_start_date',
                  'provide_end_date', 'provide_start_time', 'provide_end_time', 'provide_location', 'provide_description', 'provide_rule',
                  'provide_refund_rule',)


class ReservationPracticeRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationPracticeRoom
        fields = ('__all__')





