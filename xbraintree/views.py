from xauth.utils import get_wrapped_response

from djangoxpay import views
from .serializers import *


class ClientTokenView(views.CreateRetrieveAPIView):
    serializer_class = ClientTokenSerializer

    def post(self, request, format=None):
        return get_wrapped_response(super().post(request, format))

    def get(self, request, format=None):
        return get_wrapped_response(super().get(request, format))


class CheckoutView(views.CreateAPIView):
    serializer_class = CheckoutSerializer

    def post(self, request, format=None):
        return get_wrapped_response(super().post(request, format))
