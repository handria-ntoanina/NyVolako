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
        self.TOKEN_ACCOUNTANT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBwWmxGaGxKb1V1TU45UEpGQ3k2NCJ9.eyJpc3MiOiJodHRwczovL2tvdG9nYXN5LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMTkzNDYyODU4ODA2Mzc0NjM5OSIsImF1ZCI6Imh0dHBzOi8vbnl2b2xha28ubW9kZXJuYW50Lm1nIiwiaWF0IjoxNjI1MDQzOTI0LCJleHAiOjE2MjUxMTU5MjQsImF6cCI6ImZxTEtXV0lmbkt4cmFFbmpjRkNKMFd4eFZWckhvQXllIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhY2NvdW50czpkZWxldGUiLCJhY2NvdW50czpnZXQiLCJhY2NvdW50czpuZXciLCJhY2NvdW50czp1cGRhdGUiLCJ0cmFuc2FjdGlvbnM6ZGVsZXRlIiwidHJhbnNhY3Rpb25zOmdldCIsInRyYW5zYWN0aW9uczpuZXciLCJ0cmFuc2FjdGlvbnM6dXBkYXRlIl19.14rXbmONVH7Dk8HBHW2qbHs0etp29nHBGS0aM9nPkEMcEXQLg1UJblvG_MTG4mKe7_W0HfGCAfpbfzdw8bxpdDzcYim82hA2NZ_uNM-6FdIWFPJY7FAG0CJMavixJWVXjzBN3EVbrA4pYyFKZJZ5ou27Vwf13_lif9s9vT68dluXGtMozfxij0KOa_Y0cyAMk76RbfxiDFgs6ivAgjuvgkR-rbkoccNDol2V7TTZSGsemNeGjx5CP6y_tjlbl154PMB6LXli7b1eGIVY4NgojntZnTKJT_cxzLKDPykkPBtbHyDVGCGa08egvp6X6rs8mUgacVYcgAe-1bL_YKNWQQ"
        self.TOKEN_SECRETARY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBwWmxGaGxKb1V1TU45UEpGQ3k2NCJ9.eyJpc3MiOiJodHRwczovL2tvdG9nYXN5LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGRiOWE3YjA2MDViMjAwNzJkNjQ1MGYiLCJhdWQiOiJodHRwczovL255dm9sYWtvLm1vZGVybmFudC5tZyIsImlhdCI6MTYyNTA0NDAzOSwiZXhwIjoxNjI1MTE2MDM5LCJhenAiOiJmcUxLV1dJZm5LeHJhRW5qY0ZDSjBXeHhWVnJIb0F5ZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWNjb3VudHM6Z2V0IiwidHJhbnNhY3Rpb25zOmdldCIsInRyYW5zYWN0aW9uczpuZXciXX0.A72zGWvCVJ-0zaJwRPVba2J5y2e3f4dWeoRnL_eF3h_KMAsn46Db7tRP5DzmZFyUvLK0yQH0q7Ina832D8mW5ZzFiIWOcnEIe4pd0dBrQdJWLhLoR2S9zLHpHzIjGQ3u7Xelm0LbkRpW4DD3fj-M3wRMC1Yz2HPvlRoSM6fwv3Wb8tXsOKlaBC_IOmZ8bKml2MASPvz6IqQZNCfaOZgAT4og9K3sPszFGSZChGM3r_ffVmVnd7MyrbcJmgpupNWkOXUaD-tPV7frc7T6GqVXkxgK_83rHtLLYC9Gbqg3bmTmuHAHDBzAYsLkAn-qd8Xaixf861Rl9lL9zkUsKNqwVg"
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
