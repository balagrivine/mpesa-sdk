import httpx
from typing import Dict, Optional, Any

from mpesa.api.auth import MpesaBase

class Reversal(MpesaBase):
    """
    Reversal class interacts with M-pesa's reversal api to
    revesrse C2B transactions

    Attributes:
        authentication_token (Optionaal[str]): Access token for authenticating
        API requests

    Methods:
        reverse(): Reverses a C2B transaction
    """

    def __init__(
        self,
        env: Optional[str] = "sandbox",
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
        sandbox_url: Optional[str] = "https://sandbox.safaricom.co.ke",
        live_url: Optional[str] = "https://safaricom.co.ke"
    ):
        """
        Initializes the Reversal instance and authenticates using the MpesaBase class.

        Args:
            env (str): The environemnt in which to run; options are "sanbox" and
            "production
            app_key (str): Consumer key for Mpesa API
            app_secret (str): Consumer secret for Mpesa API
            sandbox_url (str): URL for Mpesa's sandbox environment
            live_url (str): URL for Mpesa's production environment
        """
        super().__init__(env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token: Optional[str] = self.authenticate()

    def reverse(
        self,
        receiver: int,
        initiator: str,
        amount: str,
        security_credential: str,
        transaction_id: str,
        timeout_url: str,
        result_url: str,
        occasion: Optional[str],
        remarks: str,
        receiver_identifier: str = "11"
    ):
        """
        Reverses a C2B M-Pesa transaction

        Args:
            receiver (int): The organization that receives the transaction.
            initiator (str): Name of the initiator to initiate the request.
            amount (int): Amount transacted in the transaction is to be reversed,
            down to the cent.
            security_credential (str): Encrypted password for the initiator.
            transaction_id (str): Mpesa Transaction ID of the transaction to be reversed.
            timeout_url (str): Path that stores info about timed-out transactions.
            result_url (str): Path that stores information about the transaction.
            remarks (str): Coments sent along with the transaction.
            receiver_identifier (str): Type of organization receiving the transaction.

        Returns:
            Dict[str, Any]: Parsed JSON response containing transaction details.

        Raises:
            httpx.HTTPStatusError: Raised for HTTP errors during the transaction.
            ValueError: Raised for invalid or unsuccessful response from Mpesa API.
        """

        payload = {
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID":"TransactionReversal",
            "TransactionID": transaction_id,
            "Amount": amount,
            "ReceiverParty": receiver,
            "RecieverIdentifierType": receiver_identifier,
            "ResultURL": result_url,
            "QueueTimeOutURL": timeout_url,
            "Remarks": remarks,
            "Occasion": occasion
        }

        headers = {
            "Authorization": f"Bearer {self.authentication_token}",
            "Content-Type": "application/json"
        }

        base_url = self.live_url if self.env == "production" else self.sandbox_url
        api_url = f"{base_url}/mpesa/reversal/v1/request"

        with httpx.Client() as client:
            try:
                response = client.post(api_url, headers=headers, json=payload)
                response.raise_for_status() # Raises HTTP errors if status is not 200

                return response.json()

            except httpx.HTTPStatusError as http_err:
                print(f"HTTP Error during Mpesa reversal request: {http_err}")
                raise http_err

            except (ValueError, httpx.RequestError) as err:
                print(f"Error occurred during reversal request: {err}")
                raise (
                    "An error occured during the reversal request."
                ) from err
