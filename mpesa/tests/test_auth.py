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
            app_secret="6O4TaiG8qMdsUjckbWmQPuGY7AaOnaHnYgsrm03ylOBnDF3M9TQYNOYaoxeTrwGq",
        )

        self.token = self.mpesa.authenticate()

    def test_authentication(self):

        self.assertEqual(len(self.token), 28)

if __name__ == "__main__":
    unittest.main()
