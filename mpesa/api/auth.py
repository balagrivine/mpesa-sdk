import httpx

class MpesaBase:
    def __init__(self, env="sandbox", app_key=None, app_secret=None, sandbox_url="https://sandbox.safaricom.co.ke",
                 live_url="https://safaricom.co.ke"):
        self.env = env
        self.app_key = app_key
        self.app_secret = app_secret
        self.sandbox_url = sandbox_url
        self.live_url = live_url
        self.token = None

    def authenticate(self):
        """To make Mpesa API calls, you will need to authenticate your app. This method is used to fetch the access token
        required by Mpesa. Mpesa supports client_credentials grant type. To authorize your API calls to Mpesa,
        you will need a Basic Auth over HTTPS authorization token. The Basic Auth string is a base64 encoded string
        of your app's consumer key and consumer secret.

            **Args:**
                - env (str): Current app environment. Options: sandbox, live.
                - app_key (str): The consumer key obtained from the developer portal.
                - app_secret (str): The consumer secret obtained from the developer portal.
                - sandbox_url (str): Base Safaricom sandbox url.
                - live_url (str): Base Safaricom live url.

            **Returns:**
                - access_token (str): This token is to be used with the Bearer header for further API calls to Mpesa.

            """
        if self.env == "production":
            base_url = self.live_url
        else:
            base_url = self.sandbox_url

        auth_uri = "/oauth/v1/generate?grant_type=client_credentials"
        auth_url = f"{base_url}{auth_uri}"

        with httpx.Client() as client:
            try:
                auth = httpx.BasicAuth(username=self.app_key, password=self.app_secret)
                response = client.get(auth_url, auth=auth).raise_for_status()

                if response.status_code==200:
                    self.token = response.json()['access_token']
                    return self.token
            except httpx.HTTPStatusError as exc:
                raise exc
