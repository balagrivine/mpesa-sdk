import httpx

from mpesa.api.auth import MpesaBase


class C2B(MpesaBase):
    def __init__(self, env="sandbox", app_key=None, app_secret=None, sandbox_url=None, live_url=None):
        MpesaBase.__init__(self, env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token = self.authenticate()

    def register(self, shortcode: int, response_type: str=None, confirmation_url: str=None, validation_url: str=None):
        """This method uses Mpesa's C2B API to register validation and confirmation URLs on M-Pesa.

            **Args:**
                - shortcode (int): The short code of the organization.
                - response_type (str): Default response type for timeout. Incase a tranaction times out, Mpesa will by default Complete or Cancel the transaction.
                - confirmation_url (str): Confirmation URL for the client.
                - validation_url (str): Validation URL for the client.


            **Returns:**
                - OriginatorConversationID (str): The unique request ID for tracking a transaction.
                - ConversationID (str): The unique request ID returned by mpesa for each request made
                - ResponseDescription (str): Response Description message
        """

        payload = {
            "ShortCode": shortcode,
            "ResponseType": response_type,
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url
        }

        headers = {"Authorization": f"Bearer {self.authentication_token}",
                "Content-Type": "application/json"
                }

        if self.env == "production":
            base_url = self.live_url
        else:
            base_url = self.sandbox_url

        saf_url = f"{base_url}/mpesa/c2b/v1/registerurl"
        with httpx.Client() as client:
            try:
                response = client.post(saf_url, headers=headers, json=payload).raise_for_status()
                if response.status_code==200:
                    return response.json()
            except httpx.HTTPStatusError as exc:
                raise exc

    def simulate(self, shortcode: int, command_id: str, amount: int, msisdn: int, bill_ref_number: str=None):
        """This method uses Mpesa's C2B API to simulate a C2B transaction.

            **Args:**
                - shortcode (int): The short code of the organization.
                - command_id (str): Unique command for each transaction type. - CustomerPayBillOnline - CustomerBuyGoodsOnline.
                - amount (int): The amount being transacted
                - msisdn (int): Phone number (msisdn) initiating the transaction MSISDN(12 digits)
                - bill_ref_number: Optional. Account number of the organization


            **Returns:**
                - OriginatorConverstionID (str): The unique request ID for tracking a transaction.
                - ConversationID (str): The unique request ID returned by mpesa for each request made
                - ResponseDescription (str): Response Description message
        """

        payload = {
            "ShortCode": shortcode,
            "CommandID": command_id,
            "Amount": amount,
            "Msisdn": msisdn,
            "BillRefNumber": bill_ref_number
        }

        headers = {"Authorization": f"Bearer {self.authentication_token}",
                "Content-Type": "application/json"
                }

        if self.env == "production":
            base_url = self.live_url
        else:
            base_url = self.sandbox_url
        saf_url = f"{base_url}/mpesa/c2b/v1/simulate"

        with httpx.Client() as client:
            try:
                response = client.post(saf_url, headers=headers, json=payload).raise_for_status()
                if response.status_code==200:
                    return response.json()
            except httpx.HTTPStatusError as exc:
                raise exc
