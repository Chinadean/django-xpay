from rest_framework import permissions, status
from rest_framework import views
from rest_framework.response import Response


class BaseAPIView(views.APIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = None

    @staticmethod
    def process_request(serializer):
        try:
            if serializer.is_valid():
                serializer.save()
                response = Response(data=serializer.data, status=status.HTTP_200_OK, )
            else:
                raise Exception(serializer.errors)
        except Exception as e:
            response = Response(
                data=e.args,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response


class CreateAPIView(BaseAPIView):
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        return self.process_request(serializer)


class RetrieveAPIView(BaseAPIView):
    def get(self, request, format=None):
        serializer = self.serializer_class(data=request.data or request.query_params)
        return self.process_request(serializer)


class CreateRetrieveAPIView(CreateAPIView, RetrieveAPIView):
    pass
