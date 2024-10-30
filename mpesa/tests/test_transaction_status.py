import unittest
from uuid import uuid4
from mpesa.api.status import TransactionStatus

class TransactionStatusTests(unittest.TestCase):
    def setUp(self):
        self.transaction_status = TransactionStatus(
                env="sandbox",
                app_key="9eYm49Kk89LsZti0oZNsr0gNiASNCseIJLku3keSoVNcwOdh",
                app_secret="6O4TaiG8qMdsUjckbWmQPuGY7AaOnaHnYgsrm03ylOBnDF3M9TQYNOYaoxeTrwGq",
                sandbox_url="https://sandbox.safaricom.co.ke",
                live_url="https://safaricom.co.ke"
            )

    def test_check_transaction_status(self):
        self.response = self.transaction_status.check_transaction_status(
                originator_conversation_id="AG_20241030_2010611f815ef2bc5329",
                party_a="600798",
                initiator="testapiuser",
                identifier_type=4,
                remarks="OK",
                security_credential="LpQlISX5ZnNW1QCRygMG03kd9tJxMjk78XGqVDkPplXJPboMcAIA4L0pa+r9HAo5PdyXhUAqU0GYmKWpss23Jm+jQ0Z5ZFMrtEjpPRUpSAtj+xD5c/9cWUDz46AorbDWryXquXGTGtwsDm/sI+qvNnVtXiDkO58MS/DVT4HTEt3LO0jLmq39ZumIv5XnPyC8bOEpZFVkR+12VdeAX1ittYvZJH26pZekVjFYU1kRcvTC7F3OsYW3qUfQaUmytkCF8FH5dhoU7AeydP3OR6U/QHXZkg9sSC7C8BldHcB+1XVveoi25+D/G9D+bwxP+JTc/CzDaWLcB0E1Ueodsy9sXw==",
                transaction_id="LKXXXX1234",
                queue_timeout_url="https://mydomain.com/TransactionStatus/queue/",
                result_url="https://mydomain.com/TransactionStatus/result/"
            )
        self.assertIn("Accept the service request successfully.", self.response)

if __name__ == "__main__":
    unittest.main()
