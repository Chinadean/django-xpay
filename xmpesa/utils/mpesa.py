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

    def b2c(self):
        return self._send_typed_transaction_request('b2c', {
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
        return self._send_typed_transaction_request('b2b', {
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

    def c2b(self):
        return self._send_transaction_request(
            url=r'http://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl',
            request_data={
                "ShortCode": " ",
                "ResponseType": " ",
                "ConfirmationURL": "http://ip_address:port/confirmation",
                "ValidationURL": "http://ip_address:port/validation_url",
            },
        )

    def c2b_simulate(self):
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate',
            request_data={
                "ShortCode": " ",
                "CommandID": "CustomerPayBillOnline",
                "Amount": " ",
                "Msisdn": " ",
                "BillRefNumber": " ",
            },
        )

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

    def lipa_na_mpesa(self, amount, mobile_number, account_reference=None, transaction_description=None, ):
        """
        Lipa na M-Pesa Online Payment API is used to initiate a M-Pesa transaction
        on behalf of a customer using STK Push. This is the same technique mySafaricom
         App uses whenever the app is used to make payments
        """
        # remove any host that is an ip address or localhost
        hosts = [h for h in settings.ALLOWED_HOSTS if re.search(r'[a-zA-Z]+', h) and not re.search(r'localhost', h)]
        mobile_number = re.sub(r'^0|\+254', '254', mobile_number)
        if not valid_str(mobile_number, 12):
            raise Exception(f"invalid mobile number '{mobile_number}'")
        short_code = self.__LNM.get('SHORTCODE')
        pass_key = self.__LNM.get('PASSKEY')
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        password = str(base64.encodebytes(bytes(f'{short_code}{pass_key}{timestamp}', 'utf-8')), 'utf-8')
        transaction_desc = transaction_description if valid_str(transaction_description) else 'test'
        acc_ref = account_reference if valid_str(account_reference) else 'test'
        callback_url = f'https://{hosts[0]}/mpesa/lnm/response/' if len(
            hosts) > 0 else "http://requestbin.net/r/ru8rr9ru"
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            request_data={
                "BusinessShortCode": short_code,  # The organization shortcode used to receive the transaction
                "Password": re.sub(r'\n', '', password),
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": str(Money(amount, lowest_value=True).amount),
                "PartyA": mobile_number,  # The MSISDN sending the funds
                "PartyB": short_code,  # The organization shortcode receiving the funds
                "PhoneNumber": mobile_number,  # The MSISDN sending the funds
                "CallBackURL": callback_url,
                "AccountReference": acc_ref,  # Used with M-Pesa PayBills
                "TransactionDesc": transaction_desc,  # A description of the transaction
            },
        )

    def lipa_na_mpesa_query(self):
        return self._send_transaction_request(
            url=r'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query',
            request_data={
                "BusinessShortCode": " ",
                "Password": " ",
                "Timestamp": " ",
                "CheckoutRequestID": " ",
            },
        )

    def _send_typed_transaction_request(self, type: str, request_data: dict):
        return self._send_transaction_request(
            f'https://sandbox.safaricom.co.ke/mpesa/{type}/v1/paymentrequest',
            request_data,
        )

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
