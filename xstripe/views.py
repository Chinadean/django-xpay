from xauth.views import CreateAPIView

from .serializers import ClientSecretSerializer


class ClientSecretView(CreateAPIView):
    serializer_class = ClientSecretSerializer
