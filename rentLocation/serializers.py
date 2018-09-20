from rest_framework import serializers


#버스커 객체 직렬화
from rentLocation.models import ProvideOption, Provide


class ProvideOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvideOption
        fields = ('user', 'provide_option_id', 'provide_option_name', 'provide_price')


class ProvideSerializer(serializers.ModelSerializer):
    provide_options = ProvideOptionSerializer(many=True, required=False)

    class Meta:
        model = Provide
        owner = serializers.Field(source='owner.username')
        fields = ('provide_id', 'user', 'provide_image', 'provider_phone', 'provide_start_date',
                  'provide_end_date', 'provide_start_time', 'provide_end_time', 'provide_location', 'provide_description', 'provide_rule',
                  'provide_refund_rule', 'provide_options')

    def create(self, validated_data):
        user = validated_data.get('user')

        # Get our categories
        provide_option_data = validated_data.pop('provide_options')

        # Create our item
        provide = Provide.objects.create(**validated_data)

        # Process the categories. We create any new categories, or return the ID of existing
        # categories.
        for provide_options in provide_option_data:
            provide_options['provide_option_name'] = provide_options['provide_option_name'].title()
            provide_options, created = ProvideOption.objects.get_or_create(user=user, **provide_options)
            provide.provide_options.add(provide_options.id)

        provide.save()

        return provide









