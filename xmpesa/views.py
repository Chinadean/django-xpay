from rest_framework.response import Response

from djangoxpay import views
from .serializers import c2b, express


class LNMView(views.CreateAPIView):
    serializer_class = express.LNMSerializer


class LNMResponseView(views.RetrieveAPIView):
    def get(self, request, format=None):
        print(request.data)  # TODO: Delete...
        return Response(data=request.data, )


class C2BRegisterURLView(views.CreateAPIView):
    serializer_class = c2b.C2BRegisterURLSerializer


class C2BSimulateView(views.CreateAPIView):
    serializer_class = c2b.C2BSimulateSerializer
