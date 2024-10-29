import httpx
from mpesa.api.auth import MpesaBase


class B2C(MpesaBase):
    def __init__(self, env="sandbox", app_key=None, app_secret=None, sandbox_url="https://sandbox.safaricom.co.ke",
                 live_url="https://safaricom.co.ke"):
        MpesaBase.__init__(self, env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token = self.authenticate()

    def transact(self, originator_conversation_id: str, initiator_name: str,
            security_credential: str, command_id: str, amount: str, party_a: int, party_b: int, remarks: str,
            queue_timeout_url: str, result_url: str, occassion: str=None):
        """This method uses Mpesa's B2C API to transact between an M-Pesa short code to a phone number registered on M-Pesa..

            **Args:**
                - originator_conversation_id (str): Unique request ID for tracking a transaction
                - initiator_name (str): Username used to authenticate the transaction.
                - security_credential (str): Generate from developer portal
                - command_id (str): Options: SalaryPayment, BusinessPayment, PromotionPayment
                - amount(str): Amount of money being sent to the customer.
                - party_a (int): Organization/MSISDN making the transaction - Shortcode (5-6 digits) - MSISDN (12 digits).
                - party_b (int): MSISDN receiving the transaction (12 digits).
                - remarks (str): Comments that are sent along with the transaction(maximum 100 characters).
                - account_reference (str): Use if doing paybill to banks etc.
                - queue_timeout_url (str): The url that handles information of timed out transactions.
                - result_url (str): The url that receives results from M-Pesa api call.
                - ocassion (str): Any additional info to be associated with the transaction


            **Returns:**
                - OriginatorConverstionID (str): The unique request ID for tracking a transaction.
                - ConversationID (str): The unique request ID returned by mpesa for each request made
                - ResponseDescription (str): Response Description message
        """

        payload = {
            "OriginatorConversationID": originator_conversation_id,
            "InitiatorName": initiator_name,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "Amount": amount,
            "PartyA": party_a,
            "PartyB": party_b,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "Occassion": occassion
        }

        headers = {"Authorization": f"Bearer {self.authentication_token}",
                "Content-Type": "application/json"}

        if self.env == "production":
            base_url = self.live_url
        else:
            base_url = self.sandbox_url
        saf_url = f"{base_url}/mpesa/b2c/v3/paymentrequest"

        with httpx.Client() as client:
            try:
                response = client.post(saf_url, headers=headers, json=payload)
                if response.status_code==200:
                    return response.json()
                else:
                    raise ValueError(response.json())
            except httpx.HTTPStatusError as exc:
                raise exc
