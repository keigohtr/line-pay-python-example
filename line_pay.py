import urllib3
import json
import uuid


class LinePay:
    """See https://pay.line.me/file/guidebook/technicallinking/LINE_Pay_Integration_Guide_for_Merchant-v1.1.2-JP.pdf"""

    def __init__(self, channel_id: str, channel_secret: str, line_pay_url: str, confirm_url: str,
                 confirm_url_type: str="CLIENT", check_confirm_url_browser: bool=False,
                 cancel_url: str=None):
        self.__headers = {
            'Content-Type': 'application/json',
            'X-LINE-ChannelId': channel_id,
            'X-LINE-ChannelSecret': channel_secret,
        }
        self.__line_pay_url = line_pay_url
        self.__confirm_url = confirm_url
        self.__confirm_url_type = confirm_url_type
        self.__check_confirm_url_browser = check_confirm_url_browser
        self.__cancel_url = cancel_url
        self.__http = urllib3.PoolManager()

    def request(self, method: str, url: str, fields: list=None, body: dict=None) -> dict:
        r = self.__http.request(
            method,
            url,
            fields=fields,
            body=json.dumps(body).encode('utf-8'),
            headers=self.__headers
        )
        return json.loads(r.data.decode('utf-8'))

    def get_payments(self, transaction_id: list=[], order_id: list=[]) -> dict:
        line_pay_url = self.__line_pay_url
        line_pay_endpoint = f'{line_pay_url}/v2/payments'
        method = 'GET'
        fields = []
        if not transaction_id:
            for id in transaction_id:
                fields.append(('transactionId[]', f'{id}'))
        elif not order_id:
            for id in order_id:
                fields.append(('orderId[]', f'{id}'))
        else:
            raise Exception("Error: Need \"transaction_id\" or \"order_id\"")
        return self.request(method=method, url=line_pay_endpoint, fields=fields)

    def request_payments(self, product_name: str, amount: float, currency: str,
                         product_image_url: str=None, mid: str=None, one_time_key: str=None,
                         delivery_place_phone: str=None, pay_type: str='NORMAL',
                         lang_cd: str=None, capture: bool=True,
                         extras_add_friends: dict=None, gmextras_branch_name: str=None) -> (str, dict):
        line_pay_url = self.__line_pay_url
        line_pay_endpoint = f'{line_pay_url}/v2/payments/request'
        method = 'POST'
        order_id = uuid.uuid4().hex
        body = {
            'productName': product_name,
            'amount': amount,
            'currency': currency,
            'confirmUrl': self.__confirm_url,
            'confirmUrlType': self.__confirm_url_type,
            'checkConfirmUrlBrowser': self.__check_confirm_url_browser,
            'orderId': order_id,
            'payType': pay_type,
            'capture': capture,
        }
        if product_image_url is not None:
            body['productImageUrl'] = product_image_url
        if mid is not None:
            body['mid'] = mid
        if one_time_key is not None:
            body['oneTimeKey'] = one_time_key
        if self.__cancel_url is not None:
            body['cancelUrl'] = self.__cancel_url
        if delivery_place_phone is not None:
            body['deliveryPlacePhone'] = delivery_place_phone
        if lang_cd is not None:
            body['langCd'] = lang_cd
        if extras_add_friends is not None:
            body['extras.addFriends'] = extras_add_friends
        if gmextras_branch_name is not None:
            body['gmextras.branchName'] = gmextras_branch_name
        return (order_id, self.request(method=method, url=line_pay_endpoint, body=body))

    def confirm_payments(self, transaction_id: str, amount: float, currency: str) -> dict:
        line_pay_url = self.__line_pay_url
        line_pay_endpoint = f'{line_pay_url}/v2/payments/{transaction_id}/confirm'
        method = 'POST'
        body = {
            'amount': amount,
            'currency': currency,
        }
        return self.request(method=method, url=line_pay_endpoint, body=body)

    def refund_payments(self, transaction_id: str, refund_amount: float=None) -> dict:
        line_pay_url = self.__line_pay_url
        line_pay_endpoint = f'{line_pay_url}/v2/payments/{transaction_id}/refund'
        method = 'POST'
        body = dict()
        if refund_amount is not None:
            body['refundAmount'] = refund_amount
        return self.request(method=method, url=line_pay_endpoint, body=body)

    def get_authorization_payments(self, transaction_id: list=[], order_id: list=[]) -> dict:
        line_pay_url = self.__line_pay_url
        line_pay_endpoint = f'{line_pay_url}/v2/payments/authorizations'
        method = 'GET'
        fields = []
        if not transaction_id:
            for id in transaction_id:
                fields.append(('transactionId[]', f'{id}'))
        elif not order_id:
            for id in order_id:
                fields.append(('orderId[]', f'{id}'))
        else:
            raise Exception("Error: Need \"transaction_id\" or \"order_id\"")
        return self.request(method=method, url=line_pay_endpoint, fields=fields)

    def capture_authorization_payments(self, transaction_id: str, amount: float, currency: str) -> dict:
        line_pay_url = self.__line_pay_url
        line_pay_endpoint = f'{line_pay_url}/v2/payments/authorizations/{transaction_id}/capture'
        method = 'POST'
        body = {
            'amount': amount,
            'currency': currency,
        }
        return self.request(method=method, url=line_pay_endpoint, body=body)

    def void_authorization_payments(self, transaction_id: str) -> dict:
        line_pay_url = self.__line_pay_url
        line_pay_endpoint = f'{line_pay_url}/v2/payments/authorizations/{transaction_id}/void'
        method = 'POST'
        body = {}
        return self.request(method=method, url=line_pay_endpoint, body=body)

    def payment_preapprovedpay_payments(
            self, reg_key: str, product_name: str, amount: float,
            currency: str, capture: bool=True) -> (str, dict):
        line_pay_url = self.__line_pay_url
        line_pay_endpoint = f'{line_pay_url}/v2/payments/preapprovedPay/{reg_key}/payment'
        method = 'POST'
        order_id = uuid.uuid4().hex
        body = {
            'productName': product_name,
            'amount': amount,
            'currency': currency,
            'orderId': order_id,
            'capture': capture,
        }
        return (order_id, self.request(method=method, url=line_pay_endpoint, body=body))

    def get_check_preapprovedpay_payments(self, reg_key: str, credit_card_auth: bool=False):
        line_pay_url = self.__line_pay_url
        line_pay_endpoint = f'{line_pay_url}/v2/payments/preapprovedPay/{reg_key}/check'
        method = 'GET'
        fields = [('creditCardAuth', credit_card_auth)]
        return self.request(method=method, url=line_pay_endpoint, fields=fields)

    def expire_preapprovedpay_payments(
            self, reg_key: str) -> dict:
        line_pay_url = self.__line_pay_url
        line_pay_endpoint = f'{line_pay_url}/v2/payments/preapprovedPay/{reg_key}/expire'
        method = 'POST'
        body = {}
        return self.request(method=method, url=line_pay_endpoint, body=body)

