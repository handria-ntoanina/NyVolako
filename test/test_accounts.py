import unittest
import json
import datetime
import uuid

from models import Account, Movement
from models.enum import AccountTypeEnum

from test import DefaultTestCase


class AccountsTestCase(DefaultTestCase):
    def test_get(self):
        Account.query.delete()
        account = Account()
        name = self.faker.name
        account.name = name
        account_type = AccountTypeEnum.asset
        account.type = account_type
        self.db.session.add(account)
        self.db.session.commit()
        response = self.client().get('/accounts',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        data = json.loads(response.data)
        self.assertEqual(1, len(data['objects']))
        self.assertEqual(name, data['objects'][0].name)
        self.assertEqual(account_type, data['objects'][0].type)

    def test_get_exception(self):
        Account.query.delete()
        self.db.session.commit()
        response = self.client().get('/accounts',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.assert_404(response)

    def test_post(self):
        Account.query.delete()
        self.db.session.commit()
        name = self.faker.name
        account_type = AccountTypeEnum.equity
        response = self.client().post('/accounts', json={'name': name, 'type': account_type.name},
                                      headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        accounts = Account.query.all()
        self.assertEqual(1, len(accounts))
        self.assertEqual(name, accounts[0].name)
        self.assertEqual(account_type, accounts[0].type)

    def test_post_exception(self):
        Account.query.delete()
        self.db.session.commit()
        account_type = AccountTypeEnum.equity
        response = self.client().post('/accounts', json={'name': 'a' * 500, 'type': account_type.name},
                                      headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.assert_422(response)
        response = self.client().post('/accounts', json={'name': self.faker.name, 'type': 'wrong type'},
                                      headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.assert_422(response)
        new_object = {'name': self.faker.name, 'type': account_type.name}
        for i in range(2):
            response = self.client().post('/accounts', json=new_object,
                                          headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.assert_422(response)

    def test_update(self):
        new_object = {'name': self.faker.name, 'type': AccountTypeEnum.equity.name}
        response = self.client().post('/accounts', json=new_object,
                                      headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        response = self.client().get('/accounts',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        data = json.loads(response.data)
        to_update = data['objects'][0]
        to_update['name'] = self.faker.name
        to_update['type'] = AccountTypeEnum.drawing
        response = self.client().patch('/accounts/{}'.format(to_update['id']), json=to_update,
                                       headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        response = self.client().get('/accounts',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        data = json.loads(response.data)
        updated = data['objects'][0]
        for attr in to_update:
            self.assertEqual(to_update(attr), updated(attr))

    def test_update_exception(self):
        new_object = {'name': self.faker.name, 'type': AccountTypeEnum.equity.name}
        response = self.client().post('/accounts', json=new_object,
                                      headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        response = self.client().get('/accounts',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        data = json.loads(response.data)
        to_update = data['objects'][0]
        to_update['name'] = 's' * 200
        to_update['type'] = AccountTypeEnum.drawing
        response = self.client().patch('/accounts/{}'.format(to_update['id']), json=to_update,
                                       headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.assert_422(response)

    def test_delete(self):
        new_object = {'name': self.faker.name, 'type': AccountTypeEnum.equity.name}
        response = self.client().post('/accounts', json=new_object,
                                      headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        response = self.client().get('/accounts',
                                     headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)
        data = json.loads(response.data)
        to_delete = data['objects'][0]
        response = self.client().delete('/accounts/{}'.format(to_delete['id']),
                                        headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.view_message_if_fail(response)
        self.assert_200(response)

    def test_delete_exception(self):
        Account.query.delete()
        account = Account()
        account.name = self.faker.name
        account.type = AccountTypeEnum.asset

        movement = Movement()
        movement.date = datetime.datetime.now()
        movement.amount = 150
        movement.transaction_id = str(uuid.uuid1())
        movement.account = account

        self.db.session.add(account)
        self.db.session.commit()
        account_id = account.id
        response = self.client().delete('/accounts/{}'.format(account_id),
                                        headers={'Authorization': 'bearer ' + self.TOKEN_ACCOUNTANT})
        self.assert_422(response)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
