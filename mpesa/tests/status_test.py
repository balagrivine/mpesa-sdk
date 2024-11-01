import pytest
import respx
from httpx import Response
from mpesa.api.status import TransactionStatus  # Adjust the import path as necessary


@pytest.fixture
def transaction_status_instance():
    # Create an instance of TransactionStatus with mock credentials
    return TransactionStatus(
        env="sandbox", app_key="test_key", app_secret="test_secret"
    )


@respx.mock
def test_check_transaction_status_success(transaction_status_instance):
    # Mock the transaction status endpoint with a successful response
    respx.post("https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query").mock(
        return_value=Response(
            200,
            json={
                "ResponseCode": "0",
                "ResponseDescription": "Transaction status retrieved",
            },
        )
    )

    # Call the check_transaction_status method with test data
    response = transaction_status_instance.check_transaction_status(
        security_credential="test_security_credential",
        originator_conversation_id="test_originator_id",
        party_a="254700000000",
        identifier_type="1",
        transaction_id="test_transaction_id",
        remarks="Test transaction status",
        initiator="test_initiator",
        result_url="https://example.com/result",
        queue_timeout_url="https://example.com/timeout",
    )

    # Verify the response
    assert response["ResponseCode"] == "0"
    assert response["ResponseDescription"] == "Transaction status retrieved"


@respx.mock
def test_check_transaction_status_http_error(transaction_status_instance):
    # Mock the transaction status endpoint to return a 500 error
    respx.post("https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # Expect an HTTPStatusError due to the 500 response
    with pytest.raises(httpx.HTTPStatusError):
        transaction_status_instance.check_transaction_status(
            security_credential="test_security_credential",
            originator_conversation_id="test_originator_id",
            party_a="254700000000",
            identifier_type="1",
            transaction_id="test_transaction_id",
            remarks="Test transaction status",
            initiator="test_initiator",
            result_url="https://example.com/result",
            queue_timeout_url="https://example.com/timeout",
        )


@respx.mock
def test_check_transaction_status_value_error(transaction_status_instance):
    # Test missing app_key and app_secret by creating an instance without them
    incomplete_instance = TransactionStatus(env="sandbox")

    # Attempt to check transaction status with missing credentials
    with pytest.raises(
        ValueError, match="App key and app secret must be provided for authentication."
    ):
        incomplete_instance.check_transaction_status(
            security_credential="test_security_credential",
            originator_conversation_id="test_originator_id",
            party_a="254700000000",
            identifier_type="1",
            transaction_id="test_transaction_id",
            remarks="Test transaction status",
            initiator="test_initiator",
            result_url="https://example.com/result",
            queue_timeout_url="https://example.com/timeout",
        )
