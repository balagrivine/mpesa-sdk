import unittest
import httpx

from mpesa.api.auth import MpesaBase

class TestAuth(unittest.TestCase):

    def setUp(self):

        # app_key and app_secret are simulator credentials hence pose no security risk
        # when included in this code
        self.mpesa = MpesaBase(
                env="sandbox",
                app_key="9eYm49Kk89LsZti0oZNsr0gNiASNCseIJLku3keSoVNcwOdh",
                app_secret="6O4TaiG8qMdsUjckbWmQPuGY7AaOnaHnYgsrm03ylOBnDF3M9TQYNOYaoxeTrwGq"
                )

    def test_authentication(self):
        token = self.mpesa.authenticate()

        self.assertEqual(len(token), 28)

    def test_invalid_credentials(self):
        self.mpesa.app_key = "invalid_app_key"
        self.mpesa.app_secret = "invalid_app_secret"

        with self.assertRaises(httpx.HTTPStatusError) as exc:
            self.mpesa.authenticate()

        self.assertIn("400 Bad Request", str(exc.exception))

if __name__ == "__main__":
    unittest.run()
