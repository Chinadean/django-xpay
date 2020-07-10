from xauth import views


class RetrieveAPIView(views._BaseAPIView):
    def get(self, request, format=None):
        return self.process_request(request)

    def on_valid_response_serializer(self, serializer):
        pass


class CreateRetrieveAPIView(views.CreateAPIView, RetrieveAPIView):
    pass
