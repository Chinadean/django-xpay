from djangoxpay import views
from .serializers import ClientSecretSerializer


class ClientSecretView(views.APIView):
    serializer_class = ClientSecretSerializer
