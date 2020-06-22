import braintree
from braintree import SuccessfulResult, ErrorResult
from django.conf import settings
from xauth.utils import valid_str


class Braintree:
    __BRAINTREE_SETTING = settings.PAYMENT.get('BRAINTREE', {})
    __MERCHANT_ID = __BRAINTREE_SETTING.get('MERCHANT_ID', )
    __PUBLIC_KEY = __BRAINTREE_SETTING.get('PUBLIC_KEY', )
    __PRIVATE_KEY = __BRAINTREE_SETTING.get('PRIVATE_KEY', )

    def __init__(self, environment='sandbox', merchant_id=__MERCHANT_ID, public_key=__PUBLIC_KEY,
                 private_key=__PRIVATE_KEY, ):
        environment = environment if valid_str(environment) else 'sandbox'
        merchant_id = merchant_id if valid_str(merchant_id) else self.__MERCHANT_ID
        public_key = public_key if valid_str(public_key) else self.__PUBLIC_KEY
        private_key = private_key if valid_str(private_key) else self.__PRIVATE_KEY
        self.gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.parse_environment(environment),
                merchant_id=merchant_id,
                public_key=public_key,
                private_key=private_key
            )
        )

    def client_token(self, customer_id=None):
        """
        :param customer_id: Only applies to the Drop-in UI; not needed when
         generating client tokens for custom integrations.

        A string value representing an existing customer in your Vault.
        Passing this option allows customers to manage their vaulted payment
        methods via the Drop-in UI.
        """
        params = {"customer_id": customer_id} if customer_id else None
        return self.gateway.client_token.generate(params)

    def confirm_payment(self, nonce, amount, device_data=None, ):
        result = self.gateway.transaction.sale({
            "amount": str(amount),
            "payment_method_nonce": nonce,
            "device_data": device_data,
            "options": {
                "submit_for_settlement": True,
            }
        })

        if isinstance(result, SuccessfulResult):
            result = {"success": "payment was successful"}
        elif isinstance(result, ErrorResult):
            result = {"error": result.message, "metadata": result.errors.errors.data}
        return result
