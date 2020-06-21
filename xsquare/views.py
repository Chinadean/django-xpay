from rest_framework import status
from rest_framework.response import Response
from xauth.utils import get_wrapped_response

from djangoxpay import views
from . import serializers


class PaymentView(views.APIView):
    serializer_class = serializers.PaymentSerializer

    def post(self, request, format=None):
        response = super().post(request, format)
        data = response.data
        if 'errors' in data:
            errors = data.get('errors', [{'detail': 'Error occurred'}])
            response = Response(
                data={
                    'error': errors[0].get('detail', ),
                    'metadata': errors,
                },
                status=status.HTTP_412_PRECONDITION_FAILED,
            )
        return get_wrapped_response(response)
