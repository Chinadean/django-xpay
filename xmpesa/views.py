from rest_framework.response import Response
from xauth.utils import get_wrapped_response

from djangoxpay import views
from .serializers import *


class LNMView(views.CreateAPIView):
    serializer_class = LNMSerializer

    def post(self, request, format=None):
        return get_wrapped_response(super().post(request, format))


class LNMResponseView(views.RetrieveAPIView):
    def get(self, request, format=None):
        response = Response(data=request.data, )
        print(response.data)  # TODO
        return get_wrapped_response(response)
