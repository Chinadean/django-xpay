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
    app_fee_money = MoneySerializer(write_only=True, )
    production = serializers.BooleanField(write_only=True, default=False, )
    autocomplete = serializers.BooleanField(write_only=True, default=True, )
    access_token = serializers.CharField(
        max_length=500, allow_blank=True, allow_null=True, write_only=True, default=None,
        help_text='from square developer dashboard(blank will use value from settings)'
    )
    nonce = serializers.CharField(max_length=500, allow_blank=False, allow_null=False, write_only=True, )
    location_id = serializers.CharField(max_length=50, allow_blank=True, allow_null=True, write_only=True,
                                        default=None, )
    body = serializers.DictField(allow_empty=True, allow_null=True, default=__DEFAULT_BODY, )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        body = validated_data.get('body', self.__DEFAULT_BODY)
        body['amount_money'] = json.loads(
            json.dumps(validated_data.pop('amount_money'))) if 'amount_money' in validated_data else None
        body['app_fee_money'] = json.loads(
            json.dumps(validated_data.pop('app_fee_money'))) if 'app_fee_money' in validated_data else None
        body['autocomplete'] = validated_data.pop('autocomplete') if 'autocomplete' in validated_data else True
        nonce = validated_data.get('nonce', body.get('source_id', ))
        body['source_id'] = nonce
        access_token = validated_data.pop('access_token') if 'access_token' in validated_data else None
        production = validated_data.pop('production') if 'production' in validated_data else False
        return square.Square(access_token=access_token, production=production).create_payment(nonce, body)
