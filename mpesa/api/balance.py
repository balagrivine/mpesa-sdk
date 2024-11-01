import httpx
from typing import Dict, Any, Optional
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

        """Reqests the account balance of a shortcode (B2C, buy goods, paybill).

        Args:
            initiator (str): Username used to authenticate the transaction.
            security_credential (str): Generate from developer portal.
            party_a (int): Till number being queried.
            identifier_type (int): Type of organization receiving the transaction.
                                   Options: 1 - MSISDN 2 - Till Number  4 - Organization short code
            remarks (str): Comments that are sent along with the transaction(maximum 100 characters).
            queue_timeout_url (str): The url that handles information of timed out transactions.
            result_url (str): The url that receives results from M-Pesa api call.

        Returns:
            Dict[str, Any]: Parsed JSON response from API with account balance

        Raises:
            httpx.HTTPStatuserror: Raised for HTTP errors during the request
            ValueError: Raised for invalid or unsuccessful response from Mpesa API
        """
        payload = {
            "Initiator": initiator,
            "SecurityCredential": security_credential,
            "CommandID": "AccountBalance",
            "PartyA": party_a,
            "IdentifierType": identifier_type,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
        }

        headers = {
            "Authorization": f"Bearer {self.authentication_token}",
            "Content-Type": "application/json",
        }

        # Determine base url based on the environment
        base_url = self.live_url if self.env == "production" else self.sandbox_url
        saf_url = f"{base_url}/mpesa/accountbalance/v1/query"

        with httpx.Client() as client:
            try:
                response = client.post(saf_url, headers=headers, json=payload)
                response.raise_for_status()

                return response.json()
            except httpx.HTTPStatusError as http_err:
                print(
                    f"HTTP error occured while getting account balance: {response.json()}"
                )
                raise http_err

            except (httpx.RequestError, ValueError) as e:
                raise ValueError(
                    "An error occured during the balance query process."
                ) from e
