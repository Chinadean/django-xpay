from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return validated_data


class BasePaymentSerializer(BaseSerializer):
    amount = serializers.FloatField(default=0, write_only=True, )
    mobile_number = serializers.CharField(
        max_length=13, allow_null=False, allow_blank=False,
        help_text="must be in the format '2547xxxxxxxx', '07xxxxxxxx' or '+2547xxxxxxxx'",
    )
