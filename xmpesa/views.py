from rest_framework.response import Response
from xauth.views import CreateAPIView

from djangoxpay import views
from .serializers import c2b, express


class LNMView(CreateAPIView):
    serializer_class = express.LNMSerializer


class LNMResponseView(views.CreateRetrieveAPIView):
    def post(self, request, format=None):
        return Response(data=request.data, )

    def get(self, request, format=None):
        return Response(data=request.data, )


class C2BRegisterURLView(CreateAPIView):
    serializer_class = c2b.C2BRegisterURLSerializer


class C2BSimulateView(CreateAPIView):
    serializer_class = c2b.C2BSimulateSerializer
