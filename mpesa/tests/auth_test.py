import pytest
import respx
from httpx import Response, HTTPStatusError
from mpesa.api.auth import MpesaBase
from mpesa.api.constants import AUTH_ENDPOINT


@pytest.fixture
def mpesa_instance():
    """Provides an instance of MpesaBase with mock credentials for testing."""
    return MpesaBase(env="sandbox", app_key="test_key", app_secret="test_secret")


def mock_authenticate_response(status_code, json_data):
    """Helper function to mock the authentication response."""
    respx.get(AUTH_ENDPOINT).mock(return_value=Response(status_code, json=json_data))


@respx.mock
def test_authenticate_success(mpesa_instance):
    """Test successful authentication and token retrieval."""
    mock_authenticate_response(200, {"access_token": "mock_token"})

    # Run the authenticate method and verify the token
    token = mpesa_instance.authenticate()
    assert token == "mock_token"
    assert mpesa_instance.token == "mock_token"


@respx.mock
def test_authenticate_missing_credentials():
    """Test authentication with missing credentials, expecting a ValueError."""
    with pytest.raises(ValueError, match="App key and app secret must be provided"):
        MpesaBase(env="sandbox").authenticate()


@respx.mock
def test_authenticate_failure_401(mpesa_instance):
    """Test authentication failure due to 401 Unauthorized response."""
    mock_authenticate_response(401, {"error": "invalid_client"})

    # Expect an HTTPStatusError due to unauthorized access
    with pytest.raises(HTTPStatusError) as exc_info:
        mpesa_instance.authenticate()

    assert exc_info.value.response.status_code == 401


@respx.mock
def test_authenticate_no_access_token_in_response(mpesa_instance):
    """Test authentication response without access token."""
    mock_authenticate_response(200, {})

    # Expect a ValueError if access token is not in the response
    with pytest.raises(
        ValueError, match="Authentication failed: access_token not found in response"
    ):
        mpesa_instance.authenticate()
