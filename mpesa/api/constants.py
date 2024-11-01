import os

ENV = os.getenv("ENV", "development")

SANDBOX_URL = "https://sandbox.safaricom.co.ke"
LIVE_URL = "https://safaricom.co.ke"

if ENV == "production":
    BASE_URL = LIVE_URL
    APP_KEY = os.getenv("PROD_APP_KEY")
    APP_SECRET = os.getenv("PROD_APP_SECRET")
else:
    BASE_URL = SANDBOX_URL
    APP_KEY = os.getenv("DEV_APP_KEY", "")
    APP_SECRET = os.getenv("DEV_APP_SECRET", "")


# API Endpoints
AUTH_ENDPOINT = f"{SANDBOX_URL}/oauth/v1/generate?grant_type=client_credentials"
ACCOUNT_BALANCE_ENDPOINT = f"{SANDBOX_URL}/mpesa/accountbalance/v1/query"

# Application Credentials
APP_KEY = "your_app_key"  # Replace with your actual app key
APP_SECRET = "your_app_secret"  # Replace with your actual app secret

# Other Constants
RETRY_COUNT = 3
TIMEOUT_SECONDS = 30
