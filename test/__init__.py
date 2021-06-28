import unittest

from faker import Faker
from flask import json

from config import ConfigTest
from flaskr import create_app


class DefaultTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        # This is already calling setup_db to the test DB
        self.app = create_app(test_config=ConfigTest())
        self.client = self.app.test_client
        self.db = self.app.db
        self.db.drop_all()
        self.db.create_all()
        self.TOKEN_ACCOUNTANT = 'some tokens here'
        self.TOKEN_SECRETARY = 'some tokens here'
        self.faker = Faker()

    def tearDown(self):
        """Executed after each test"""
        self.db.session.close()

    @staticmethod
    def _print_when_different_error(response, expected_status_code):
        if response.status_code == expected_status_code:
            return
        try:
            body = json.loads(response.data)
            message = body['message']
            print(message)
        except Exception:
            print(response.data)

    def assert_200(self, response):
        self._print_when_different_error(response, 200)
        self.assertEqual(200, response.status_code)
        body = json.loads(response.data)
        self.assertTrue(body['success'])

    def assert_400(self, response):
        self._print_when_different_error(response, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(response.status_code, 400)

    def assert_401(self, response):
        self._print_when_different_error(response, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 401)
        self.assertIsNotNone(data['message'])
        self.assertEqual(response.status_code, 401)

    def assert_403(self, response):
        self._print_when_different_error(response, 403)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(403, data['error'])
        self.assertEqual(403, response.status_code)

    def assert_404(self, response):
        self._print_when_different_error(response, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'No matching resources was found')
        self.assertEqual(response.status_code, 404)

    def assert_422(self, response):
        self._print_when_different_error(response, 422)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(422, response.status_code)

    def assert_custom_error(self, response, status_code, message):
        self._print_when_different_error(response, status_code)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(status_code, data['error'])
        self.assertEqual(message, data['message'])
        self.assertEqual(response.status_code, status_code)

    @staticmethod
    def view_message_if_fail(response):
        status_code = response.status_code
        if status_code == 200:
            return
        try:
            response = json.loads(response.data)
            if not response['success']:
                if 'message' in response:
                    print('Error {}: {}'.format(status_code, response['message']))
                else:
                    print(response)
        except Exception:
            print('Error {}: {}'.format(status_code, response.data))
