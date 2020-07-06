from . import *
from ..utils.mpesa import MpesaExpress


class LNMSerializer(BasePaymentSerializer):
    transaction_type = serializers.ChoiceField(choices=MpesaExpress.COMMAND_ID_CHOICES, default='CustomerPayBillOnline', )
    account_reference = serializers.CharField(
        max_length=255, allow_null=True,
        allow_blank=True, default=None,
    )
    transaction_description = serializers.CharField(
        max_length=255, allow_null=True,
        allow_blank=True, default=None,
    )

    def to_representation(self, instance):
        return MpesaExpress().lipa_na_mpesa(**instance)
