from uuid import uuid4

import stripe
from django.conf import settings
from xauth.utils import valid_str

from djangoxpay.models import Money


class Stripe:
    __STRIPE_SETTING = settings.PAYMENT.get('STRIPE', {})
    __API_KEY = __STRIPE_SETTING.get('API_KEY', )

    def __init__(self, api_key=__API_KEY):
        stripe.api_key = api_key if valid_str(api_key) else self.__API_KEY

    @staticmethod
    def get_client_secret(money: Money, **kwargs, ):
        intent = stripe.PaymentIntent.create(
            amount=money.amount,
            currency=money.currency.lower(),
            idempotency_key=uuid4().hex,
            **kwargs,
        )
        return intent.to_dict_recursive()['client_secret']
