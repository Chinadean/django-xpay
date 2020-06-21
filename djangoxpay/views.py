import json

from rest_framework import permissions, status
from rest_framework import views
from rest_framework.response import Response


class APIView(views.APIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = None

    def post(self, request, format=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = Response(
                    data=serializer.data,
                    status=status.HTTP_200_OK,
                )
            else:
                response = Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            response = Response(
                data={'error': json.dumps(e.args[0]), },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response
