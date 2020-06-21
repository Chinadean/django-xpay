import json

from rest_framework import serializers

from djangoxpay.models import Money
from xsquare.utils import square


class MoneySerializer(serializers.Serializer):
    amount = serializers.FloatField(default=0, )
    currency = serializers.ChoiceField(Money.CURRENCIES, default=Money.DEFAULT_CURRENCY)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return validated_data


class PaymentSerializer(serializers.Serializer):
    __DEFAULT_BODY = {
        "source_id": None,
        "customer_id": "VDKXEEKPJN48QDG3BGGFAK05P8",
        "reference_id": "123456",
        "note": "Brief description"
    }
    amount_money = MoneySerializer(write_only=True, )
    app_fee_money = MoneySerializer(write_only=True, allow_null=True, )
    production = serializers.BooleanField(write_only=True, default=False, )
    autocomplete = serializers.BooleanField(write_only=True, default=True, )
    access_token = serializers.CharField(
        max_length=500, allow_blank=True, allow_null=True, write_only=True, default=None,
        help_text='from square developer dashboard(blank will use value from settings)'
    )
    nonce = serializers.CharField(max_length=100, allow_blank=False, allow_null=False, write_only=True,
                                  default='cnon:card-nonce-ok', )
    location_id = serializers.CharField(max_length=50, allow_blank=True, allow_null=True, write_only=True,
                                        default=None, )
    body = serializers.DictField(allow_empty=True, allow_null=True, default=__DEFAULT_BODY, write_only=True, )

    def to_representation(self, instance):
        body = instance.get('body', self.__DEFAULT_BODY)
        if 'amount_money' in instance:
            amount_money = json.loads(json.dumps(instance.pop('amount_money')))
            body['amount_money'] = Money(**amount_money).json
        if 'app_fee_money' in instance:
            app_fee_money = json.loads(json.dumps(instance.pop('app_fee_money')))
            body['app_fee_money'] = Money(**app_fee_money).json
        body['autocomplete'] = instance.pop('autocomplete') if 'autocomplete' in instance else True
        nonce = instance.get('nonce', body.get('source_id', 'cnon:card-nonce-ok'))
        body['source_id'] = nonce
        access_token = instance.pop('access_token') if 'access_token' in instance else None
        production = instance.pop('production') if 'production' in instance else False
        return square.Square(
            access_token=access_token,
            production=production,
        ).create_payment(nonce, body).body

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return validated_data
