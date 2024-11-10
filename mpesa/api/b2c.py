from typing import Optional, Dict, Any
import httpx
from mpesa.api.auth import MpesaBase


class B2C(MpesaBase):
    """
    B2C class interacts with Mpesa's B2C API to facilitate transactions from an M-Pesa
    short code to a registered phone number.

    Attributes:
        authentication_token (Optional[str]): Access token for authenticating requests
        to the B2C API.

    Methods:
        transact(): Performs a B2C transaction using the specified details and returns
        the response data.
    """

    def __init__(
        self,
        env: str = "sandbox",
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
        sandbox_url: str = "https://sandbox.safaricom.co.ke",
        live_url: str = "https://safaricom.co.ke",
    ):
        """
        Initializes the B2C instance and authenticates using the MpesaBase class.

        Args:
            env (str): The environment in which to run; options are "sandbox" or
              "production".
            app_key (Optional[str]): Consumer key for the Mpesa API.
            app_secret (Optional[str]): Consumer secret for the Mpesa API.
            sandbox_url (str): URL for Mpesa's sandbox environment.
            live_url (str): URL for Mpesa's production environment.
        """
        super().__init__(env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token: Optional[str] = self.authenticate()

    def transact(
        self,
        originator_conversation_id: str,
        initiator_name: str,
        security_credential: str,
        command_id: str,
        amount: str,
        party_a: int,
        party_b: int,
        remarks: str,
        queue_timeout_url: str,
        result_url: str,
        occassion: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Executes a B2C transaction through the Mpesa API.

        Args:
            originator_conversation_id (str): Unique ID to track the transaction.
            initiator_name (str): Username for transaction authentication.
            security_credential (str): Encrypted credential from the developer portal.
            command_id (str): Type of payment; options include "SalaryPayment",
            "BusinessPayment", "PromotionPayment".
            amount (str): Amount to be sent to the customer.
            party_a (int): Shortcode or MSISDN of the transaction initiator.
            party_b (int): MSISDN of the transaction recipient.
            remarks (str): Remarks for the transaction, max 100 characters.
            queue_timeout_url (str): URL to handle timeouts.
            result_url (str): URL to receive the transaction results.
            occassion (Optional[str]): Optional transaction metadata.

        Returns:
            Dict[str, Any]: Parsed JSON response from the API with transaction details.

        Raises:
            ValueError: Raised for invalid or unsuccessful response from Mpesa API.
            httpx.HTTPStatusError: Raised for HTTP errors during the request.
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
            "Occassion": occassion,
        }

        headers = {
            "Authorization": f"Bearer {self.authentication_token}",
            "Content-Type": "application/json",
        }

        # Define URL based on environment
        base_url = self.live_url if self.env == "production" else self.sandbox_url
        saf_url = f"{base_url}/mpesa/b2c/v3/paymentrequest"

        # Execute the request
        with httpx.Client() as client:
            try:
                response = client.post(saf_url, headers=headers, json=payload)
                response.raise_for_status()  # Ensures HTTP errors are raised

                return response.json()

            except httpx.HTTPStatusError as exc:
                print(f"HTTP error during B2C transaction: {response.json()}")
                raise exc

            except (ValueError, httpx.RequestError) as e:
                print(f"Error occurred during B2C transaction: {e}")
                raise ValueError(
                    "An error occurred during the transaction process."
                ) from e
