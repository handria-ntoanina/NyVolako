import json
import unittest
import datetime
import uuid

from models import Account, AccountTypeEnum, Movement, Transaction
from test import DefaultTestCase


class RbacTestCase(DefaultTestCase):
    """
    Accountant:
        Manages accounts,
        post new transactions, update transactions, delete transactions, get transactions
    Secretary:
        Post new transactions
        View accounts
        View transactions
    """

    def test_accountant_add_account(self):
        response = self.add_account(self.TOKEN_ACCOUNTANT)
        self.view_message_if_fail(response)
        self.assert_200(response)

    def add_account(self, token):
        Account.query.delete()
        self.db.session.commit()
        name = self.faker.name()
        account_type = AccountTypeEnum.equity
        response = self.client().post('/accounts', json={'name': name, 'type': account_type.name},
                                      headers={'Authorization': 'bearer ' + token})
        return response

    def test_accountant_update_account(self):
        response = self.update_account(self.TOKEN_ACCOUNTANT)
        self.view_message_if_fail(response)
        self.assert_200(response)

    def update_account(self, token):
        response = self.add_account(self.TOKEN_ACCOUNTANT)
        self.view_message_if_fail(response)
        self.assert_200(response)
        response = self.client().get('/accounts',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        data = json.loads(response.data)
        to_update = data['objects'][0]
        to_update['name'] = self.faker.name()
        to_update['type'] = AccountTypeEnum.drawing.name
        response = self.client().patch('/accounts/{}'.format(to_update['id']), json=to_update,
                                       headers={'Authorization': 'bearer ' + token})
        return response

    def test_accountant_delete_account(self):
        response = self.delete_account(self.TOKEN_ACCOUNTANT)
        self.view_message_if_fail(response)
        self.assert_200(response)

    def delete_account(self, token):
        response = self.add_account(self.TOKEN_ACCOUNTANT)
        self.view_message_if_fail(response)
        self.assert_200(response)
        response = self.client().get('/accounts',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        data = json.loads(response.data)
        to_delete = data['objects'][0]
        response = self.client().delete('/accounts/{}'.format(to_delete['id']),
                                        headers={'Authorization': 'bearer ' + token})
        return response

    def test_accountant_get_accounts(self):
        response = self.get_accounts(self.TOKEN_ACCOUNTANT)
        self.view_message_if_fail(response)
        self.assert_200(response)

    def get_accounts(self, token):
        Account.query.delete()
        account = Account(name=self.faker.name(), type=AccountTypeEnum.asset)
        self.db.session.add(account)
        self.db.session.commit()
        response = self.client().get('/accounts',
                                     headers={'Authorization': 'bearer ' + token})
        return response

    def test_accountant_post_new_transaction(self):
        response = self.post_new_transaction(self.TOKEN_ACCOUNTANT)
        self.view_message_if_fail(response)
        self.assert_200(response)

    def post_new_transaction(self, token):
        Movement.query.delete()
        Transaction.query.delete()
        Account.query.delete()
        self.db.session.commit()
        bank_account = Account(name='Bank', type=AccountTypeEnum.asset)
        sales_account = Account(name='Sales', type=AccountTypeEnum.revenue)
        self.db.session.add(bank_account)
        self.db.session.add(sales_account)
        self.db.session.commit()
        new_transaction = {'date': (datetime.datetime.now()),
                           'description': (self.faker.name()),
                           'movements': [
                               {'account_id': bank_account.id,
                                'amount': 150},
                               {'account_id': sales_account.id,
                                'amount': 150}
                           ]}
        response = self.client().post('/transactions', json=new_transaction,
                                      headers={'Authorization': 'bearer ' + token})
        return response

    def test_accountant_update_transaction(self):
        response = self.update_transaction(self.TOKEN_ACCOUNTANT)
        self.view_message_if_fail(response)
        self.assert_200(response)

    def update_transaction(self, token):
        self.post_new_transaction(self.TOKEN_ACCOUNTANT)
        response = self.client().get('/transactions',
                                     headers={'Authorization': 'bearer ' + token})
        self.view_message_if_fail(response)
        self.assert_200(response)
        transactions = json.loads(response.data)['objects']
        transaction = transactions[0]
        response = self.client().patch('/transactions/{}'.format(transaction['id']), json=transaction,
                                       headers={'Authorization': 'bearer ' + token})
        return response

    def test_accountant_delete_transaction(self):
        response = self.delete_transaction(self.TOKEN_ACCOUNTANT)
        self.view_message_if_fail(response)
        self.assert_200(response)

    def delete_transaction(self, token):
        self.post_new_transaction(self.TOKEN_ACCOUNTANT)
        response = self.client().get('/transactions',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        transactions = json.loads(response.data)['objects']
        transaction = transactions[0]
        response = self.client().delete('/transactions/{}'.format(transaction['id']),
                                        headers={'Authorization': 'bearer ' + token})
        return response

    def test_accountant_get_transactions(self):
        response = self.get_transactions(self.TOKEN_ACCOUNTANT)
        self.view_message_if_fail(response)
        self.assert_200(response)

    def get_transactions(self, token):
        Movement.query.delete()
        Transaction.query.delete()
        transaction = Transaction(date=datetime.datetime.now(), description=self.faker.name())
        movement = Movement(amount=200)
        movement.transaction = transaction
        self.db.session.add(transaction)
        self.db.session.commit()
        response = self.client().get('/transactions',
                                     headers={'Authorization': 'bearer ' + token})
        return response

    def test_secretary_forbidden_actions(self):
        response = self.add_account(self.TOKEN_SECRETARY)
        self.assert_403(response)
        response = self.update_account(self.TOKEN_SECRETARY)
        self.assert_403(response)
        response = self.delete_account(self.TOKEN_SECRETARY)
        self.assert_403(response)
        response = self.update_transaction(self.TOKEN_SECRETARY)
        self.assert_403(response)
        response = self.delete_transaction(self.TOKEN_SECRETARY)
        self.assert_403(response)

    def test_secretary_post_transactions(self):
        response = self.post_new_transaction(self.TOKEN_SECRETARY)
        self.view_message_if_fail(response)
        self.assert_200(response)

    def test_secretary_get_accounts(self):
        response = self.get_accounts(self.TOKEN_SECRETARY)
        self.view_message_if_fail(response)
        self.assert_200(response)

    def test_secretary_get_transactions(self):
        response = self.get_transactions(self.TOKEN_SECRETARY)
        self.view_message_if_fail(response)
        self.assert_200(response)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
