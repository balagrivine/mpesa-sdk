import httpx
from typing import Optional, Dict, Any

from mpesa.api.auth import MpesaBase


class TransactionStatus(MpesaBase):
    def __init__(
        self,
        env: str = "sandbox",
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
        sandbox_url: str = "https://sandbox.safaricom.co.ke",
        live_url: str = "https://safaricom.co.ke",
    ):

        super().__init__(env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token: Optional[str] = self.authenticate()

    def check_transaction_status(
        self,
        security_credential: str,
        originator_conversation_id: str,
        party_a: str,
        identifier_type: str,
        transaction_id: str,
        remarks: str,
        initiator: str,
        result_url: str,
        queue_timeout_url: str,
        occassion: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Checks the status of a transaction through Mpesa API.

            Args:
                security_credential (str): Encrypted credential of the user getting transaction status
                originator_conversation_id: (str): unique identifier for the transaction request
                party_a (str): Organization/MSISDN receiving the transaction - MSISDN or shortcode.
                identifier_type (int): Type of organization receiving the transaction 1-MSISDN. 2-Till Number, 3-Shortcode.
                transaction_id (str): Unique identifier to identify a transaction on Mpesa
                remarks (str): Comments that are sent along with the transaction(maximum 100 characters).
                initiator (str): This is the credential/username used to authenticate the transaction request.
                result_url (str): The url that handles information from the mpesa API call.
                queue_timeout_url (str): The url that stores information of timed out transactions.
                occassion (str):

        Returns:
            Dict[str, Any]: Parsed JSON response from the API transaction status

        Raises:
            ValueError: Raised for invalid or unsuccessful response from the API
            httpx.HTTPStatusError: Raised for HTTP errors during the transaction
        """

        # Validation for required credentials
        if not self.app_key or not self.app_secret:
            raise ValueError(
                "App key and app secret must be provided for authentication."
            )

        payload = {
            "Securitycredential": security_credential,
            "OriginatorconversationID": originator_conversation_id,
            "CommandID": "TransactionStatusQuery",
            "PartyA": party_a,
            "IdentifierType": identifier_type,
            "Remarks": remarks,
            "Initiator": initiator,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "TransactionID": originator_conversation_id,
            "Occasion": occassion,
        }
        headers = {
            "Authorization": f"Bearer {self.authentication_token}",
            "Content-Type": "application/json",
        }

        # Determine te base url based on environment
        base_url = self.live_url if self.env == "production" else self.sandbox_url
        saf_url = f"{base_url}/mpesa/transactionstatus/v1/query"

        with httpx.Client() as client:
            try:
                response = client.post(saf_url, headers=headers, json=payload)
                response.raise_for_status()

                return response.json()

            except httpx.HTTPStatusError as exc:
                raise exc

            except (httpx.RequestError, ValueError) as e:
                raise ValueError(
                    "An error occured during retrieval of transaction status process."
                ) from e
