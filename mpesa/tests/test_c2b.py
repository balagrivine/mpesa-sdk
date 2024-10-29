import unittest
import httpx

from mpesa.api.c2b import C2B
from mpesa.api.auth import MpesaBase


class TestC2B(unittest.TestCase):
    def setUp(self):
        self.c2b = C2B(
            env="sandbox",
            app_key="9eYm49Kk89LsZti0oZNsr0gNiASNCseIJLku3keSoVNcwOdh",
            app_secret="6O4TaiG8qMdsUjckbWmQPuGY7AaOnaHnYgsrm03ylOBnDF3M9TQYNOYaoxeTrwGq",
            sandbox_url="https://sandbox.safaricom.co.ke",
            live_url="https://safaricom.co.ke",
        )

        self.token = self.c2b.authenticate()

    def test_register(self):
        response = self.c2b.register(
            shortcode=600992,
            response_type="Completed",
            confirmation_url="https://mydomain.com/confirmation",
            validation_url="https://mydomain.com/validation",
        )

        self.assertEqual(response["ResponseCode"], "0")

    def test_simulate(self):
        response = self.c2b.simulate(
            command_id="CustomerBuyGoodsOnline",
            amount=1,
            msisdn="254708374149",
            bill_ref_number="null",
            shortcode=174379,
        )

        self.assertEqual(response["ResponseCode"], "0")
