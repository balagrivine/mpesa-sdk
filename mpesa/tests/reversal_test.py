import pytest
import respx
from httpx import HTTPStatusError, Response

from mpesa.api.reversal import Reversal


@pytest.fixture
def mock_authentication():
    with respx.mock() as respx_mock:
        # Mock the authentication endpoint with a fake response
        respx_mock.get("https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials").mock(
            return_value=Response(
                200,
                json={
                    "access_token": "mock_token",
                    "expires_in": 3599
                }
            )
        )
        yield

@pytest.fixture
def reversal_instance(mock_authentication):
    # Create an instance of reversal class with mock details

    return Reversal(
        env="sandbox", app_key="test_key", app_secret="test_secret"
    )

@respx.mock
def test_reversal_success(reversal_instance):
    # Mock the reversal API endpoint to return 200 success code
    respx.post("https://sandbox.safaricom.co.ke/mpesa/reversal/v1/request").mock(
        return_value=Response(
            200,
            json={
                "ResponseCode": "0",
                "ResponseDescription": "Accept the service request successfully."
            }
        )
    )

    response = reversal_instance.reverse(
        receiver=600798,
        initiator="testapi",
        security_credential="security_credential",
        transaction_id="transaction_id",
        amount=10,
        timeout_url="https://example.com/timeout",
        result_url="https://example.com/result",
        occasion="Test reversal",
        remarks="Remarks",
        receiver_identifier="11"
    )

    assert response["ResponseCode"] == "0"
    assert response["ResponseDescription"] == "Accept the service request successfully."

@respx.mock
def test_reversal_http_error(reversal_instance):
    # Mock the reversal endpoint to return 500 error code
    respx.post("https://sandbox.safaricom.co.ke/mpesa/reversal/v1/request").mock(
        return_value=Response(
            500,
            json={"error": "Internal server error"}
        )
    )

    with pytest.raises(HTTPStatusError):
        reversal_instance.reverse(
            receiver=600798,
            initiator="testapi",
            security_credential="security_credential",
            transaction_id="transaction_id",
            amount=10,
            timeout_url="https://example.com/timeout",
            result_url="https://example.com/result",
            occasion="Test reversal",
            remarks="Remarks",
            receiver_identifier="11"
        )
