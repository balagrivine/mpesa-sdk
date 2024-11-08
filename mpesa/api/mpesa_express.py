import httpx
import time
import base64
from datetime import datetime
from typing import Dict, Any

from mpesa.api.auth import MpesaBase

class MpesaExpress(MpesaBase):
    """
    MpesaExpress class interacts with Mpesa's Mpesa Express API to simulate
    stk pushes and check the status of those transactions

    Attributes:
        authentication_token: Optional[str]: token to authenticate Mpesa Express API calls

    Methods:
        stk_push() -> Dict[str, Any]: Initiates a Lipa na Mpesa payment
        query() -> Dict[str, Any]: Queries the status of a Lipa na Mpesa transaction
    """
    def __init__(
            self,
            app_key: str=None,
            app_secret: str=None,
            env="sandbox",
            sandbox_url: str="https://sandbox.safaricom.co.ke",
            live_url: str="https://safaricom.co.ke"
        ):
        super().__init__(env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token: Optional[str] = self.authenticate()

    def stk_push(
            self,
            short_code: int,
            pass_key: str,
            transaction_type: str,
            amount: int,
            sender_msisdn: int,
            receiver_msisdn: int,
            callback_url: str,
            transaction_desc: str,
            account_ref: str
        ) -> Dict[str, Any]:
        """
        Initiates an online payment on behalf of a customer

        Args:
            short_code (int): The organization shortcode used to receive the transaction
            pass_key (str): Lipa na Mpesa pass key
            transaction_type (str): Identifies the transaction when sending request to Mpesa.
                                    Options are CustomerPayBillOnline and CustomerBuyGoodsOnline
            amount (int): Amount transacted
            sender_msisdn (int): A valid Safaricom mobile number that is M-PESA registered
            receiver_msisdn (int): The mobile number to receive the STK pin prompt
            callback_url (str): A valid secure URL that is used to receive notifications from M-Pesa API
            transaction_desc (str): Additional info sent along with the request
            account_ref (str): Identifier of the transaction for the CustomerPayBillOnline transaction type

        Returns:
            Dict[str, Any]: Parsed JSON response from the API with transaction details

        Raises:
            httpx.HTTPStatusError: Raised for HTTP errors during the request
            ValueError: Raised for invalid or unsuccessful response from Mpesa API
        """
        password = self.create_password(short_code, pass_key)
        timestamp = self.create_timestamp()
        
        payload = {
            "BusinessShortCode": short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": transaction_type,
            "Amount": amount,
            "PartyA": sender_msisdn,
            "PartyB": short_code,
            "PhoneNumber": receiver_msisdn,
            "CallBackURL": callback_url,
            "AccountReference": account_ref,
            "TransactionDesc": transaction_desc
        }

        headers = {
            "Authorization": f"Bearer {self.authentication_token}",
            "Content-Type": "application/json"
        }

        base_url = self.live_url if self.env == "production" else self.sandbox_url
        api_url = f"{base_url}/mpesa/stkpush/v1/processrequest"

        with httpx.Client() as client:
            try:
                response = client.post(api_url, headers=headers, json=payload)
                response.raise_for_status()

                return response.json()

            except httpx.HTTPStatusError as http_err:
                raise http_err

            except (ValueError, httpx.RequestError) as err:
                print(f"An error occured during Lipa na Mpesa transaction: {err}")
                raise (
                    "An error occured during the tranaction process"
                    ) from err

    def create_timestamp(self) -> str:
        """
        Creates a timestamp when a transaction was initiated
        
        Returns:
            (str): The created timestamp
        """
        timestamp = time.time()
        formatted_timestamp = datetime.fromtimestamp(timestamp).strftime("%Y%m%d%H%M%S")

        return formatted_timestamp

    def create_password(self, pass_key: str, short_code: int) -> str:
        """Creates a password used for encrypting the request sent

        Returns:
            Base64 encoded combination of short_code+pass_key+timestamp
        """
        try:
            timestamp = self.create_timestamp()
            # String to be encoded and used as password
            to_encode=f"{str(short_code)}{pass_key}{timestamp}"
            password = base64.b64encode(to_encode.encode())

            return str(password)
        except Exception as e:
            raise e

    def status(
            self,
            short_code: str,
            checkout_request_id: str,
            pass_key: str
        ):
        """
        Checks the status of a Lipa Na M-Pesa online payment

        Args:
            short_code (str): Organization's shortcode used to receive the transaction
            checkout_request_id (str): Unique identifier of the processed checkout transaction request
            pass_key: Pass key for Lipa Na M-Pesa

        Returns:
            Dict[str, Any]: Parsed JSON response from the API with transaction details

        Raises:
            httpx.HTTPStatusError: raised for HTTP errors during the request
            ValueError: Raised for invalid or unsuccessful response from Mpesa API
        """

        password = self.create_password(short_code, pass_key)
        timestamp = self.create_timestamp()

        headers = {
            "Authorization": f"Bearer {self.authentication_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": short_code,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        base_url = self.live_url if self.env == "production" else self.sandbox_url
        api_url = f"{base_url}/mpesa/stkpushquery/v1/query"
        
        with httpx.Client() as client:
            try:
                response = client.post(api_url, headers=headers, json=payload)
                response.raise_for_status()

                return response.json()

            except httpx.HTTPStatusError as http_err:
                print(f"{http_err.response.status_code} - {http_err.request.url}")
                raise http_err

            except (ValueError, httpx.RequestError) as err:
               raise (
                    "An error occured during checking trnsaction status."
                    ) from err
