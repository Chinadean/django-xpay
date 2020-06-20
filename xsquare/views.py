from djangoxpay import views
from . import serializers


class PaymentView(views.APIView):
    serializer_class = serializers.PaymentSerializer
