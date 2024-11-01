import pytest
import respx
from httpx import Response
from mpesa.api.b2c import B2C  # Adjust this import path if necessary


@pytest.fixture
def b2c_instance():
    # Mock credentials and instance of B2C for testing
    return B2C(env="sandbox", app_key="test_key", app_secret="test_secret")


@respx.mock
def test_transact_success(b2c_instance):
    # Mock the B2C endpoint with a successful response
    respx.post("https://sandbox.safaricom.co.ke/mpesa/b2c/v3/paymentrequest").mock(
        return_value=Response(
            200, json={"ResponseCode": "0", "ResponseDescription": "Success"}
        )
    )

    # Call transact with test data
    response = b2c_instance.transact(
        originator_conversation_id="12345",
        initiator_name="test_initiator",
        security_credential="test_credential",
        command_id="BusinessPayment",
        amount="1000",
        party_a=600123,
        party_b=254700000000,
        remarks="Test Transaction",
        queue_timeout_url="https://example.com/timeout",
        result_url="https://example.com/result",
        occassion="Test",
    )

    # Assertions to verify the response
    assert response["ResponseCode"] == "0"
    assert response["ResponseDescription"] == "Success"


@respx.mock
def test_transact_http_error(b2c_instance):
    # Mock the B2C endpoint to return a 500 error
    respx.post("https://sandbox.safaricom.co.ke/mpesa/b2c/v3/paymentrequest").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # Expect an HTTPStatusError due to the 500 response
    with pytest.raises(httpx.HTTPStatusError):
        b2c_instance.transact(
            originator_conversation_id="12345",
            initiator_name="test_initiator",
            security_credential="test_credential",
            command_id="BusinessPayment",
            amount="1000",
            party_a=600123,
            party_b=254700000000,
            remarks="Test Transaction",
            queue_timeout_url="https://example.com/timeout",
            result_url="https://example.com/result",
            occassion="Test",
        )


@respx.mock
def test_transact_missing_token():
    # Test that a missing authentication token raises an error
    with pytest.raises(
        ValueError, match="An error occurred during the transaction process"
    ):
        B2C(env="sandbox").transact(
            originator_conversation_id="12345",
            initiator_name="test_initiator",
            security_credential="test_credential",
            command_id="BusinessPayment",
            amount="1000",
            party_a=600123,
            party_b=254700000000,
            remarks="Test Transaction",
            queue_timeout_url="https://example.com/timeout",
            result_url="https://example.com/result",
            occassion="Test",
        )
