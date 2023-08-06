import unittest
from ping.api_resources import payments_api
from ping.payments_api import PaymentsApi
import os
from dotenv import load_dotenv

class testHelper(unittest.TestCase):
    load_dotenv()
    def run_tests(self, response, status = 200):
        self.assertIsNotNone(response)
        if status > 204:
            self.assertEqual(response.status_code, status)
            self.assertFalse(response.is_success())
            self.assertTrue(response.is_error())
            self.assertIsNotNone(response.body)
        else:
            self.assertEqual(response.status_code, status)
            self.assertFalse(response.is_error())
            self.assertTrue(response.is_success())
            self.assertIsNotNone(response.body)
            self.assertIsNone(response.errors)


    def api_is_connected():
        payments_api = PaymentsApi(os.getenv("TENANT_ID"))
        ping = payments_api.ping.ping_the_api()
        return True if ping.body == "pong" else False