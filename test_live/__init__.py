import unittest
import requests
from faker import Faker
from models.enum import AccountTypeEnum

from test.tokens import TOKEN_ACCOUNTANT

API_URL = 'https://ny-volako.herokuapp.com'


class TestLive(unittest.TestCase):

    def setUp(self) -> None:
        self.faker = Faker()

    def test_accountant(self):
        self.delete_all_accounts()
        account_type = AccountTypeEnum.drawing.name
        account_name = self.faker.name()
        response = requests.post(API_URL + '/accounts', json={'name': account_name,
                                                              'type': account_type},
                                 headers={'Authorization': 'bearer ' + TOKEN_ACCOUNTANT})
        self.assertEqual(200, response.status_code)

        response = requests.get(API_URL + '/accounts',
                                headers={'Authorization': 'bearer ' + TOKEN_ACCOUNTANT})
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertTrue('objects' in data)
        self.assertEqual(1, len(data['objects']))
        self.assertEqual(account_name, data['objects'][0]['name'])
        self.assertEqual(account_type, data['objects'][0]['type'])

    def delete_all_accounts(self):
        response = requests.get(API_URL + '/accounts',
                                headers={'Authorization': 'bearer ' + TOKEN_ACCOUNTANT})
        if response.status_code == 404:
            return
        self.delete_all_transactions()
        self.assertEqual(200, response.status_code)
        accounts = response.json()['objects']
        for account in accounts:
            response = requests.delete('{}/accounts/{}'.format(API_URL, account['id']),
                                       headers={'Authorization': 'bearer ' + TOKEN_ACCOUNTANT})
            self.assertEqual(200, response.status_code)

    def delete_all_transactions(self):
        response = requests.get(API_URL + '/transactions',
                                headers={'Authorization': 'bearer ' + TOKEN_ACCOUNTANT})
        if response.status_code == 404:
            return
        self.assertEqual(200, response.status_code)
        transactions = response.json()['objects']
        for transaction in transactions:
            response = requests.delete('{}/transactions/{}'.format(API_URL, transaction['id']),
                                       headers={'Authorization': 'bearer ' + TOKEN_ACCOUNTANT})
            self.assertEqual(200, response.status_code)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
