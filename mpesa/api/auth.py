from typing import Optional
import httpx


class MpesaBase:
    """
    MpesaBase is a utility class for interacting with Mpesa's authentication service.
    It enables fetching an access token required for making secure API calls to Mpesa.
    This access token is generated using the Basic Auth method over HTTPS.

    Attributes:
        env (str): Specifies the environment, either "sandbox" or "production".
        app_key (str): Consumer key obtained from the Mpesa developer portal.
        app_secret (str): Consumer secret obtained from the Mpesa developer portal.
        sandbox_url (str): Base URL for Mpesa's sandbox environment.
        live_url (str): Base URL for Mpesa's production environment.
        token (Optional[str]): Access token obtained upon successful authentication.

    Methods:
        authenticate() -> Optional[str]: Authenticates with Mpesa and retrieves an access token.
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
        Initializes an instance of MpesaBase with the specified environment and credentials.

        Args:
            env (str): Environment to use; options are "sandbox" or "production".
            app_key (Optional[str]): Consumer key from Mpesa's developer portal.
            app_secret (Optional[str]): Consumer secret from Mpesa's developer portal.
            sandbox_url (str): URL for the sandbox environment (default is Safaricom's sandbox).
            live_url (str): URL for the live production environment (default is Safaricom's live URL).
        """
        self.env = env
        self.app_key = app_key
        self.app_secret = app_secret
        self.sandbox_url = sandbox_url
        self.live_url = live_url
        self.token: Optional[str] = None

    def authenticate(self) -> Optional[str]:
        """
        Authenticates with the Mpesa API using Basic Auth and fetches an access token.
        The token obtained is stored in the `self.token` attribute for reuse in other
        API calls.

        The method dynamically chooses the appropriate environment URL based on the
        `env` attribute.
        It raises an HTTPStatusError for any unsuccessful responses, ensuring error
        awareness.

        Returns:
            Optional[str]: The access token to be used with the "Bearer" authorization
            header
                           for subsequent API requests, or None if authentication fails.

        Raises:
            ValueError: Raised if app_key or app_secret is not provided.
            httpx.HTTPStatusError: Raised if the authentication request returns a
            non-200 status code.
        """
        # Validation for required credentials
        if not self.app_key or not self.app_secret:
            raise ValueError(
                "App key and app secret must be provided for authentication."
            )

        # Determine the base URL based on the environment
        base_url = self.live_url if self.env == "production" else self.sandbox_url
        auth_url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"

        # Setting up Basic Auth credentials
        auth = httpx.BasicAuth(username=self.app_key, password=self.app_secret)

        with httpx.Client() as client:
            try:
                response = client.get(auth_url, auth=auth)
                response.raise_for_status()

                # Parsing access token from JSON response
                token_data = response.json()
                self.token = token_data.get("access_token")

                if not self.token:
                    raise ValueError(
                        "Authentication failed: access_token not found in response."
                    )

                return self.token

            except httpx.HTTPStatusError as http_err:
                # Handle and log any HTTP errors, providing feedback on status code and
                # URL
                print(f"{http_err.response.status_code} - {http_err.request.url}")
                raise http_err

            except (httpx.RequestError, ValueError) as e:
                # Handle general request or parsing errors, with descriptive
                # error logging
                print(f"An error occurred during authentication: {e}")
                raise e
