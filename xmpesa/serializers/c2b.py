from . import *
from ..utils.mpesa import MpesaC2B


class BaseC2BSerializer(BaseSerializer):
    short_code = serializers.CharField(max_length=6, allow_blank=True, allow_null=True, default=None, )

    @staticmethod
    def get_short_code(kwargs):
        return kwargs.pop('short_code') if 'short_code' in kwargs else None


class C2BRegisterURLSerializer(BaseC2BSerializer):
    response_type = serializers.ChoiceField(choices=MpesaC2B.RESPONSE_TYPES, default='canceled', )
    confirmation_url = serializers.CharField(max_length=1000, allow_blank=True, allow_null=True, default=None, )
    validation_url = serializers.CharField(max_length=1000, allow_blank=True, allow_null=True, default=None, )

    def to_representation(self, instance):
        return MpesaC2B(self.get_short_code(instance)).register_url(**instance)


class C2BSimulateSerializer(BaseC2BSerializer, BasePaymentSerializer):
    command_id = serializers.ChoiceField(choices=MpesaC2B.COMMAND_ID_CHOICES, default=MpesaC2B.COMMAND_IDS[0], )
    account_number = serializers.CharField(max_length=20, )

    def to_representation(self, instance):
        return MpesaC2B(self.get_short_code(instance)).simulate(**instance)
