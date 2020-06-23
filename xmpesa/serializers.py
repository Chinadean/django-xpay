from rest_framework import serializers

from xmpesa.utils import mpesa


class LNMSerializer(serializers.Serializer):
    amount = serializers.FloatField(default=0, write_only=True, )
    mobile_number = serializers.CharField(
        max_length=13, allow_null=False, allow_blank=False,
        help_text="must be in the format '2547xxxxxxxx', '07xxxxxxxx' or '+2547xxxxxxxx'",
    )
    account_reference = serializers.CharField(
        max_length=255, allow_null=True,
        allow_blank=True, default=None,
    )
    transaction_description = serializers.CharField(
        max_length=255, allow_null=True,
        allow_blank=True, default=None,
    )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return validated_data

    def to_representation(self, instance):
        return mpesa.Mpesa().lipa_na_mpesa(**instance)
