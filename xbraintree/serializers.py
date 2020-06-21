from rest_framework import serializers

from djangoxpay.models import Money
from xbraintree.utils import braintree


class BaseSerializer(serializers.Serializer):
    environment = serializers.CharField(
        allow_blank=True, allow_null=True, default=None,
        max_length=20, write_only=True,
    )
    merchant_id = serializers.CharField(
        allow_blank=True, allow_null=True, default=None,
        max_length=50, write_only=True,
    )
    public_key = serializers.CharField(
        allow_blank=True, allow_null=True, default=None,
        max_length=50, write_only=True,
    )
    private_key = serializers.CharField(
        allow_blank=True, allow_null=True, default=None,
        max_length=50, write_only=True,
    )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return validated_data


class ClientTokenSerializer(BaseSerializer):
    customer_id = serializers.CharField(
        allow_blank=True, allow_null=True, default=None,
        max_length=255, write_only=True,
    )

    def to_representation(self, instance):
        customer_id = instance.pop('customer_id') if 'customer_id' in instance else None
        token = braintree.Braintree(**instance).client_token(customer_id)
        return {'token': token}


class CheckoutSerializer(serializers.Serializer):
    nonce = serializers.CharField(
        allow_blank=False, allow_null=False,
        max_length=255, write_only=True,
    )
    device_data = serializers.CharField(
        allow_blank=True, allow_null=True, default=None,
        max_length=1500, write_only=True,
    )
    amount = serializers.FloatField(default=0, write_only=True, )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return validated_data

    def to_representation(self, instance):
        return braintree.Braintree().confirm_payment(
            nonce=instance.get('nonce'),
            amount=Money(instance.get('amount', 0)).amount,
            device_data=instance.get('device_data'),
        )
