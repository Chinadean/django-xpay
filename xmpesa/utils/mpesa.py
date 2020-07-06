import base64
import json
import re
from datetime import datetime

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from xauth.utils import valid_str, is_http_response_success

from djangoxpay.models import Money


class Mpesa:
    COMMAND_IDS = ['CustomerPayBillOnline', 'CustomerBuyGoodsOnline']
    COMMAND_ID_CHOICES = [('CustomerPayBillOnline', 'Pay Bill',), ('CustomerBuyGoodsOnline', 'Buy Goods',)]
    _DEFAULT_CALLBACK_URL = "http://requestbin.net/r/ru8rr9ru"
    __MPESA_SETTING = settings.PAYMENT.get('MPESA', {})
    __CONSUMER_KEY = __MPESA_SETTING.get('CONSUMER_KEY')
    __CONSUMER_SECRET = __MPESA_SETTING.get('CONSUMER_SECRET')
    __LNM = __MPESA_SETTING.get('LNM', {})

    def __init__(self, consumer_key=__CONSUMER_KEY, consumer_secret=__CONSUMER_SECRET):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    @property
    def access_token(self):
        response = json.loads(requests.get(
            r"https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
            auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
        ).text)
        return response['access_token']

    @staticmethod
    def get_sanitized_amount(amount):
        return str(Money(amount, lowest_value=True).amount)

    @staticmethod
    def get_sanitized_msisdn(number):
        mobile_number = re.sub(r'^0|\+254', '254', number)
        if not valid_str(mobile_number, 12):
            raise Exception(f"invalid mobile number '{mobile_number}'")
        return mobile_number

    def account_balance(self):
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query',
            request_data={
                "Initiator": " ",
                "SecurityCredential": " ",
                "CommandID": "AccountBalance",
                "PartyA": "shortcode",
                "IdentifierType": "4",
                "Remarks": "Remarks",
                "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                "ResultURL": "https://ip_address:port/result_url",
            },
        )

    def transaction_status(self):
        """
        Transaction Status API checks the status of a B2B, B2C and C2B APIs transactions
        """
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query',
            request_data={
                "Initiator": " ",
                "SecurityCredential": " ",
                "CommandID": "TransactionStatusQuery",
                "TransactionID": " ",
                "PartyA": " ",
                "IdentifierType": "1",
                "ResultURL": "https://ip_address:port/result_url",
                "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                "Remarks": " ",
                "Occasion": " ",
            },
        )

    def reverse(self):
        """
        Reverses a B2B, B2C or C2B M-Pesa transaction
        """
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/reversal/v1/request',
            request_data={
                "Initiator": " ",
                "SecurityCredential": " ",
                "CommandID": "TransactionReversal",
                "TransactionID": " ",
                "Amount": " ",
                "ReceiverParty": " ",
                "RecieverIdentifierType": "4",
                "ResultURL": "https://ip_address:port/result_url",
                "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                "Remarks": " ",
                "Occasion": " ",
            },
        )

    def get_command_type_or_fail(self, command_id=COMMAND_IDS[0]):
        command_id = command_id if valid_str(command_id) else self.COMMAND_IDS[0]
        assert command_id in self.COMMAND_IDS, f'Command must be one of \'{", ".join(self.COMMAND_IDS)}\''
        return command_id

    def _send_transaction_request(self, url: str, request_data: dict, ):
        request = requests.post(
            url=url,
            json=request_data,
            headers={'Authorization': f'Bearer {self.access_token}', },
        )
        response = json.loads(request.text)
        if is_http_response_success(request.status_code):
            return response
        raise Exception(response.get('errorMessage'), response)

    @staticmethod
    def _create_callback_url(default=_DEFAULT_CALLBACK_URL):
        # remove any host that is an ip address or localhost
        hosts = [h for h in settings.ALLOWED_HOSTS if re.search(r'[a-zA-Z]+', h) and not re.search(r'localhost', h)]
        return f'https://{hosts[0]}/mpay/lnm/response/' if len(hosts) > 0 else default


class _MpesaC2BPay(Mpesa):
    def __init__(self, short_code=None, **kwargs):
        self.short_code = self.__LNM.get('SHORTCODE') if not valid_str(short_code) else short_code
        super(_MpesaC2BPay, self).__init__(**kwargs)


class MpesaExpress(_MpesaC2BPay):

    def lipa_na_mpesa(self, amount, mobile_number, transaction_type=None, account_reference=None,
                      transaction_description=None, ):
        """
        Lipa na M-Pesa Online Payment API is used to initiate a M-Pesa transaction
        on behalf of a customer using STK Push. This is the same technique mySafaricom
         App uses whenever the app is used to make payments
        """
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        password = str(base64.encodebytes(bytes(f'{self.short_code}{self.__LNM.get("PASSKEY")}{timestamp}', 'utf-8')),
                       'utf-8')
        transaction_desc = transaction_description if valid_str(transaction_description) else 'test'
        acc_ref = account_reference if valid_str(account_reference) else 'test'
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            request_data={
                "BusinessShortCode": self.short_code,  # The organization shortcode used to receive the transaction
                "Password": re.sub(r'\n', '', password),
                "Timestamp": timestamp,
                "TransactionType": self.get_command_type_or_fail(transaction_type),
                "Amount": self.get_sanitized_amount(amount),
                "PartyA": self.get_sanitized_msisdn(mobile_number),  # The MSISDN sending the funds
                "PartyB": self.short_code,  # The organization shortcode receiving the funds
                "PhoneNumber": mobile_number,  # The MSISDN sending the funds
                "CallBackURL": self._create_callback_url(),
                "AccountReference": acc_ref,  # Used with M-Pesa PayBills
                "TransactionDesc": transaction_desc,  # A description of the transaction
            },
        )

    def query(self):
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query',
            request_data={
                "BusinessShortCode": " ",
                "Password": " ",
                "Timestamp": " ",
                "CheckoutRequestID": " ",
            },
        )


class MpesaC2B(_MpesaC2BPay):
    RESPONSE_TYPES = ['Canceled', 'Completed']

    def register_url(self, response_type=None, confirmation_url=None, validation_url=None):
        response_type = response_type.lower().capitalize() if valid_str(response_type) else 'Canceled'
        response_types = ", ".join(self.RESPONSE_TYPES)
        assert response_type in self.RESPONSE_TYPES, f'Response type must be one of \'{response_types}\''
        confirmation_url = confirmation_url if valid_str(confirmation_url) else self._create_callback_url()
        validation_url = validation_url if valid_str(validation_url) else self._DEFAULT_CALLBACK_URL
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl',
            request_data={
                "ShortCode": self.short_code,
                "ResponseType": response_type,
                "ConfirmationURL": confirmation_url,
                # replace 'mpesa' word with 'mpay'
                "ValidationURL": re.sub(r'[Mm]-*[Pp][Ee][Ss][Aa]', 'mpay', validation_url),
            },
        )

    def simulate(self, amount, account_number, mobile_number, command_id="CustomerPayBillOnline"):
        command_id = self.get_command_type_or_fail(command_id)
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate',
            request_data={
                "ShortCode": self.short_code,  # This is the Short Code receiving the amount being transacted
                "CommandID": command_id,  # This is a unique identifier of the transaction type
                "Amount": self.get_sanitized_amount(amount),  # This is the amount being transacted
                # This is the phone number initiating the C2B transaction
                "Msisdn": self.get_sanitized_msisdn(mobile_number),
                # This is used on CustomerPayBillOnline option only. This is where a customer is expected
                # to enter a unique bill identifier, e.g an Account Number
                "BillRefNumber": f'{account_number}',
            },
        )


class MpesaB2CorB(Mpesa):
    def b2c(self):
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest',
            request_data={
                "InitiatorName": " ",
                "SecurityCredential": " ",
                "CommandID": " ",
                "Amount": " ",
                "PartyA": " ",
                "PartyB": " ",
                "Remarks": " ",
                "QueueTimeOutURL": "http://your_timeout_url",
                "ResultURL": "http://your_result_url",
                "Occasion": " ",
            }, )

    def b2b(self):
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/b2b/v1/paymentrequest',
            request_data={
                "Initiator": " ",
                "SecurityCredential": " ",
                "CommandID": " ",
                "SenderIdentifierType": " ",
                "RecieverIdentifierType": " ",
                "Amount": " ",
                "PartyA": " ",
                "PartyB": " ",
                "AccountReference": " ",
                "Remarks": " ",
                "QueueTimeOutURL": "http://your_timeout_url",
                "ResultURL": "http://your_result_url",
            })
