import pytest
import respx
from httpx import Response, HTTPStatusError

from mpesa.api.auth import MpesaBase
from mpesa.api.mpesa_express import MpesaExpress

@pytest.fixture
def mock_authentication():
    # Start the `respx` mocker for all requests in the test
    with respx.mock() as respx_mock:
        # Mock the authentication endpoint with a fake response
        respx_mock.get("https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials").mock(
            return_value=Response(
                200,
                json={"access_token": "mock_token", "expires_in": 3599}
            )
        )
        yield

@pytest.fixture
def mpesa_express_instance(mock_authentication):
    # Create an instance of MpesaExpress with mock details
    return MpesaExpress(
        env="sandbox", app_key="test_key", app_secret="test_secret"
    )

@respx.mock
def test_stk_push_success(mpesa_express_instance):
    # Mock the stk push endpoint with a successful response
    respx.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest").mock(
        return_value=Response(
            200,
            json={
                "ResponseCode": "0",
                "ResponseDescription": "Success. Request accepted for processing",
            },
        )
    )

    # Call the stk_push method with test data
    response = mpesa_express_instance.stk_push(
        short_code=600789,
        pass_key="pass_key",
        transaction_type="TransactionType",
        amount=10,
        sender_msisdn="2547000000",
        receiver_msisdn="2547000000",
        callback_url="https://example.com/callback",
        transaction_desc="Test transaction",
        account_ref="Account reference"
    )

    assert response["ResponseCode"] == "0"
    assert response["ResponseDescription"] == "Success. Request accepted for processing"

@respx.mock
def test_stk_push_http_error(mpesa_express_instance):
    # Mock the stk push endpoint to return a 500 error
    respx.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest").mock(
        return_value=Response(
            500,
            json={
                "error": "Internal Server Error"
            },
        )
    )

    # Expect an HTTPStatusError due to the 500 response
    with pytest.raises(HTTPStatusError):
        mpesa_express_instance.stk_push(
            short_code=600798,
            pass_key="pass_key",
            transaction_type="TransactionType",
            amount=10,
            sender_msisdn="2547000000",
            receiver_msisdn="2547000000",
            callback_url="https://example.com/callback",
            transaction_desc="Test transaction",
            account_ref="Account reference"
        )

@respx.mock
def test_stk_push_value_error(mpesa_express_instance):
    # Attempt to simulate stk push with missing credentials
    with pytest.raises(
        ValueError, match="App key and app secret must be provided for authentication."
    ):
        MpesaExpress(env="sandbox").stk_push(
            short_code=600798,
            pass_key="pass-key",
            transaction_type="TransactionType",
            amount=10,
            sender_msisdn="2547000000",
            receiver_msisdn="2547000000",
            callback_url="https://example.com/callback",
            transaction_desc="Test transaction",
            account_ref="Account reference"
         )

@respx.mock
def test_stk_status_success(mpesa_express_instance):
    #Mock the stk query endpoint with a successful response
    respx.post("https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query").mock(
        return_value=Response(
            200,
            json={
                "ResponseCode": "0",
                "ResponseDescription": "The service request has been accepted successfully"
            },
        )
    )

    # Call the status method with test data
    response = mpesa_express_instance.status(
        short_code=600798,
        pass_key="pass_key",
        checkout_request_id="checkout_id"
    )

    assert response["ResponseCode"] == "0"
    assert response["ResponseDescription"] == "The service request has been accepted successfully"

@respx.mock
def test_stk_status_http_error(mpesa_express_instance):
    # Mock the stk status endpoint to return 500 error
    respx.post("https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query").mock(
        return_value=Response(
            500,
            json={
                "error": "Internal server error"
            },
        )
    )

    # Expect an HTTPStatusErrordue to the 500 response
    with pytest.raises(HTTPStatusError):
        mpesa_express_instance.status(
            short_code=600798,
            pass_key="pass_key",
            checkout_request_id="ceckout_id"
        )

@respx.mock
def test_stk_status_value_error(mpesa_express_instance):
    # Test missing app_key and app_secret by creating an instance without them

    with pytest.raises(
        ValueError, match="App key and app secret must be provided for authentication."
    ):
        MpesaExpress(env="sandbox").status(
            short_code=600798,
            pass_key="pass_key",
            checkout_request_id="checkout_id"
        )
