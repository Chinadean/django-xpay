from rest_framework import serializers

from djangoxpay.models import Money
from xstripe.models import ClientSecret
from xstripe.utils import stripe


class ClientSecretSerializer(serializers.Serializer):
    api_key = serializers.CharField(
        max_length=500, write_only=True, allow_null=True, allow_blank=True, default=None,
        help_text='from stripe developer dashboard(living blank will use key provided in settings)',
    )
    amount = serializers.FloatField(default=0, write_only=True, )
    client_secret = serializers.CharField(max_length=500, read_only=True, )
    currency = serializers.ChoiceField(Money.CURRENCIES, default=Money.DEFAULT_CURRENCY, write_only=True, )

    def update(self, instance, validated_data):
        instance.api_key = validated_data.get('api_key', instance.api_key)
        instance.client_secret = validated_data.get('client_secret', instance.client_secret)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.currency = validated_data.get('currency', instance.currency)
        return instance

    def create(self, validated_data):
        api_key = validated_data.pop('api_key') if 'api_key' in validated_data else None
        currency = validated_data.pop('currency') if 'currency' in validated_data else Money.DEFAULT_CURRENCY
        amount = validated_data.pop('amount') if 'amount' in validated_data else 0
        money = Money(amount=amount, currency=currency)
        validated_data['client_secret'] = stripe.Stripe(api_key=api_key).get_client_secret(money)
        return ClientSecret(**validated_data)
