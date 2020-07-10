from xauth.views import CreateAPIView

from djangoxpay import views
from .serializers import *


class ClientTokenView(views.CreateRetrieveAPIView):
    serializer_class = ClientTokenSerializer


class CheckoutView(CreateAPIView):
    serializer_class = CheckoutSerializer
