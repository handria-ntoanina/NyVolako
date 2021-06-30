import datetime
from datetime import timedelta
from dateutil import parser
import json
import unittest

from models import Movement, Account, Transaction
from models.enum import AccountTypeEnum
from test import DefaultTestCase


class TransactionsTestCase(DefaultTestCase):
    def test_get(self):
        Movement.query.delete()
        Transaction.query.delete()
        transaction = Transaction(date=datetime.datetime.now(), description=self.faker.name())
        now = datetime.datetime.now()
        amount = 200
        movement = Movement(amount=amount)
        movement.transaction = transaction
        self.db.session.add(transaction)
        self.db.session.commit()

        response = self.client().get('/transactions',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        data = json.loads(response.data)
        transactions = data['objects']
        self.assertEqual(1, len(transactions))
        movements = transactions[0]['movements']
        self.assertEqual(1, len(movements))
        self.assertLess(now - parser.parse(transactions[0]['date'], ignoretz=True), timedelta(seconds=1))
        self.assertEqual(amount, movements[0]['amount'])

    def test_get_exception(self):
        Movement.query.delete()
        Transaction.query.delete()
        self.db.session.commit()

        response = self.client().get('/transactions',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.assert_404(response)

    def test_post(self):
        Movement.query.delete()
        Transaction.query.delete()
        Account.query.delete()
        self.db.session.commit()
        bank_account = Account(name='Bank', type=AccountTypeEnum.asset)
        sales_account = Account(name='Sales', type=AccountTypeEnum.revenue)
        self.db.session.add(bank_account)
        self.db.session.add(sales_account)
        self.db.session.commit()
        bank_id = bank_account.id
        sales_id = sales_account.id
        self.assertIsNotNone(bank_id)
        self.assertIsNotNone(sales_id)
        now = datetime.datetime.now()
        name = self.faker.name()
        amount = 150
        new_transaction = {'date': now,
                           'description': name,
                           'movements': [
                               {'account_id': bank_id,
                                'amount': amount},
                               {'account_id': sales_id,
                                'amount': amount}
                           ]}
        response = self.client().post('/transactions', json=new_transaction,
                                      headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)

        response = self.client().get('/transactions',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        data = json.loads(response.data)
        transactions = data['objects']
        self.assertEqual(1, len(transactions))
        self.assertLess(now - parser.parse(transactions[0]['date'], ignoretz=True), timedelta(seconds=1))
        self.assertEqual(name, transactions[0]['description'])
        movements = transactions[0]['movements']
        self.assertEqual(2, len(movements))
        accounts_involved = [m['account_id'] for m in movements]
        self.assertTrue(bank_id in accounts_involved)
        self.assertTrue(sales_id in accounts_involved)
        for m in movements:
            self.assertTrue(m['amount'] == amount)

        return transactions[0]['id']

    def test_post_exception(self):
        # Post unbalanced movements
        Movement.query.delete()
        Transaction.query.delete()
        Account.query.delete()
        self.db.session.commit()
        bank_account = Account(name='Bank', type=AccountTypeEnum.asset)
        liability_account = Account(name='Liability', type=AccountTypeEnum.liability)
        self.db.session.add(bank_account)
        self.db.session.add(liability_account)
        self.db.session.commit()
        bank_id = bank_account.id
        liability_id = liability_account.id
        now = datetime.datetime.now()
        name = self.faker.name()
        amount = 150
        new_transaction = {'date': now,
                           'description': name,
                           'movements': [
                               {'account_id': bank_id,
                                'amount': amount},
                               {'account_id': liability_id,
                                'amount': -amount}
                           ]}
        response = self.client().post('/transactions', json=new_transaction,
                                      headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.assert_422(response)

    def test_update(self):
        # First post a transaction
        # then modify that transaction
        transaction_id = self.test_post()
        equity_account = Account(name='Owner Equity', type=AccountTypeEnum.equity)
        expense_account = Account(name='Expenditure', type=AccountTypeEnum.expense)
        self.db.session.add(equity_account)
        self.db.session.add(expense_account)
        self.db.session.commit()
        equity_id = equity_account.id
        expense_id = expense_account.id
        now = datetime.datetime.now()
        name = self.faker.name()
        amount = 510
        updated_transaction = {'date': now,
                               'description': name,
                               'movements': [
                                   {'account_id': equity_id,
                                    'amount': amount},
                                   {'account_id': expense_id,
                                    'amount': amount}
                               ]}
        response = self.client().patch('/transactions/{}'.format(transaction_id), json=updated_transaction,
                                       headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)

        # Check the saved transaction
        response = self.client().get('/transactions',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        data = json.loads(response.data)
        transactions = data['objects']
        self.assertEqual(1, len(transactions))
        self.assertLess(now - parser.parse(transactions[0]['date'], ignoretz=True), timedelta(seconds=1))
        self.assertEqual(name, transactions[0]['description'])
        movements = transactions[0]['movements']
        self.assertEqual(2, len(movements))
        accounts_involved = [m['account_id'] for m in movements]
        self.assertTrue(equity_id in accounts_involved)
        self.assertTrue(expense_id in accounts_involved)
        for m in movements:
            self.assertTrue(m['amount'] == amount)

    def test_update_exception(self):
        # Post a transaction
        # Try to update with non balanced movements
        transaction_id = self.test_post()
        equity_account = Account(name='Owner Equity', type=AccountTypeEnum.equity)
        expense_account = Account(name='Expenditure', type=AccountTypeEnum.expense)
        self.db.session.bulk_save_objects([equity_account, expense_account])
        self.db.session.commit()
        equity_id = equity_account.id
        expense_id = expense_account.id
        now = datetime.datetime.now()
        name = self.faker.name()
        amount = 123
        updated_transaction = {'date': now,
                               'description': name,
                               'movements': [
                                   {'account_id': equity_id,
                                    'amount': amount},
                                   {'account_id': expense_id,
                                    'amount': -amount}
                               ]}
        response = self.client().patch('/transactions/{}'.format(transaction_id), json=updated_transaction,
                                       headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.assert_422(response)

    def test_delete(self):
        transaction_id_to_delete = self.test_post()

        response = self.client().delete('/transactions/{}'.format(transaction_id_to_delete),
                                        headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)

        # Check that there is no transaction left
        response = self.client().get('/transactions',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.assert_404(response)

    def test_delete_exception(self):
        # Delete a non existing transaction
        Movement.query.delete()
        Transaction.query.delete()
        Account.query.delete()
        self.db.session.commit()
        transaction_id_to_delete = 5
        response = self.client().delete('/transactions/{}'.format(transaction_id_to_delete),
                                        headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.assert_404(response)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

