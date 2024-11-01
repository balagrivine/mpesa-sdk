import pytest
import respx
from httpx import Response
from mpesa.api.balance import Balance  # Adjust the import path as necessary


@pytest.fixture
def balance_instance():
    # Create an instance of Balance with mock credentials
    return Balance(env="sandbox", app_key="test_key", app_secret="test_secret")


@respx.mock
def test_get_balance_success(balance_instance):
    # Mock the account balance endpoint with a successful response
    respx.post("https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query").mock(
        return_value=Response(
            200,
            json={
                "ResponseCode": "0",
                "ResponseDescription": "Balance retrieved successfully",
            },
        )
    )

    # Call the get_balance method with test data
    response = balance_instance.get_balance(
        initiator="test_initiator",
        security_credential="test_security_credential",
        party_a="600000",
        identifier_type=4,
        remarks="Test balance query",
        queue_timeout_url="https://example.com/timeout",
        result_url="https://example.com/result",
    )

    # Verify the response
    assert response["ResponseCode"] == "0"
    assert response["ResponseDescription"] == "Balance retrieved successfully"


@respx.mock
def test_get_balance_http_error(balance_instance):
    # Mock the account balance endpoint to return a 500 error
    respx.post("https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # Expect an HTTPStatusError due to the 500 response
    with pytest.raises(httpx.HTTPStatusError):
        balance_instance.get_balance(
            initiator="test_initiator",
            security_credential="test_security_credential",
            party_a="600000",
            identifier_type=4,
            remarks="Test balance query",
            queue_timeout_url="https://example.com/timeout",
            result_url="https://example.com/result",
        )


@respx.mock
def test_get_balance_value_error(balance_instance):
    # Test missing app_key and app_secret by creating an instance without them
    incomplete_instance = Balance(env="sandbox")

    # Attempt to check balance with missing credentials
    with pytest.raises(
        ValueError, match="App key and app secret must be provided for authentication."
    ):
        incomplete_instance.get_balance(
            initiator="test_initiator",
            security_credential="test_security_credential",
            party_a="600000",
            identifier_type=4,
            remarks="Test balance query",
            queue_timeout_url="https://example.com/timeout",
            result_url="https://example.com/result",
        )
