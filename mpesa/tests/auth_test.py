import pytest
import respx
from httpx import Response
from mpesa.api import MpesaBase  # Ensure MpesaBase is accessible in your import path


@pytest.fixture
def mpesa_instance():
    # Provides an instance of MpesaBase with mock credentials for testing
    return MpesaBase(env="sandbox", app_key="test_key", app_secret="test_secret")


@respx.mock
def test_authenticate_success(mpesa_instance):
    # Mock the URL for the authentication endpoint
    respx.get(
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    ).mock(return_value=Response(200, json={"access_token": "mock_token"}))

    # Run the authenticate method and verify the token
    token = mpesa_instance.authenticate()
    assert token == "mock_token"
    assert mpesa_instance.token == "mock_token"


@respx.mock
def test_authenticate_missing_credentials():
    # Test with missing credentials, expecting a ValueError
    with pytest.raises(ValueError, match="App key and app secret must be provided"):
        MpesaBase(env="sandbox").authenticate()


@respx.mock
def test_authenticate_failure_401(mpesa_instance):
    # Mock an unsuccessful response (401 Unauthorized)
    respx.get(
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    ).mock(return_value=Response(401, json={"error": "invalid_client"}))

    # Expect an HTTPStatusError due to unauthorized access
    with pytest.raises(Exception) as exc_info:
        mpesa_instance.authenticate()
    assert exc_info.value.response.status_code == 401


@respx.mock
def test_authenticate_no_access_token_in_response(mpesa_instance):
    # Mock a successful response but without an access token in the JSON
    respx.get(
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    ).mock(return_value=Response(200, json={}))

    # Expect a ValueError if access token is not in the response
    with pytest.raises(
        ValueError, match="Authentication failed: access_token not found in response"
    ):
        mpesa_instance.authenticate()
