import pytest
import respx
from httpx import Response, HTTPStatusError
from mpesa.api.c2b import C2B


@pytest.fixture
def c2b_instance():
    return C2B(env="sandbox", app_key="test_key", app_secret="test_secret")


@respx.mock
def test_register_success(c2b_instance):
    respx.post("https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl").mock(
        return_value=Response(
            200,
            json={"ResponseCode": "0", "ResponseDescription": "Registration success"},
        )
    )

    response = c2b_instance.register(
        shortcode=123456,
        response_type="Completed",
        confirmation_url="https://example.com/confirmation",
        validation_url="https://example.com/validation",
    )

    # Verify the response
    assert response["ResponseCode"] == "0"
    assert response["ResponseDescription"] == "Registration success"


@respx.mock
def test_register_http_error(c2b_instance):
    # Mock the C2B registration endpoint to return a 500 error
    respx.post("https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # Expect an HTTPStatusError due to the 500 response
    with pytest.raises(HTTPStatusError):
        c2b_instance.register(
            shortcode=123456,
            response_type="Completed",
            confirmation_url="https://example.com/confirmation",
            validation_url="https://example.com/validation",
        )


@respx.mock
def test_simulate_success(c2b_instance):
    # Mock the C2B simulation endpoint with a successful response
    respx.post("https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate").mock(
        return_value=Response(
            200, json={"ResponseCode": "0", "ResponseDescription": "Simulation success"}
        )
    )

    # Call the simulate method with test data
    response = c2b_instance.simulate(
        shortcode=123456,
        command_id="CustomerPayBillOnline",
        amount=1000,
        msisdn=254700000000,
        bill_ref_number="TestBillRef",
    )

    # Verify the response
    assert response["ResponseCode"] == "0"
    assert response["ResponseDescription"] == "Simulation success"


@respx.mock
def test_simulate_http_error(c2b_instance):
    # Mock the C2B simulation endpoint to return a 500 error
    respx.post("https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # Expect an HTTPStatusError due to the 500 response
    with pytest.raises(HTTPStatusError):
        c2b_instance.simulate(
            shortcode=123456,
            command_id="CustomerPayBillOnline",
            amount=1000,
            msisdn=254700000000,
            bill_ref_number="TestBillRef",
        )
