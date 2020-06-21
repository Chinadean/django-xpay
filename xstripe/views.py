from xauth.utils import get_wrapped_response

from djangoxpay import views
from .serializers import ClientSecretSerializer


class ClientSecretView(views.APIView):
    serializer_class = ClientSecretSerializer

    def post(self, request, format=None):
        return get_wrapped_response(super().post(request, format))
