import httpx
from typing import Dict, Any
from mpesa.api.auth import MpesaBase


class Balance(MpesaBase):
    def __init__(
        self,
        env: str = "sandbox",
        app_key: str = None,
        app_secret: str = None,
        sandbox_url: str = "https://sandbox.safaricom.co.ke",
        live_url: str = "https://safaricom.co.ke",
    ):
        super().__init__(env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token: str = self.authenticate()

    def get_balance(
        self,
        initiator: str,
        security_credential: str,
        party_a: str,
        identifier_type: int,
        remarks: str,
        queue_timeout_url: str,
        result_url: str,
    ) -> Dict[str, Any]:
        """Requests the account balance of a shortcode (B2C, buy goods, paybill).

        Args:
            initiator (str): Username used to authenticate the transaction.
            security_credential (str): Generated from the developer portal.
            party_a (str): Till number being queried.
            identifier_type (int): Type of organization receiving the transaction.
                                   Options: 1 - MSISDN, 2 - Till Number, 4 -
                                   Organization short code
            remarks (str): Comments sent with the transaction (max 100 characters).
            queue_timeout_url (str): URL that handles timed-out transactions.
            result_url (str): URL that receives results from the M-Pesa API call.

        Returns:
            Dict[str, Any]: Parsed JSON response from API with account balance.

        Raises:
            httpx.HTTPStatusError: Raised for HTTP errors during the request.
            ValueError: Raised for invalid or unsuccessful responses from M-Pesa API.
        """
        payload = self._construct_payload(
            initiator,
            security_credential,
            party_a,
            identifier_type,
            remarks,
            queue_timeout_url,
            result_url,
        )

        headers = self._construct_headers()

        saf_url = self._get_saf_url()

        with httpx.Client() as client:
            try:
                response = client.post(saf_url, headers=headers, json=payload)
                response.raise_for_status()

                return response.json()
            except httpx.HTTPStatusError as http_err:
                raise http_err
            except (httpx.RequestError, ValueError) as e:
                raise ValueError(
                    "An error occurred during the balance query process."
                ) from e

    def _construct_payload(
        self,
        initiator: str,
        security_credential: str,
        party_a: str,
        identifier_type: int,
        remarks: str,
        queue_timeout_url: str,
        result_url: str,
    ) -> Dict[str, Any]:
        """Constructs the payload for the balance request."""
        return {
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID": "AccountBalance",
            "PartyA": party_a,
            "IdentifierType": identifier_type,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
        }

    def _construct_headers(self) -> Dict[str, str]:
        """Constructs the headers for the API request."""
        return {
            "Authorization": f"Bearer {self.authentication_token}",
            "Content-Type": "application/json",
        }

    def _get_saf_url(self) -> str:
        """Determines the base URL based on the environment."""
        base_url = self.live_url if self.env == "production" else self.sandbox_url
        return f"{base_url}/mpesa/accountbalance/v1/query"


# Set a breakpoint here to inspect the balance retrieval process.
