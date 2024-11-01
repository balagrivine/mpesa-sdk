from typing import Optional, Dict, Any
import httpx
from mpesa.api.auth import MpesaBase


class C2B(MpesaBase):
    """
    C2B (Customer to Business) class interacts with Mpesa's C2B API to register URLs and simulate transactions.

    Attributes:
        authentication_token (Optional[str]): Access token for authenticating requests to the C2B API.

    Methods:
        register(): Registers validation and confirmation URLs with Mpesa for C2B transactions.
        simulate(): Simulates a C2B transaction using provided transaction details.
    """

    def __init__(
        self,
        env: str = "sandbox",
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
        sandbox_url: Optional[str] = "https://sandbox.safaricom.co.ke",
        live_url: Optional[str] = "https://safaricom.co.ke",
    ):
        """
        Initializes the C2B instance and authenticates using the MpesaBase class.

        Args:
            env (str): The environment in which to run; options are "sandbox" or "production".
            app_key (Optional[str]): Consumer key for the Mpesa API.
            app_secret (Optional[str]): Consumer secret for the Mpesa API.
            sandbox_url (Optional[str]): URL for Mpesa's sandbox environment.
            live_url (Optional[str]): URL for Mpesa's production environment.
        """
        super().__init__(env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token: Optional[str] = self.authenticate()

    def register(
        self,
        shortcode: int,
        response_type: str,
        confirmation_url: str,
        validation_url: str,
    ) -> Dict[str, Any]:
        """
        Registers confirmation and validation URLs with Mpesa for C2B transactions.

        Args:
            shortcode (int): The shortcode of the organization.
            response_type (str): Default response type if a transaction times out ("Complete" or "Cancel").
            confirmation_url (str): URL that receives confirmation for completed transactions.
            validation_url (str): URL that receives validation requests before transaction confirmation.

        Returns:
            Dict[str, Any]: Parsed JSON response from Mpesa API indicating registration status.

        Raises:
            ValueError: Raised for invalid or unsuccessful response from Mpesa API.
            httpx.HTTPStatusError: Raised for HTTP errors during the request.
        """
        payload = {
            "ShortCode": shortcode,
            "ResponseType": response_type,
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url,
        }

        headers = {
            "Authorization": f"Bearer {self.authentication_token}",
            "Content-Type": "application/json",
        }

        base_url = self.live_url if self.env == "production" else self.sandbox_url
        saf_url = f"{base_url}/mpesa/c2b/v1/registerurl"

        with httpx.Client() as client:
            try:
                response = client.post(saf_url, headers=headers, json=payload)
                response.raise_for_status()  # Raises HTTP errors if status is not 200
                return response.json()
            except httpx.HTTPStatusError as exc:
                print(f"HTTP error during C2B registration: {exc}")
                raise exc

    def simulate(
        self,
        shortcode: int,
        command_id: str,
        amount: int,
        msisdn: int,
        bill_ref_number: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Simulates a C2B transaction with Mpesa using the provided transaction details.

        Args:
            shortcode (int): The shortcode of the organization.
            command_id (str): Unique command type, e.g., "CustomerPayBillOnline" or "CustomerBuyGoodsOnline".
            amount (int): Transaction amount.
            msisdn (int): Phone number initiating the transaction in MSISDN format (12 digits).
            bill_ref_number (Optional[str]): Optional bill reference number for the transaction.

        Returns:
            Dict[str, Any]: Parsed JSON response from the Mpesa API containing transaction details.

        Raises:
            ValueError: Raised for invalid or unsuccessful response from Mpesa API.
            httpx.HTTPStatusError: Raised for HTTP errors during the request.
        """
        payload = {
            "ShortCode": shortcode,
            "CommandID": command_id,
            "Amount": amount,
            "Msisdn": msisdn,
            "BillRefNumber": bill_ref_number,
        }

        headers = {
            "Authorization": f"Bearer {self.authentication_token}",
            "Content-Type": "application/json",
        }

        base_url = self.live_url if self.env == "production" else self.sandbox_url
        saf_url = f"{base_url}/mpesa/c2b/v1/simulate"

        with httpx.Client() as client:
            try:
                response = client.post(saf_url, headers=headers, json=payload)
                response.raise_for_status()  # Raises HTTP errors if status is not 200
                return response.json()
            except httpx.HTTPStatusError as exc:
                print(f"HTTP error during C2B transaction simulation: {exc}")
                raise exc
