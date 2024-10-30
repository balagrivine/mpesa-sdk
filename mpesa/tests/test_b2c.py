import unittest
from uuid import uuid4

from mpesa.api.b2c import B2C


class TestB2C(unittest.TestCase):
    def setUp(self):
        self.b2c = B2C(
            "sandbox",
            app_key="9eYm49Kk89LsZti0oZNsr0gNiASNCseIJLku3keSoVNcwOdh",
            app_secret="6O4TaiG8qMdsUjckbWmQPuGY7AaOnaHnYgsrm03ylOBnDF3M9TQYNOYaoxeTrwGq",
            sandbox_url="https://sandbox.safaricom.co.ke",
            live_url="https://safaricom.co.ke",
        )

    def test_transact(self):
        conversation_id = str(uuid4())
        response = self.b2c.transact(
            originator_conversation_id=conversation_id,
            initiator_name="testapi",
            security_credential="T1NPOb3DhjM0Z8+ko2/ctFrpGVwgRZMSBWqaiD6PEmptHeAlufsRbtc6ZuKgojrPmfy4I5n8bOgROmJyvX8ml5qUCm8tE+EjlgwcPorVIU2SZX2DdSwRmPO4bpaoJm/gPDhv5EkIxikNGmdAabwXAjZ/SmICfv37GZGkFGSBouy0mHFIYcDbg9PirCDtfOIb3mnVBgWN+dtVDvn8/w0Q7lXAEQGMyWnVrrN1XL9uDMeJ/t+42wtjjMXHcsSFXas9K/ZZxFqc9D6ogL4nl+2L6dSNNMTs+xtm2wS+hqQmgobE0lQdkcuLB/0n+KWYCcAb7kfSCRicVCUKRAowre+mTg==",
            command_id="BusinessPayment",
            amount=10,
            party_a=600998,
            party_b=254708374149,
            remarks="Testing b2c payment",
            queue_timeout_url="https://mydomain.com/b2c/queue",
            result_url="https://mydomain.com/b2c/result",
            occassion="Testing occassions.",
        )

        self.assertEqual(response["OriginatorConversationID"], conversation_id)

if __name__ == "__main__":
    unittest.main()
