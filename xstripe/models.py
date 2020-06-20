from djangoxpay.models import BaseModel


class ClientSecret(BaseModel):
    def __init__(self, client_secret=None):
        self.client_secret = client_secret
